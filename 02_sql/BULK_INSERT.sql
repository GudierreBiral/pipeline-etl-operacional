
USE operacional_db;
GO

BULK INSERT stg_depara_skill
FROM 'C:\etl_operacional\saida_csv\depara_skill.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '0x0A',
    CODEPAGE = '65001', -- UTF-8
    TABLOCK
);


TRUNCATE TABLE stg_forecast;

BULK INSERT stg_forecast
FROM 'C:\etl_operacional\saida_csv\forecast.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '0x0A',
    CODEPAGE = '65001',
    TABLOCK
);


TRUNCATE TABLE stg_hsplit;

BULK INSERT stg_hsplit
FROM 'C:\etl_operacional\saida_csv\hsplit.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '0x0A',
    CODEPAGE = '65001',
    TABLOCK
);


TRUNCATE TABLE stg_hagent;

BULK INSERT stg_hagent
FROM 'C:\etl_operacional\saida_csv\hagent.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '0x0A',
    CODEPAGE = '65001',
    TABLOCK
);


--select top 10 * from stg_forecast;