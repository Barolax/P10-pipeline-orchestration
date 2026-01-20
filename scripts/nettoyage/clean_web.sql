-- Nettoyage du fichier WEB
-- Étape 1 : Suppression des lignes avec sku manquant
-- Étape 2 : Dédoublonnage avec stratégie MAX sur total_sales

-- Étape 1 : Supprimer les valeurs manquantes
CREATE OR REPLACE TABLE web_clean AS
SELECT *
FROM read_excel('data_bottleneck/web.xlsx')
WHERE sku IS NOT NULL;

-- Étape 2 : Dédoublonnage avec MAX sur total_sales
CREATE OR REPLACE TABLE web_dedup AS
SELECT * FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY sku ORDER BY total_sales DESC) as rn
    FROM web_clean
) WHERE rn = 1;

-- Supprimer la colonne auxiliaire
ALTER TABLE web_dedup DROP COLUMN rn;

-- Vérifications
SELECT 'Après nettoyage' as etape, COUNT(*) as nb_lignes FROM web_clean
UNION ALL
SELECT 'Après dédoublonnage' as etape, COUNT(*) as nb_lignes FROM web_dedup;