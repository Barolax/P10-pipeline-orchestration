import duckdb
import yaml

# Charger la config de test
with open('config/test_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Connexion DuckDB
conn = duckdb.connect()

print("=== TESTS VINS PREMIUM ===\n")

# Test nombre de vins premium
result = conn.execute("SELECT COUNT(*) FROM vins_premium").fetchone()[0]
expected = config['identification']['vins_premium']
assert result == expected, f"❌ Vins premium: {result} au lieu de {expected}"
print(f"✅ Vins premium: {result} (attendu: {expected})")

# Vérifier que tous les z-scores premium sont > 2
min_zscore = conn.execute("SELECT MIN(z_score) FROM vins_premium").fetchone()[0]
seuil = config['identification']['zscore_seuil']
assert min_zscore > seuil, f"❌ Z-score min des premium: {min_zscore} (doit être > {seuil})"
print(f"✅ Tous les vins premium ont z-score > {seuil}")

# Vérifier que tous les z-scores ordinaires sont <= 2
max_zscore = conn.execute("SELECT MAX(z_score) FROM vins_ordinaires").fetchone()[0]
assert max_zscore <= seuil, f"❌ Z-score max des ordinaires: {max_zscore} (doit être <= {seuil})"
print(f"✅ Tous les vins ordinaires ont z-score <= {seuil}")

# Vérifier le total
total = conn.execute("SELECT COUNT(*) FROM vins_premium").fetchone()[0] + \
        conn.execute("SELECT COUNT(*) FROM vins_ordinaires").fetchone()[0]
assert total == 714, f"❌ Total: {total} au lieu de 714"
print(f"✅ Total vins: {total}")

print("\n✅ Tous les tests vins premium sont OK !")

conn.close()