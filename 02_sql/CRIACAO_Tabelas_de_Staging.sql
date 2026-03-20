--DEPARA_SKILL
CREATE TABLE stg_depara_skill (
    SEGMENTOS VARCHAR(100),
    OPERACOES VARCHAR(200),
    Skill_Tecnica INT,
    OPERACOES_FORECAST VARCHAR(200),
    INI_VIGENCIA DATE,
    FIM_VIGENCIA DATE,
    SERVIDOR VARCHAR(50),
    GRUPO VARCHAR(50),
    ACD INT,
    SEGMENTOS_CALCULADORA_FIN VARCHAR(100),
    DUMMY INT,
    CH INT,
    CH_Minutos INT,
    Consolidado VARCHAR(100),
    ALTERACAO DATE,
    CHAMADO VARCHAR(50),
    id_skill INT
);

--FORECAST
CREATE TABLE stg_forecast (
    Data DATE,
    Intervalo TIME,
    Skill VARCHAR(50),
    Volume_Forecast FLOAT,
    TMA_Forecast FLOAT,
    NS_Forecast FLOAT,
    HC_Forecast FLOAT
);

--HAGENT
CREATE TABLE stg_hagent (
    Data DATE,
    Intervalo INT,
    ACD INT,
    Split INT,
    Tempo_Logado INT,
    Tempo_Disponivel INT,
    Tempo_Pausa INT
);

--HSPLIT
CREATE TABLE stg_hsplit (
    Data DATE,
    Intervalo INT,
    ACD INT,
    Split INT,
    Chamadas_Recebidas INT,
    Chamadas_Atendidas INT,
    Tempo_Falado INT,
    Tempo_Espera INT
);
