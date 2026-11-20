# GestLotissement

Application web de gestion et d'analyse des lotissements, développée en binôme lors d'un stage à la **Municipalité de Kelaa des Sraghna** pour digitaliser un processus 100% papier.

---

## Aperçu

GestLotissement permet d'importer des fichiers de données de lotissements (CSV / Excel), de les normaliser automatiquement, et d'afficher des statistiques interactives par étage et par vocation.

**Avant** : gestion manuelle sur papier, saisie répétitive, aucune vue d'ensemble.  
**Après** : import en un clic, tableau de bord dynamique, détection automatique des incohérences.

---

## Fonctionnalités

- Import de fichiers CSV, XLS et XLSX
- Détection intelligente des colonnes (s'adapte aux différents formats sans configuration)
- Normalisation automatique des étages (ex: "2ème étage", "r+2" → `R+2`)
- Normalisation automatique des vocations (ex: "eco", "habitation" → `Economique`)
- Tableau de bord avec comptage par étage et par vocation
- Détection et alerte automatique des incohérences dans les données

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Python / Flask |
| Base de données | MySQL |
| Traitement données | Pandas |
| Frontend | HTML / CSS / JavaScript |
| Versioning | Git / GitHub |

---

## Structure du projet
```
gest_lotissements/
│
├── app.py                  # Application principale Flask + routes
├── config.py               # Configuration base de données MySQL
├── database.sql            # Schéma SQL
├── requirements.txt        # Dépendances Python
│
├── static/
│   ├── style.css
│   └── app.js
│
├── templates/
│   ├── layout.html
│   ├── home.html
│   ├── import.html
│   ├── lots.html
│   └── help.html
│
└── uploads/                # Fichiers importés (ignoré par Git)
```

---

## Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/Samah-boudallaa/GestLotissement.git
cd GestLotissement
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configurer la base de données
```bash
mysql -u root -p < database.sql
```

Puis renseigner vos identifiants dans `config.py` :
```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'votre_mot_de_passe',
    'database': 'gest_lotissements'
}
```

### 4. Lancer l'application
```bash
python app.py
```

Accessible sur : [http://localhost:5000](http://localhost:5000)

---

## Utilisation

1. Aller sur la page **Importer**
2. Charger un fichier CSV ou Excel avec les colonnes : `nom`, `étage`, `vocation`
3. Les données sont normalisées et affichées automatiquement
4. Les statistiques se mettent à jour en temps réel
5. Une alerte s'affiche en cas d'incohérence détectée

### Format de fichier attendu

| nom | etages | vocation |
|-----|--------|----------|
| Lotissement Al Fath | R+2 | Economique |
| Résidence Sraghna | R+3 | Villa |

> Les noms de colonnes sont détectés automatiquement, plusieurs variantes acceptées.

---

## Auteures

Projet réalisé en binôme par deux étudiantes en Ingénierie des Données de l'EST Kelaa des Sraghna.

| | |
|---|---|
| **Samah Boudallaa** | [github.com/Samah-boudallaa](https://github.com/Samah-boudallaa) · s.boudallaa2659@uca.ac.ma |
| **Khadija Rizqy** | [github.com/khadija-rizqy](https://github.com/khadija-rizqy) · k.rizqy1110@uca.ac.ma |

---

## Contexte

Projet développé lors d'un stage de 2 mois (juillet-août 2025) à la Municipalité de Kelaa des Sraghna dans le cadre de la digitalisation des services internes.
