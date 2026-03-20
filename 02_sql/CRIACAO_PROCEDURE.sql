USE operacional_db;
GO

CREATE OR ALTER PROCEDURE sp_tratar_carga_operacional
AS
BEGIN
    SET NOCOUNT ON;

    ------------------------------------------------------------
    -- 0. LIMPEZA CONTROLADA (EVITA DUPLICIDADE)
    ------------------------------------------------------------
    TRUNCATE TABLE fato_forecast;
    TRUNCATE TABLE fato_real;

    ------------------------------------------------------------
    -- 1. DIM_TEMPO
    ------------------------------------------------------------
    INSERT INTO dim_tempo (data, ano, mes, semana)
    SELECT DISTINCT
        d.data,
        YEAR(d.data),
        MONTH(d.data),
        DATEPART(WEEK, d.data)
    FROM (
        SELECT
            TRY_CONVERT(
                DATE,
                REPLACE(REPLACE(LTRIM(RTRIM(Data)), '"', ''), CHAR(13), ''),
                23
            ) AS data
        FROM stg_forecast
    ) d
    WHERE d.data IS NOT NULL
      AND NOT EXISTS (
            SELECT 1
            FROM dim_tempo t
            WHERE t.data = d.data
      );

    ------------------------------------------------------------------
    -- 2. DIM_INTERVALO (PADRÃO TIME, DERIVADO DO FORECAST)
    ------------------------------------------------------------------
    INSERT INTO dim_intervalo (intervalo)
    SELECT DISTINCT
        TRY_CONVERT(
            TIME,
            REPLACE(REPLACE(LTRIM(RTRIM(Intervalo)), '"', ''), CHAR(13), '')
        )
    FROM stg_forecast
    WHERE TRY_CONVERT(
            TIME,
            REPLACE(REPLACE(LTRIM(RTRIM(Intervalo)), '"', ''), CHAR(13), '')
        ) IS NOT NULL
    AND NOT EXISTS (
        SELECT 1
        FROM dim_intervalo i
        WHERE i.intervalo = TRY_CONVERT(
            TIME,
            REPLACE(REPLACE(LTRIM(RTRIM(Intervalo)), '"', ''), CHAR(13), '')
        )
    );

    ------------------------------------------------------------
    -- 3. DIM_SKILL (DEPARA)
    ------------------------------------------------------------
    INSERT INTO dim_skill (
        id_skill,
        skill_nome,
        ACD,
        INI_VIGENCIA,
        FIM_VIGENCIA
    )
    SELECT DISTINCT
        TRY_CONVERT(INT, REPLACE(REPLACE(id_skill, '"', ''), CHAR(13), '')),
        REPLACE(REPLACE(OPERACOES, '"', ''), CHAR(13), ''),
        TRY_CONVERT(INT, REPLACE(REPLACE(ACD, '"', ''), CHAR(13), '')),
        TRY_CONVERT(DATE, REPLACE(REPLACE(INI_VIGENCIA, '"', ''), CHAR(13), ''), 23),
        TRY_CONVERT(DATE, REPLACE(REPLACE(FIM_VIGENCIA, '"', ''), CHAR(13), ''), 23)
    FROM stg_depara_skill
    WHERE TRY_CONVERT(INT, REPLACE(REPLACE(id_skill, '"', ''), CHAR(13), '')) IS NOT NULL
      AND NOT EXISTS (
            SELECT 1
            FROM dim_skill s
            WHERE s.id_skill = TRY_CONVERT(INT, REPLACE(REPLACE(id_skill, '"', ''), CHAR(13), ''))
      );

    ------------------------------------------------------------
    -- 3.1 SKILL PADRÃO PARA NÃO MAPEADOS
    ------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM dim_skill WHERE id_skill = -1)
    BEGIN
        INSERT INTO dim_skill (id_skill, skill_nome, ACD, INI_VIGENCIA, FIM_VIGENCIA)
        VALUES (-1, 'NAO MAPEADO', NULL, '1900-01-01', '2999-12-31');
    END;

    ------------------------------------------------------------
    -- 4. FATO_FORECAST (GLOBAL)
    ------------------------------------------------------------
    INSERT INTO fato_forecast (
        id_tempo,
        id_intervalo,
        volume_forecast,
        tma_forecast,
        ns_forecast,
        hc_forecast
    )
    SELECT
        t.id_tempo,
        i.id_intervalo,
        TRY_CONVERT(FLOAT, REPLACE(REPLACE(f.Volume_Forecast, '"', ''), CHAR(13), '')),
        TRY_CONVERT(FLOAT, REPLACE(REPLACE(f.TMA_Forecast, '"', ''), CHAR(13), '')),
        TRY_CONVERT(FLOAT, REPLACE(REPLACE(f.NS_Forecast, '"', ''), CHAR(13), '')),
        TRY_CONVERT(FLOAT, REPLACE(REPLACE(f.HC_Forecast, '"', ''), CHAR(13), ''))
    FROM stg_forecast f
    JOIN dim_tempo t
        ON t.data = TRY_CONVERT(
            DATE,
            REPLACE(REPLACE(f.Data, '"', ''), CHAR(13), ''),
            23
        )
    JOIN dim_intervalo i
        ON i.intervalo = TRY_CONVERT(
            TIME,
            REPLACE(REPLACE(f.Intervalo, '"', ''), CHAR(13), '')
        );

    ------------------------------------------------------------
    -- 5. FATO_REAL (HSPLIT + HAGENT)
    ------------------------------------------------------------
    INSERT INTO fato_real (
        id_tempo,
        id_intervalo,
        id_skill,
        ACD,
        Split,
        chamadas_recebidas,
        chamadas_atendidas,
        tempo_falado,
        tempo_espera,
        tempo_logado,
        tempo_pausa
    )
    SELECT
        t.id_tempo,
        i.id_intervalo,
        ISNULL(s.id_skill, -1),
        TRY_CONVERT(INT, REPLACE(REPLACE(r.ACD, '"', ''), CHAR(13), '')),
        TRY_CONVERT(INT, REPLACE(REPLACE(r.Split, '"', ''), CHAR(13), '')),
        TRY_CONVERT(INT, REPLACE(REPLACE(r.Chamadas_Recebidas, '"', ''), CHAR(13), '')),
        TRY_CONVERT(INT, REPLACE(REPLACE(r.Chamadas_Atendidas, '"', ''), CHAR(13), '')),
        TRY_CONVERT(INT, REPLACE(REPLACE(r.Tempo_Falado, '"', ''), CHAR(13), '')),
        TRY_CONVERT(INT, REPLACE(REPLACE(r.Tempo_Espera, '"', ''), CHAR(13), '')),
        TRY_CONVERT(INT, REPLACE(REPLACE(a.Tempo_Logado, '"', ''), CHAR(13), '')),
        TRY_CONVERT(INT, REPLACE(REPLACE(a.Tempo_Pausa, '"', ''), CHAR(13), ''))
    FROM stg_hsplit r
    LEFT JOIN stg_hagent a
        ON r.Data = a.Data
       AND r.Intervalo = a.Intervalo
       AND r.ACD = a.ACD
       AND r.Split = a.Split
    JOIN dim_tempo t
        ON t.data = TRY_CONVERT(
            DATE,
            REPLACE(REPLACE(r.Data, '"', ''), CHAR(13), ''),
            23
        )
    JOIN dim_intervalo i
        ON i.intervalo = DATEADD(
            MINUTE,
            TRY_CONVERT(INT, REPLACE(REPLACE(r.Intervalo, '"', ''), CHAR(13), '')),
            CAST('00:00:00' AS TIME)
        )

    LEFT JOIN dim_skill s
        ON s.ACD = TRY_CONVERT(INT, REPLACE(REPLACE(r.ACD, '"', ''), CHAR(13), ''))
       AND s.id_skill = TRY_CONVERT(INT, REPLACE(REPLACE(r.Split, '"', ''), CHAR(13), ''));

END;
GO

