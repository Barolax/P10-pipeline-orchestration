-- Calcul du chiffre d'affaires
-- CA = price × total_sales

-- Ajouter la colonne ca à data_finale
ALTER TABLE data_finale ADD COLUMN IF NOT EXISTS ca DOUBLE;

UPDATE data_finale 
SET ca = price * total_sales;

-- Calcul du CA total
CREATE OR REPLACE TABLE ca_total AS
SELECT SUM(ca) as chiffre_affaires_total
FROM data_finale;

-- Afficher le résultat
SELECT * FROM ca_total;

-- Créer le rapport CA par produit
CREATE OR REPLACE TABLE rapport_ca AS
SELECT 
    product_id,
    post_title,
    price,
    total_sales,
    ca
FROM data_finale
ORDER BY ca DESC;

-- Afficher les stats
SELECT 
    COUNT(*) as nb_produits,
    ROUND(SUM(ca), 2) as ca_total,
    ROUND(AVG(ca), 2) as ca_moyen,
    ROUND(MIN(ca), 2) as ca_min,
    ROUND(MAX(ca), 2) as ca_max
FROM rapport_ca;