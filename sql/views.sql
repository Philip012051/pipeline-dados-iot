-- VIEW 1: Temperatura media por dispositivo
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT
    dispositivo_id,
    ROUND(AVG(temperatura)::numeric, 2) AS temperatura_media
FROM leituras_temperatura
GROUP BY dispositivo_id;

-- VIEW 2: Quantidade de leituras por hora
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM data_leitura)::integer AS hora,
    COUNT(*) AS quantidade_leituras
FROM leituras_temperatura
GROUP BY EXTRACT(HOUR FROM data_leitura)
ORDER BY hora;

-- VIEW 3: Temperatura maxima e minima por dia
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    data_leitura::date AS data,
    MAX(temperatura) AS temperatura_maxima,
    MIN(temperatura) AS temperatura_minima
FROM leituras_temperatura
GROUP BY data_leitura::date;