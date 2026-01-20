import duckdb
import yaml

# Charger la config de test
with open('config/test_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Connexion DuckDB
conn = duckdb.connect()

print("=== IDENTIFICATION VINS PREMIUM ===\n")

# Calculer le z-score
conn.execute("""
    ALTER TABLE data_finale ADD COLUMN IF NOT EXISTS z_score DOUBLE;
    
    UPDATE data_finale
    SET z_score = (price - (SELECT AVG(price) FROM data_finale)) / 
                  (SELECT STDDEV(price) FROM data_finale);
""")

# Statistiques
prix_moyen = conn.execute("SELECT AVG(price) FROM data_finale").fetchone()[0]
prix_std = conn.execute("SELECT STDDEV(price) FROM data_finale").fetchone()[0]
seuil = config['identification']['zscore_seuil']

print(f"Prix moyen: {prix_moyen:.2f}€")
print(f"Écart-type: {prix_std:.2f}€")
print(f"Seuil z-score: {seuil}")

# Créer les tables vins premium et ordinaires
conn.execute(f"""
    CREATE OR REPLACE TABLE vins_premium AS
    SELECT 
        product_id,
        post_title,
        price,
        total_sales,
        ca,
        z_score
    FROM data_finale
    WHERE z_score > {seuil}
    ORDER BY z_score DESC;
""")

conn.execute(f"""
    CREATE OR REPLACE TABLE vins_ordinaires AS
    SELECT 
        product_id,
        post_title,
        price,
        total_sales,
        ca,
        z_score
    FROM data_finale
    WHERE z_score <= {seuil}
    ORDER BY ca DESC;
""")

# Afficher les résultats
nb_premium = conn.execute("SELECT COUNT(*) FROM vins_premium").fetchone()[0]
nb_ordinaires = conn.execute("SELECT COUNT(*) FROM vins_ordinaires").fetchone()[0]

print(f"\n🍷 Vins premium: {nb_premium}")
print(f"🍷 Vins ordinaires: {nb_ordinaires}")

# Export des fichiers
conn.execute("COPY vins_premium TO 'outputs/vins_premium.csv' (HEADER, DELIMITER ',');")
conn.execute("COPY vins_ordinaires TO 'outputs/vins_ordinaires.csv' (HEADER, DELIMITER ',');")
conn.execute("COPY rapport_ca TO 'outputs/rapport_ca.xlsx' WITH (FORMAT GDAL, DRIVER 'xlsx');")

print("\n✅ Fichiers exportés dans outputs/")

conn.close()