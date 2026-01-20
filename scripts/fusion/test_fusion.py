import duckdb
import yaml

# Charger la config de test
with open('config/test_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Connexion DuckDB
conn = duckdb.connect()

print("=== TESTS FUSION ===\n")

# Test fusion finale
result = conn.execute("SELECT COUNT(*) FROM data_finale").fetchone()[0]
expected = config['fusion']['lignes_finales']
assert result == expected, f"❌ Fusion finale: {result} lignes au lieu de {expected}"
print(f"✅ Fusion finale: {result} lignes")

# Vérifier qu'on a bien les colonnes nécessaires
columns = conn.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'data_finale'
""").fetchall()

required_cols = ['price', 'total_sales', 'product_id', 'post_title']
for col in required_cols:
    assert any(col in str(c) for c in columns), f"❌ Colonne manquante: {col}"
print(f"✅ Toutes les colonnes nécessaires sont présentes")

print("\n✅ Tous les tests de fusion sont OK !")

conn.close()