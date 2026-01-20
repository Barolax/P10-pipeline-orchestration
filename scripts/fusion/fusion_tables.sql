-- Fusion des 3 fichiers
-- Étape 1 : ERP + LIAISON
-- Étape 2 : Résultat + WEB

-- Fusion ERP + LIAISON sur product_id
CREATE OR REPLACE TABLE erp_liaison AS
SELECT 
    e.*,
    l.id_web
FROM erp_clean e
INNER JOIN liaison_clean l ON e.product_id = l.product_id;

-- Fusion avec WEB sur id_web = sku
CREATE OR REPLACE TABLE data_finale AS
SELECT 
    el.*,
    w.total_sales,
    w.post_title,
    w.virtual,
    w.downloadable,
    w.rating_count,
    w.average_rating
FROM erp_liaison el
INNER JOIN web_dedup w ON el.id_web = w.sku;

-- Vérifications
SELECT 'ERP + LIAISON' as etape, COUNT(*) as nb_lignes FROM erp_liaison
UNION ALL
SELECT 'Fusion finale' as etape, COUNT(*) as nb_lignes FROM data_finale;