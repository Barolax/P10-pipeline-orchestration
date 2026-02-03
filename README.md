# P10 - Pipeline d'orchestration de flux de données

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-24.0-blue)
![Kestra](https://img.shields.io/badge/Kestra-latest-orange)
![Status](https://img.shields.io/badge/Status-Complete-success)


## 📋 Contexte

Projet de mise en place d'un pipeline automatisé pour **BottleNeck**, marchand de vins en ligne.

**Objectif :** Automatiser le processus mensuel d'analyse des ventes (actuellement manuel) pour :
- Calculer le chiffre d'affaires par produit
- Identifier les vins premium via analyse statistique (z-score)
- Générer des rapports pour les responsables produits

---

## 🎯 Livrables

- ✅ Workflow d'orchestration Kestra (`.yaml`)
- ✅ Pipeline automatisé avec 14 tâches
- ✅ 7 tests de validation automatisés
- ✅ Rapport CA en Excel (`.xlsx`)
- ✅ Extractions vins premium/ordinaires (`.csv`)
- ✅ Planification mensuelle (15 du mois à 9h)

---

## 🏗️ Architecture
```
P10 - mise en place pipeline orchestration de flux/
├── data_bottleneck/          # Fichiers sources (ERP, LIAISON, WEB)
├── config/
│   └── test_config.yaml      # Valeurs de référence pour tests
├── notebooks/
│   └── exploration.ipynb     # EDA complète
├── scripts/
│   ├── nettoyage/           # Scripts SQL/Python de nettoyage + tests
│   ├── fusion/              # Scripts fusion + tests
│   ├── calculs/             # Scripts calcul CA + tests
│   └── premium/             # Script identification vins premium + tests
├── kestra/
│   └── workflow.yaml        # Workflow d'orchestration
├── diagrams/
│   └── P10.drawio.png       # Logigramme du pipeline
├── Dockerfile               # Image Docker personnalisée
└── requirements.txt
```

---

## 🛠️ Technologies

- **Orchestration :** Kestra
- **Conteneurisation :** Docker
- **Base de données :** DuckDB (in-memory)
- **Langage :** Python 3.11, SQL
- **Bibliothèques :** pandas, scipy, openpyxl, pyyaml
- **Format d'échange :** Parquet

---

## 📊 Workflow

Le pipeline comprend **14 tâches** organisées en DAG :

### 1. Nettoyage (5 tâches)
- `nettoyage-complet` : Suppression valeurs manquantes + dédoublonnage
- `test-nettoyage-erp` : Validation 825 lignes
- `test-nettoyage-liaison` : Validation 825 lignes
- `test-nettoyage-web-clean` : Validation 1428 lignes
- `test-nettoyage-web-dedup` : Validation 714 lignes

### 2. Fusion (2 tâches)
- `fusion-tables` : INNER JOIN ERP + LIAISON + WEB
- `test-fusion` : Validation 714 lignes finales

### 3. Calcul CA (2 tâches)
- `calcul-ca` : Calcul CA = price × total_sales
- `test-ca` : Validation CA total = 70 568,60€

### 4. Identification vins premium (3 tâches)
- `identification-premium` : Calcul z-score, séparation premium/ordinaires
- `test-premium` : Validation 30 vins premium (z-score > 2)
- `notification-succes` : Message de fin

---

## 🧪 Tests automatisés

7 tests de validation avec alertes granulaires :

| Test | Critère | Valeur attendue |
|------|---------|----------------|
| ERP | Absence doublons | 825 lignes |
| LIAISON | Absence doublons | 825 lignes |
| WEB clean | Suppression valeurs manquantes | 1428 lignes |
| WEB dedup | Dédoublonnage | 714 lignes |
| Fusion | Cohérence volumétrie | 714 lignes |
| CA | Cohérence calcul | 70 568,60€ |
| Premium | Cohérence z-score | 30 vins |

---

## 🐳 Docker

Image personnalisée `bottleneck-pipeline:latest` contenant :
- Python 3.11
- DuckDB 1.4.3
- pandas, openpyxl, scipy, pyyaml

**Build :**
```bash
docker build -t bottleneck-pipeline:latest .
```

---

## 🚀 Déploiement

### Prérequis
- Docker Desktop installé et démarré

### 1. Construire l'image Docker du pipeline
```bash
docker build -t bottleneck-pipeline:latest .
```

### 2. Lancer Kestra dans un container
```bash
docker run -d \
  --name kestra-server \
  --user root \
  -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  kestra/kestra:latest \
  server local
```

**Note :** Kestra tourne dans un container Docker qui a accès au socket Docker pour lancer d'autres containers (pour les tâches du pipeline).

### 3. Accéder à l'interface Kestra
Ouvrir un navigateur : http://localhost:8080

### 4. Importer le workflow
1. Copier le contenu de `kestra/workflow.yaml`
2. Créer un nouveau flow dans Kestra
3. Coller le workflow

### 5. Exécuter le pipeline
1. Cliquer sur "Execute"
2. Uploader les 4 fichiers :
   - `data_bottleneck/erp.xlsx`
   - `data_bottleneck/liaison.xlsx`
   - `data_bottleneck/web.xlsx`
   - `config/test_config.yaml`
3. Lancer l'exécution
4. Suivre les logs en temps réel

---

## 📅 Planification

**Trigger cron :** `0 9 15 * *`

Exécution automatique le **15 de chaque mois à 9h**

---

## 📈 Résultats

Le pipeline génère automatiquement :
- `rapport_ca.xlsx` : Chiffre d'affaires par produit
- `vins_premium.csv` : 30 vins avec z-score > 2
- `vins_ordinaires.csv` : 684 vins avec z-score ≤ 2

---

## 🔧 Défis techniques

### Persistance des données
**Problème :** Chaque tâche Kestra s'exécute dans un container isolé → données perdues entre tâches

**Solution :** Export/Import systématique en Parquet

### Dédoublonnage WEB
**Problème :** 3 SKU avec `total_sales` différents entre doublons

**Solution :** Stratégie MAX (tri DESC + keep first)

### Tests granulaires
**Problème :** Alerte globale peu informative

**Solution :** 7 tests séparés = identification précise des erreurs

---

## 🔮 Améliorations futures

- Notifications automatiques (email/Slack)
- Dashboard de monitoring (Grafana)
- Retry automatique en cas d'erreur
- Historisation mensuelle des données

---

## 👤 Auteur
Axelle 
Data Engineer - OpenClassrooms  
Projet P10 - [Fév 2026]