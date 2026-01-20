- id: test_nettoyage
    type: io.kestra.plugin.scripts.python.Script
    description: Tests de validation du nettoyage
    docker:
      image: bottleneck-pipeline:latest
    inputFiles:
      test_config.yaml: "{{ inputs.config_file }}"
      erp_clean.parquet: "{{ outputs['nettoyage-complet'].outputFiles['erp_clean.parquet'] }}"
      liaison_clean.parquet: "{{ outputs['nettoyage-complet'].outputFiles['liaison_clean.parquet'] }}"
      web_clean.parquet: "{{ outputs['nettoyage-complet'].outputFiles['web_clean.parquet'] }}"
      web_dedup.parquet: "{{ outputs['nettoyage-complet'].outputFiles['web_dedup.parquet'] }}"
    script: |
      import duckdb
      import yaml
      
      with open('test_config.yaml', 'r') as f:
          config = yaml.safe_load(f)
      
      conn = duckdb.connect()
      
      # IMPORTER LES TABLES
      conn.execute("CREATE TABLE erp_clean AS SELECT * FROM 'erp_clean.parquet'")
      conn.execute("CREATE TABLE liaison_clean AS SELECT * FROM 'liaison_clean.parquet'")
      conn.execute("CREATE TABLE web_clean AS SELECT * FROM 'web_clean.parquet'")
      conn.execute("CREATE TABLE web_dedup AS SELECT * FROM 'web_dedup.parquet'")
      
      print("=== TESTS NETTOYAGE ===\n")
      
      # Test ERP
      result = conn.execute("SELECT COUNT(*) FROM erp_clean").fetchone()[0]
      expected = config['nettoyage']['erp_apres_dedoublonnage']
      assert result == expected, f"❌ ERP: {result} au lieu de {expected}"
      print(f"✅ ERP: {result} lignes")
      
      # Test LIAISON
      result = conn.execute("SELECT COUNT(*) FROM liaison_clean").fetchone()[0]
      expected = config['nettoyage']['liaison_apres_dedoublonnage']
      assert result == expected, f"❌ LIAISON: {result} au lieu de {expected}"
      print(f"✅ LIAISON: {result} lignes")
      
      # Test WEB clean
      result = conn.execute("SELECT COUNT(*) FROM web_clean").fetchone()[0]
      expected = config['nettoyage']['web_apres_nettoyage']
      assert result == expected, f"❌ WEB clean: {result} au lieu de {expected}"
      print(f"✅ WEB clean: {result} lignes")
      
      # Test WEB dedup
      result = conn.execute("SELECT COUNT(*) FROM web_dedup").fetchone()[0]
      expected = config['nettoyage']['web_apres_dedoublonnage']
      assert result == expected, f"❌ WEB dedup: {result} au lieu de {expected}"
      print(f"✅ WEB dedup: {result} lignes")
      
      print("\n✅ Tous les tests de nettoyage OK !")
      conn.close()