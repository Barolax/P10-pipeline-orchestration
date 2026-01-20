import duckdb
import yaml

# Charger la config de test
with open('config/test_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Connexion DuckDB
conn = duckdb.connect()

print("=== TESTS NETTOYAGE ===\n")

# Test ERP
result = conn.execute("SELECT COUNT(*) FROM erp_clean").fetchone()[0]
expected = config['nettoyage']['erp_apres_dedoublonnage']
assert result == expected, f"❌ ERP: {result} lignes au lieu de {expected}"
print(f"✅ ERP: {result} lignes")

# Test LIAISON
result = conn.execute("SELECT COUNT(*) FROM liaison_clean").fetchone()[0]
expected = config['nettoyage']['liaison_apres_dedoublonnage']
assert result == expected, f"❌ LIAISON: {result} lignes au lieu de {expected}"
print(f"✅ LIAISON: {result} lignes")

# Test WEB après nettoyage
result = conn.execute("SELECT COUNT(*) FROM web_clean").fetchone()[0]
expected = config['nettoyage']['web_apres_nettoyage']
assert result == expected, f"❌ WEB clean: {result} lignes au lieu de {expected}"
print(f"✅ WEB clean: {result} lignes")

# Test WEB après dédoublonnage
result = conn.execute("SELECT COUNT(*) FROM web_dedup").fetchone()[0]
expected = config['nettoyage']['web_apres_dedoublonnage']
assert result == expected, f"❌ WEB dedup: {result} lignes au lieu de {expected}"
print(f"✅ WEB dedup: {result} lignes")

print("\n✅ Tous les tests de nettoyage sont OK !")

conn.close()