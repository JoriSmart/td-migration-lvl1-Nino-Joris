-- ==============================================
-- TD Migration Niveau 1 - Scripts de vérification
-- À exécuter dans PostgreSQL après la migration
-- ==============================================

-- ==============================================
-- 1. Vérification de la structure des tables
-- ==============================================
\echo '=== VÉRIFICATION DE LA STRUCTURE ==='

-- Liste des tables migrées
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- ==============================================
-- 2. Vérification du nombre d'enregistrements
-- ==============================================
\echo '=== COMPTAGE DES ENREGISTREMENTS ==='

SELECT 'Utilisateurs' AS table_name, COUNT(*) AS nombre FROM utilisateurs
UNION ALL
SELECT 'Destinations', COUNT(*) FROM destinations
UNION ALL
SELECT 'Reservations', COUNT(*) FROM reservations;

-- Vérifications attendues:
-- Utilisateurs: 500
-- Destinations: 20
-- Reservations: 1000

-- ==============================================
-- 3. Vérification de l'intégrité des données
-- ==============================================
\echo '=== TESTS D INTÉGRITÉ ==='

-- Vérifier qu'il n'y a pas de valeurs NULL dans les colonnes critiques
SELECT 'Utilisateurs avec nom NULL' AS test, COUNT(*) AS erreurs
FROM utilisateurs WHERE nom IS NULL
UNION ALL
SELECT 'Utilisateurs avec email NULL', COUNT(*)
FROM utilisateurs WHERE email IS NULL
UNION ALL
SELECT 'Réservations sans utilisateur valide', COUNT(*)
FROM reservations r
LEFT JOIN utilisateurs u ON r.utilisateurid = u.id
WHERE u.id IS NULL
UNION ALL
SELECT 'Réservations sans destination valide', COUNT(*)
FROM reservations r
LEFT JOIN destinations d ON r.destinationid = d.id
WHERE d.id IS NULL;

-- ==============================================
-- 4. Échantillon de données
-- ==============================================
\echo '=== ÉCHANTILLON DE DONNÉES ==='

-- Premiers utilisateurs
SELECT id, nom, prenom, email 
FROM utilisateurs 
LIMIT 5;

-- Premières réservations avec détails
SELECT 
    r.id,
    u.nom || ' ' || u.prenom AS client,
    d.ville || ', ' || d.pays AS destination,
    r.datedepart,
    r.dateretour,
    r.prixtotal,
    r.statut
FROM reservations r
JOIN utilisateurs u ON r.utilisateurid = u.id
JOIN destinations d ON r.destinationid = d.id
LIMIT 5;

-- ==============================================
-- 5. Statistiques sur les réservations
-- ==============================================
\echo '=== STATISTIQUES ==='

-- Répartition par statut
SELECT statut, COUNT(*) AS nombre
FROM reservations
GROUP BY statut
ORDER BY nombre DESC;

-- Top 5 destinations
SELECT d.ville, d.pays, COUNT(*) AS nb_reservations
FROM reservations r
JOIN destinations d ON r.destinationid = d.id
GROUP BY d.ville, d.pays
ORDER BY nb_reservations DESC
LIMIT 5;
