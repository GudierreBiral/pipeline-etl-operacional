--Fato Forecast
CREATE TABLE fato_forecast (
    id_tempo INT,
    id_intervalo INT,
    volume_forecast FLOAT,
    tma_forecast FLOAT,
    ns_forecast FLOAT,
    hc_forecast FLOAT
);


--Fato Real Unificado
CREATE TABLE fato_real (
    id_tempo INT,
    id_intervalo INT,
    id_skill INT,
    ACD INT,
    Split INT,
    chamadas_recebidas INT,
    chamadas_atendidas INT,
    tempo_falado INT,
    tempo_espera INT,
    tempo_logado INT,
    tempo_pausa INT
);