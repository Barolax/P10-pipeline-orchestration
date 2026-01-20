-- Chargement et vérification du fichier ERP
-- Normalement déjà propre (pas de doublons, pas de valeurs manquantes)

CREATE OR REPLACE TABLE erp_clean AS
SELECT *
FROM read_excel('data_bottleneck/erp.xlsx');

-- Vérification : pas de doublons sur product_id
SELECT 
    COUNT(*) as total_lignes,
    COUNT(DISTINCT product_id) as product_id_uniques
FROM erp_clean;