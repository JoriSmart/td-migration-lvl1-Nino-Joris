"""
TD Migration Niveau 1 - Génération de données avec Faker
Génère 500 utilisateurs et 1000 réservations dans MySQL
"""

import mysql.connector
from faker import Faker
import random
from datetime import timedelta
import hashlib

# Configuration de la connexion MySQL (Authentification Windows)
DB_CONFIG = {
    'host': 'localhost',
    'user': '',  # Laisser vide pour l'authentification Windows
    'password': '',  # Laisser vide pour l'authentification Windows
    'database': 'ReservationVoyage',
    'auth_plugin': 'authentication_windows_client'
}

# Liste de destinations populaires
DESTINATIONS = [
    ('Paris', 'France', 'La ville lumière, capitale de la France'),
    ('Rome', 'Italie', 'La ville éternelle avec son histoire millénaire'),
    ('Barcelone', 'Espagne', 'Ville cosmopolite au bord de la Méditerranée'),
    ('Amsterdam', 'Pays-Bas', 'Ville des canaux et des musées'),
    ('Londres', 'Royaume-Uni', 'Capitale historique et moderne'),
    ('Berlin', 'Allemagne', 'Ville dynamique au cœur de l\'Europe'),
    ('Lisbonne', 'Portugal', 'Ville aux sept collines'),
    ('Vienne', 'Autriche', 'Capitale de la musique classique'),
    ('Prague', 'République Tchèque', 'La ville aux cent clochers'),
    ('Dublin', 'Irlande', 'Ville chaleureuse et accueillante'),
    ('Athènes', 'Grèce', 'Berceau de la civilisation occidentale'),
    ('Stockholm', 'Suède', 'Venise du Nord'),
    ('Copenhague', 'Danemark', 'Ville du design et du hygge'),
    ('Bruxelles', 'Belgique', 'Capitale de l\'Europe'),
    ('Zurich', 'Suisse', 'Ville au bord du lac'),
    ('New York', 'États-Unis', 'La ville qui ne dort jamais'),
    ('Tokyo', 'Japon', 'Métropole futuriste et traditionnelle'),
    ('Sydney', 'Australie', 'Ville emblématique d\'Océanie'),
    ('Marrakech', 'Maroc', 'Perle du Sud marocain'),
    ('Le Caire', 'Égypte', 'Porte vers les pyramides')
]

def hash_password(password: str) -> str:
    """Hash un mot de passe avec SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_users(cursor, fake: Faker, count: int = 500):
    """Génère et insère des utilisateurs dans la base de données"""
    print(f"Génération de {count} utilisateurs...")
    
    users = []
    emails_used = set()
    
    for i in range(count):
        # Générer un email unique
        while True:
            email = fake.email()
            if email not in emails_used:
                emails_used.add(email)
                break
        
        user = (
            fake.last_name(),
            fake.first_name(),
            email,
            hash_password(fake.password(length=12)),
            fake.phone_number()[:20],
            fake.date_time_between(start_date='-2y', end_date='now')
        )
        users.append(user)
        
        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{count} utilisateurs générés")
    
    query = """
        INSERT INTO Utilisateurs (Nom, Prenom, Email, MotDePasse, Telephone, DateCreation)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(query, users)
    print(f"✓ {count} utilisateurs insérés avec succès")

def generate_destinations(cursor):
    """Insère les destinations dans la base de données"""
    print("Insertion des destinations...")
    
    destinations = []
    for ville, pays, description in DESTINATIONS:
        prix = round(random.uniform(50, 300), 2)
        destinations.append((ville, pays, description, prix))
    
    query = """
        INSERT INTO Destinations (Ville, Pays, Description, PrixMoyenParJour)
        VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(query, destinations)
    print(f"✓ {len(DESTINATIONS)} destinations insérées avec succès")

def generate_reservations(cursor, fake: Faker, count: int = 1000):
    """Génère et insère des réservations dans la base de données"""
    print(f"Génération de {count} réservations...")
    
    # Récupérer les IDs des utilisateurs et destinations
    cursor.execute("SELECT Id FROM Utilisateurs")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT Id, PrixMoyenParJour FROM Destinations")
    destinations = [(row[0], float(row[1])) for row in cursor.fetchall()]
    
    statuts = ['En attente', 'Confirmée', 'Annulée', 'Terminée']
    reservations = []
    
    for i in range(count):
        user_id = random.choice(user_ids)
        dest_id, prix_jour = random.choice(destinations)
        
        date_depart = fake.date_between(start_date='-1y', end_date='+6M')
        duree = random.randint(2, 14)
        date_retour = date_depart + timedelta(days=duree)
        
        nb_personnes = random.randint(1, 5)
        prix_total = round(prix_jour * duree * nb_personnes, 2)
        
        # Statut basé sur les dates
        if date_depart > fake.date_object():
            statut = random.choice(['En attente', 'Confirmée', 'Annulée'])
        else:
            statut = random.choice(['Terminée', 'Annulée'])
        
        commentaire = fake.sentence() if random.random() > 0.7 else None
        
        reservation = (
            user_id,
            dest_id,
            fake.date_time_between(start_date='-1y', end_date='now'),
            date_depart,
            date_retour,
            nb_personnes,
            prix_total,
            statut,
            commentaire
        )
        reservations.append(reservation)
        
        if (i + 1) % 200 == 0:
            print(f"  {i + 1}/{count} réservations générées")
    
    query = """
        INSERT INTO Reservations 
        (UtilisateurId, DestinationId, DateReservation, DateDepart, DateRetour, 
         NombrePersonnes, PrixTotal, Statut, Commentaires)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(query, reservations)
    print(f"✓ {count} réservations insérées avec succès")

def main():
    """Fonction principale"""
    print("=" * 50)
    print("TD Migration - Génération de données")
    print("=" * 50)
    
    # Initialiser Faker avec locale français
    fake = Faker('fr_FR')
    Faker.seed(42)  # Pour reproductibilité
    random.seed(42)
    
    try:
        # Connexion à MySQL
        print("\nConnexion à MySQL...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✓ Connecté à MySQL")
        
        # Génération des données
        print("\n" + "-" * 50)
        generate_destinations(cursor)
        conn.commit()
        
        print("\n" + "-" * 50)
        generate_users(cursor, fake, 500)
        conn.commit()
        
        print("\n" + "-" * 50)
        generate_reservations(cursor, fake, 1000)
        conn.commit()
        
        # Afficher les statistiques
        print("\n" + "=" * 50)
        print("RÉSUMÉ")
        print("=" * 50)
        
        cursor.execute("SELECT COUNT(*) FROM Utilisateurs")
        print(f"Utilisateurs: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Destinations")
        print(f"Destinations: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Reservations")
        print(f"Réservations: {cursor.fetchone()[0]}")
        
        print("\n✓ Génération terminée avec succès!")
        
    except mysql.connector.Error as err:
        print(f"\n✗ Erreur MySQL: {err}")
        print("\nAssurez-vous que:")
        print("  1. MySQL est en cours d'exécution")
        print("  2. La base de données 'ReservationVoyage' existe")
        print("  3. Les identifiants dans DB_CONFIG sont corrects")
        raise
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
