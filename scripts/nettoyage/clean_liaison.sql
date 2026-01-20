-- Chargement et vérification du fichier LIAISON
-- Normalement déjà propre (pas de doublons sur product_id)

CREATE OR REPLACE TABLE liaison_clean AS
SELECT *
FROM read_excel('data_bottleneck/liaison.xlsx');

-- Vérification : pas de doublons sur product_id
SELECT 
    COUNT(*) as total_lignes,
    COUNT(DISTINCT product_id) as product_id_uniques,
    COUNT(DISTINCT id_web) as id_web_uniques
FROM liaison_clean;