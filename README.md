# TD Migration MySQL → PostgreSQL (Niveau 1)

## Groupe
- **Nino**
- **Joris**

## Journal de Bord

### Date: 02/02/2026

#### Travail réalisé
- Création du schéma de base de données MySQL
- Développement du script Python de génération de données
- Préparation des scripts de vérification

---

## Structure du Projet

```
td-migration-lvl1-Nino-Joris/
├── mysql/
│   └── mysql_schema.sql      # Schéma de la BDD MySQL
├── scripts/
│   ├── generate_data.py      # Génération de données avec Faker
│   └── requirements.txt      # Dépendances Python
├── verification/
│   └── verification.sql      # Scripts de vérification PostgreSQL
├── captures/                 # Screenshots (à ajouter)
├── README.md                 # Ce fichier
└── Instructions.md           # Consignes du TP
```

---

## Étapes de Migration

### Étape 1: Prérequis

1. **MySQL** installé et en cours d'exécution
2. **PostgreSQL** installé avec **pgAdmin**
3. **DBeaver Community Edition** installé
4. **Python 3.x** avec pip

### Étape 2: Création de la base MySQL

```bash
# Connexion à MySQL
mysql -u root -p

# Exécuter le script de création
source mysql/mysql_schema.sql
```

### Étape 3: Génération des données

```bash
# Installer les dépendances
cd scripts
pip install -r requirements.txt

# Générer les données
python generate_data.py
```

**Résultat attendu:**
- 500 utilisateurs
- 20 destinations
- 1000 réservations

### Étape 4: Migration avec DBeaver

1. Ouvrir **DBeaver**
2. Créer une connexion à MySQL (`localhost:3306`, base `ReservationVoyage`)
3. Créer une connexion à PostgreSQL (`localhost:5432`)
4. Dans PostgreSQL, créer une base de données `reservation_voyage`
5. Clic droit sur la base MySQL → **Tools** → **Migrate Database**
6. Sélectionner PostgreSQL comme cible
7. Choisir toutes les tables (Utilisateurs, Destinations, Reservations)
8. Exécuter la migration

### Étape 5: Vérification

```bash
# Dans pgAdmin ou psql, exécuter:
\i verification/verification.sql
```

**Vérifications:**
- [x] 500 utilisateurs migrés
- [x] 20 destinations migrées  
- [x] 1000 réservations migrées
- [x] Intégrité des clés étrangères préservée

---

## Captures d'écran

> À ajouter dans le dossier `captures/`:
> - Schéma MySQL créé
> - Données générées
> - Interface de migration DBeaver
> - Résultat de la vérification dans pgAdmin

---

## Notes Techniques

### Différences MySQL → PostgreSQL

| MySQL | PostgreSQL |
|-------|------------|
| `AUTO_INCREMENT` | `SERIAL` |
| `DATETIME` | `TIMESTAMP` |
| `ENUM(...)` | `VARCHAR` avec CHECK ou type ENUM |
| `ENGINE=InnoDB` | Non nécessaire |

### Problèmes rencontrés et solutions

*À documenter pendant le TP*

---

## Références

- [Documentation Faker Python](https://faker.readthedocs.io/)
- [DBeaver Data Migration](https://dbeaver.com/docs/dbeaver/Data-migration/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)