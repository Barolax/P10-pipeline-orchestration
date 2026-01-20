import duckdb
import yaml

# Charger la config de test
with open('config/test_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Connexion DuckDB
conn = duckdb.connect()

print("=== TESTS CALCUL CA ===\n")

# Test CA total
result = conn.execute("SELECT chiffre_affaires_total FROM ca_total").fetchone()[0]
expected = config['calculs']['ca_total']
tolerance = config['calculs']['tolerance_ca']

diff = abs(result - expected)
assert diff < tolerance, f"❌ CA total: {result}€ au lieu de {expected}€ (diff: {diff}€)"
print(f"✅ CA total: {result:.2f}€ (attendu: {expected}€)")

# Vérifier qu'aucun CA n'est NULL
null_count = conn.execute("SELECT COUNT(*) FROM data_finale WHERE ca IS NULL").fetchone()[0]
assert null_count == 0, f"❌ {null_count} valeurs NULL dans ca"
print(f"✅ Aucune valeur NULL dans ca")

# Vérifier que le rapport CA contient bien 714 produits
nb_produits = conn.execute("SELECT COUNT(*) FROM rapport_ca").fetchone()[0]
assert nb_produits == 714, f"❌ Rapport CA: {nb_produits} produits au lieu de 714"
print(f"✅ Rapport CA: {nb_produits} produits")

print("\n✅ Tous les tests de calcul CA sont OK !")

conn.close()