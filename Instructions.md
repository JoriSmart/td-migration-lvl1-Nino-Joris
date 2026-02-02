TD – Migration de données
simple
Migration MySQL vers PostgreSQL
Objectif du TP
Ce TP a pour objectif d'initier à la migration de bases de données SQL d'un système de gestion de
base de données (SGBD) à un autre, en utilisant des outils gratuits.
Le scénario retenu consiste à migrer une base de données depuis MySQL vers PostgreSQL,
deux des SGBD les plus utilisés dans l'écosystème SQL[1][2].
Projet à faire en groupe
Le travail sera réalisé en groupe de 2 à 4 personnes.
Tous les scripts devront être sauvegardés dans un dépôt Git nommé :
td-migration-lvl1-nom-nom-nom
Un journal de bord devra être tenu et sauvegardé dans le dépôt (fichier PDF ou README).
Rendu attendu
Le rendu comprendra :
• Dépôt Git avec l'ensemble des scripts (SQL, Python, Docker, Flyway)
• Journal de bord documentant la progression du travail
• Rapport de migration (optionnel selon le niveau)
• Captures d'écran des étapes clés
Date limite de rendu :
Niveau 1
Outils nécessaires (proposés)
• MySQL : pour la base de données source
• PostgreSQL : pour la base de données cible
• pgAdmin : interface graphique pour la gestion de PostgreSQL
• DBeaver Community Edition : client SQL universel pour la migration[3]
• Faker : bibliothèque Python pour générer des données factices (optionnel pour
peupler la base de données)[4][5]
Étapes du TP
Étape 1 : Installation des outils
1. Installer MySQL : si ce n'est pas déjà fait, télécharger et installer MySQL
2. Installer PostgreSQL et pgAdmin : télécharger et installer PostgreSQL, qui inclut
généralement pgAdmin
3. Installer DBeaver Community Edition : télécharger et installer DBeaver CE à partir de
son site officiel
4. Préparer Python et Faker (optionnel) : si la génération de données factices est
souhaitée, s'assurer que Python est installé et installer la bibliothèque Faker avec pip
install Faker
Étape 2 : Préparation de la base de données source
Création de la base de données MySQL
Utiliser MySQL Workbench ou la ligne de commande pour créer une base de données de test.
Exemple de script SQL MySQL :
CREATE DATABASE ReservationVoyage DEFAULT CHARACTER SET utf8mb4 COLLATE
utf8mb4_unicode_ci;
USE ReservationVoyage;
CREATE TABLE Utilisateurs (
Id INT AUTO_INCREMENT PRIMARY KEY,
Nom VARCHAR(100) NOT NULL,
Prenom VARCHAR(100) NOT NULL,
Email VARCHAR(255) NOT NULL,
MotDePasse VARCHAR(255) NOT NULL
);
Peuplement de la base de données
Completer la BDD (Schema + data) :
● 500 users
● 1000 réservations
Utiliser des scripts SQL ou la bibliothèque Faker pour insérer des données dans la base de
données MySQL.
Exemple de script Python avec Faker[4][5] :
Étape 3 : Migration avec DBeaver
Connexion aux bases de données
1. Ouvrir DBeaver et créer une nouvelle connexion à la base de données MySQL
2. Créer ensuite une nouvelle connexion à la base de données PostgreSQL
Démarrage de la migration
1. Clic droit sur la base de données source MySQL dans DBeaver, puis choisir Tools >
Migrate Database
2. Sélectionner la base de données cible PostgreSQL lorsque demandé
3. Choisir les objets (tables, schémas, données) à migrer
4. Laisser DBeaver générer le script SQL pour la migration et l'exécuter
Étape 4 : Vérification
Vérification des données migrées
1. Utiliser pgAdmin pour se connecter à la base de données PostgreSQL
2. Vérifier que toutes les tables et données attendues ont bien été migrées
Niveau 2
Objectif du TP
Migrer une base de données existante de MySQL vers PostgreSQL à l'aide de Docker pour
héberger les bases de données et Flyway pour gérer les scripts de migration[6][7].
Outils nécessaires (proposés)
• Docker
• Flyway[6][7]
Étapes du TP
Étape 1 : Configuration initiale
Lancement des instances avec Docker
Exemple de fichier docker-compose.yml minimal :
version: '3.8'
services:
mysql:
image: mysql:8
container_name: mysql-reservation
environment:
MYSQL_ROOT_PASSWORD: root
MYSQL_DATABASE: ReservationVoyage
ports:
- "3306:3306"
volumes:
- ./mysql-data:/var/lib/mysql
postgres:
image: postgres:16
container_name: postgres-reservation
environment:
POSTGRES_USER: postgres
POSTGRES_PASSWORD: postgres
POSTGRES_DB: reservation_voyage
ports:
- "5432:5432"
volumes:
- ./pg-data:/var/lib/postgresql/data
Lancement des services :
docker compose up -d
Étape 2 : Préparation de la base de données MySQL
Création de la base de données et insertion de données
Se connecter à l'instance MySQL et créer une base de données de test avec insertion de quelques
données.
Étape 3 : Configuration de Flyway pour la migration
Création de l'environnement Flyway
Sur le système hôte, créer un dossier pour le projet Flyway, par exemple flyway_migration.
Dans ce dossier, créer deux sous-dossiers :
• sql pour les scripts de migration
• conf pour le fichier de configuration
Configuration de Flyway
Dans le sous-dossier conf, créer un fichier nommé flyway.conf avec le contenu suivant :
flyway.url=jdbc:postgresql://localhost:5432/reservation_voyage
flyway.user=postgres
flyway.password=postgres
flyway.schemas=public
flyway.locations=filesystem:sql
Préparation des scripts de migration
Dans le sous-dossier sql, créer un fichier nommé V1__Create_table.sql contenant les
commandes SQL pour recréer la structure de la base de données MySQL dans PostgreSQL.
Exemple :
CREATE TABLE utilisateurs (
id SERIAL PRIMARY KEY,
nom VARCHAR(100) NOT NULL,
prenom VARCHAR(100) NOT NULL,
email VARCHAR(255) NOT NULL UNIQUE,
mot_de_passe VARCHAR(255) NOT NULL,
date_creation TIMESTAMP NOT NULL DEFAULT NOW()
);
Ajouter un deuxième script, V2__Insert_data.sql, pour insérer des données dans PostgreSQL.
Utiliser des INSERTS ou un autre mécanisme pour copier les données de MySQL.
Exemple :
INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe)
VALUES ('Dupont', 'Alice', 'alice.dupont@example.com', 'motdepasse123');
Étape 4 : Lancement de la migration avec Flyway
Exécution de Flyway
Ouvrir un terminal et naviguer vers le dossier flyway_migration.
Lancer la migration en exécutant Flyway avec Docker :
docker run --rm
-v $(pwd)/sql:/flyway/sql
-v $(pwd)/conf:/flyway/conf
flyway/flyway
-configFiles=/flyway/conf/flyway.conf migrate
Étape 5 : Vérification de la migration
Vérification dans PostgreSQL
Se connecter à PostgreSQL pour vérifier que les données ont été migrées.
Utiliser les commandes SQL pour vérifier les données :
SELECT COUNT(*) FROM utilisateurs;
Niveau 3
Objectif du TP
Intégrer des tests durant la migration[8].
Étapes du TP
Étape 1 : Créer des scripts de test
Dans le dossier flyway_migration/sql, ajouter des scripts SQL qui seront exécutés après la
migration pour tester la base de données.
V3__Test_integrite.sql
Ce script peut contenir des assertions SQL vérifiant l'intégrité des relations entre les tables,
comme des vérifications de clés étrangères ou l'absence de valeurs nulles où elles ne sont pas
autorisées.
Exemple :
-- V3__Test_integrite.sql
-- Tests d'intégrité de la base migrée
-- Vérification de l'absence de valeurs NULL dans les colonnes critiques
SELECT COUNT(*) AS nb_nom_null
FROM utilisateurs
WHERE nom IS NULL;
SELECT COUNT(*) AS nb_email_null
FROM utilisateurs
WHERE email IS NULL;
V4__Test_completude.sql
Ce script pourrait compter le nombre d'enregistrements dans certaines tables clés et le comparer
à des valeurs attendues pour s'assurer que toutes les données nécessaires ont été migrées.
Exemple :
-- V4__Test_completude.sql
-- Tests de complétude (volumétrie globale)
-- Nombre d'utilisateurs après migration
SELECT COUNT(*) AS nb_utilisateurs_pg
FROM utilisateurs;
Étape 2 : Exécuter Flyway
Automatisation des tests avec un script Shell
Exemple de script Shell pour automatiser l'exécution :
Références
[1] Bytebase. (2024). How to Migrate database from MySQL to PostgreSQL.
https://www.bytebase.com/reference/migration/how-to-migrate-database-from-mysql-to-postg
res/
[2] Streams DBConvert. (2025). MySQL ↔ PostgreSQL Schema Conversion: The Real-World
Guide. https://streams.dbconvert.com/blog/mysql-postgresql-schema-conversion/
[3] Dev.to. (2025). Migrating from MySQL to PostgreSQL Key Query Differences and
Considerations.
https://dev.to/msnmongare/migrating-from-mysql-to-postgresql-key-query-differences-and-co
nsiderations-3831
[4] Red Gate. (2023). Getting Started with Flyway Migrations on PostgreSQL.
https://www.red-gate.com/hub/product-learning/flyway/getting-started-with-flyway-migration
s-on-postgresql
[5] PingCAP. (2024). Mastering Flyway for Seamless Database Schema Migrations.
https://www.pingcap.com/article/mastering-flyway-seamless-database-schema-migrations/
[6] DBeaver Documentation. (2026). Data migration.
https://dbeaver.com/docs/dbeaver/Data-migration/
[7] Liquid Web. (2025). DBeaver Tutorial for PostgreSQL, SQLite, MySQL, and MariaDB.
https://www.liquidweb.com/help-docs/server-administration/database-management/dbeaver-t
utorial/
[8] BuildDevOps. (2025). How to Generate Dummy Data in MySQL Using the Python Faker
Module.
https://www.builddevops.com/post/how-to-generate-dummy-data-in-mysql-using-the-python-f
aker-module
[9] Percona. (2022). How to Generate Test Data for MySQL With Python.
https://www.percona.com/blog/how-to-generate-test-data-for-mysql-with-python/
[10] Dev.to. (2025). Moving data from mysql to postgresql.
https://dev.to/reinny_kimutai_4b1a5c2da8/moving-data-from-mysql-to-postgresql-n75