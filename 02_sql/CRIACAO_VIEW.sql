CREATE OR ALTER VIEW vw_operacional_consolidado AS
SELECT
    t.data,
    i.intervalo,
    s.skill_nome,
    f.volume_forecast,
    f.tma_forecast,
    f.ns_forecast,
    f.hc_forecast,
    r.chamadas_recebidas,
    r.chamadas_atendidas,
    r.tempo_falado,
    r.tempo_espera,
    r.tempo_logado,
    r.tempo_pausa
FROM fato_forecast f
JOIN dim_tempo t ON f.id_tempo = t.id_tempo
JOIN dim_intervalo i ON f.id_intervalo = i.id_intervalo
LEFT JOIN fato_real r
    ON r.id_tempo = f.id_tempo
   AND r.id_intervalo = f.id_intervalo
LEFT JOIN dim_skill s
    ON r.id_skill = s.id_skill;
