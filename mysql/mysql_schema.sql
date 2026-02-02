-- ==============================================
-- TD Migration Niveau 1 - Schéma MySQL
-- Base de données ReservationVoyage
-- ==============================================

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS ReservationVoyage 
    DEFAULT CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE ReservationVoyage;

-- ==============================================
-- Table Utilisateurs
-- ==============================================
CREATE TABLE Utilisateurs (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Prenom VARCHAR(100) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    MotDePasse VARCHAR(255) NOT NULL,
    Telephone VARCHAR(20),
    DateCreation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ==============================================
-- Table Destinations
-- ==============================================
CREATE TABLE Destinations (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Ville VARCHAR(100) NOT NULL,
    Pays VARCHAR(100) NOT NULL,
    Description TEXT,
    PrixMoyenParJour DECIMAL(10, 2) NOT NULL DEFAULT 100.00
) ENGINE=InnoDB;

-- ==============================================
-- Table Reservations
-- ==============================================
CREATE TABLE Reservations (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    UtilisateurId INT NOT NULL,
    DestinationId INT NOT NULL,
    DateReservation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    DateDepart DATE NOT NULL,
    DateRetour DATE NOT NULL,
    NombrePersonnes INT NOT NULL DEFAULT 1,
    PrixTotal DECIMAL(10, 2) NOT NULL,
    Statut ENUM('En attente', 'Confirmée', 'Annulée', 'Terminée') NOT NULL DEFAULT 'En attente',
    Commentaires TEXT,
    FOREIGN KEY (UtilisateurId) REFERENCES Utilisateurs(Id) ON DELETE CASCADE,
    FOREIGN KEY (DestinationId) REFERENCES Destinations(Id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ==============================================
-- Index pour améliorer les performances
-- ==============================================
CREATE INDEX idx_reservations_utilisateur ON Reservations(UtilisateurId);
CREATE INDEX idx_reservations_destination ON Reservations(DestinationId);
CREATE INDEX idx_reservations_dates ON Reservations(DateDepart, DateRetour);
CREATE INDEX idx_utilisateurs_email ON Utilisateurs(Email);
