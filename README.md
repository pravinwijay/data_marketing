# Système Intelligent d'Optimisation du ROI Marketing

> Prédiction des ventes à partir des budgets marketing multicanal (TV, Radio, Social Media, Influencer)

---

## Structure du projet

```
data_marketing/
├── api/
│   ├── main.py          
│   └── schemas.py      
├── data/
│   └── marketing_and_sales.csv   
├── models/
│   └── gradient_boosting_pipeline.pkl   
├── notebooks/
│   ├── 01_EDA.ipynb     
│   └── 02_Modeling.ipynb  
├── src/
│   └── app.py           
├── requirements.txt     
└── README.md
```

---

## Installation

### Prérequis

- Python **3.10+**
- pip

### 1. Cloner le dépôt

```bash
git clone https://github.com/pravinwijay/data_marketing.git
cd data_marketing
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```
---

## Lancer le projet

Le projet nécessite de lancer **deux services en parallèle** : l'API et le dashboard.
Ouvre **deux terminaux** distincts.

---

### Terminal 1 — Démarrer l'API FastAPI

```bash
# Depuis la racine du projet
cd api
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

L'API est accessible sur : **http://127.0.0.1:8000**

Documentation interactive Swagger : **http://127.0.0.1:8000/docs**

**Vérifier que l'API fonctionne :**

```bash
curl http://127.0.0.1:8000/health
# Réponse attendue : {"status":"ok"}
```

---

### Terminal 2 — Démarrer le Dashboard Streamlit

```bash
# Depuis la racine du projet
streamlit run src/app.py
```

Le dashboard s'ouvre automatiquement dans ton navigateur sur : **http://localhost:8501**

> ⚠️ **L'API doit être lancée AVANT le dashboard.** Le dashboard appelle l'API pour obtenir les prédictions.

---

## Utilisation de l'API

### `GET /health`

Vérifie que le service est actif.

```bash
curl http://127.0.0.1:8000/health
```

```json
{"status": "ok"}
```

---

### `POST /predict`

Prédit le volume de ventes (en M€) à partir d'une combinaison budgétaire.

**Corps de la requête (JSON) :**

| Champ | Type | Description | Contrainte |
|-------|------|-------------|------------|
| `TV` | float | Budget TV en M€ | ≥ 0 |
| `Radio` | float | Budget Radio en M€ | ≥ 0 |
| `Social_Media` | float | Budget Social Media en M€ | ≥ 0 |
| `Influencer` | string | Type d'influenceur | `Mega`, `Macro`, `Micro` ou `Nano` |

**Exemple de requête :**

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "TV": 150.0,
    "Radio": 25.0,
    "Social_Media": 10.0,
    "Influencer": "Mega"
  }'
```

**Réponse :**

```json
{"predicted_sales_millions": 214.37}
```

**Codes d'erreur :**

| Code | Signification |
|------|--------------|
| `200` | Prédiction retournée avec succès |
| `422` | Données invalides (champ manquant, type incorrect, valeur négative, Influencer inconnu) |
| `400` | Erreur interne lors de la prédiction |

---

## 📓 Notebooks

Les notebooks sont dans le dossier `notebooks/`. Lance Jupyter pour les ouvrir :

```bash
jupyter notebook
# ou
jupyter lab
```

| Notebook | Contenu |
|----------|---------|
| `01_EDA.ipynb` | Audit des données, détection des outliers (boxplots), distributions, corrélations (heatmap), scatterplots budget → Sales, feature engineering |
| `02_Modeling.ipynb` | Préparation (Pipeline sklearn), entraînement de 4 modèles, évaluation (RMSE, MAE, R²), cross-validation, feature importance, sauvegarde du modèle |

---

## Modèles entraînés

Quatre algorithmes ont été comparés sur la tâche de régression (prédiction de `Sales`) :

| Modèle | RMSE (M€) | R² | Notes |
|--------|-----------|-----|-------|
| Régression Linéaire | ~6.43 | 0.9975 | Baseline — très interprétable |
| Random Forest | ~4.12 | 0.9990 | Capture les non-linéarités |
| **Gradient Boosting** | **3.31** | **0.9987** | **✅ Modèle retenu** |
| MLP (Deep Learning) | ~8.20 | 0.9955 | Surapprentissage sur ce dataset |

Le modèle final (Gradient Boosting) est sérialisé dans `models/gradient_boosting_pipeline.pkl`.
Il inclut le pipeline complet : imputation + StandardScaler + OneHotEncoder + modèle.

---

## Dashboard

Le dashboard Streamlit permet à un utilisateur métier de :

- **Simuler un scénario budgétaire** via des sliders (TV, Radio, Social Media) et un sélecteur d'influenceur
- **Obtenir une prédiction de ventes en temps réel** (appel à l'API)
- **Visualiser le ROI estimé** (Sales / budget total)
- **Comparer les performances** des 4 modèles entraînés

---

## Dépendances principales

| Package | Version | Rôle |
|---------|---------|------|
| `scikit-learn` | 1.8.0 | Modèles ML, Pipeline, métriques |
| `pandas` | 3.0.2 | Manipulation des données |
| `numpy` | 2.4.4 | Calcul numérique |
| `fastapi` | 0.136.1 | API REST |
| `uvicorn` | 0.46.0 | Serveur ASGI pour FastAPI |
| `pydantic` | 2.13.4 | Validation des données API |
| `joblib` | 1.5.3 | Sérialisation du modèle |
| `matplotlib` | 3.10.9 | Visualisations |
| `seaborn` | 0.13.2 | Visualisations statistiques |
| `scipy` | 1.17.1 | Tests statistiques (QQ-plot) |
| `streamlit` | — | Dashboard interactif |

---

## Dataset

- **Source :** [Kaggle — Dummy Advertising and Sales Data](https://www.kaggle.com/datasets/harrimansaragih/dummy-advertising-and-sales-data)
- **Fichier :** `data/marketing_and_sales.csv`
- **Taille :** ~4 500 enregistrements, 5 colonnes
- **Variables :** `TV`, `Radio`, `Social Media` (budgets en M€), `Influencer` (catégorielle), `Sales` (cible, en M€)

---

## Points clés du pipeline

```
CSV brut
  → Audit (nulls, doublons, outliers)
  → Train / Test split (80/20)
  → Pipeline sklearn (imputation + scaling + encoding)
  → Entraînement 4 modèles
  → Évaluation (RMSE, MAE, R², Cross-Validation)
  → Sélection Gradient Boosting
  → Sérialisation (joblib)
  → API FastAPI (/predict)
  → Dashboard Streamlit
```

---

## Auteurs

@Behsouu, @Gustave75, @ayoubenn03
