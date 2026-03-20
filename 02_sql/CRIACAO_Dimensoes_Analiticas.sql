--Dimensão Tempo
CREATE TABLE dim_tempo (
    id_tempo INT IDENTITY PRIMARY KEY,
    data DATE UNIQUE,
    ano INT,
    mes INT,
    semana INT
);

--Dimensão Intervalo
CREATE TABLE dim_intervalo (
    id_intervalo INT IDENTITY PRIMARY KEY,
    intervalo INT UNIQUE
);

--Dimensão Skill (vem do DEPARA)
CREATE TABLE dim_skill (
    id_skill INT PRIMARY KEY,
    skill_nome VARCHAR(200),
    ACD INT,
    INI_VIGENCIA DATE,
    FIM_VIGENCIA DATE
);