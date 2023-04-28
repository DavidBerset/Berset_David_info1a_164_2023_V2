-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: Berset_David_info1a_164_2023

-- Destruction de la BD si elle existe.
-- Pour être certain d'avoir la dernière version des données

DROP DATABASE IF EXISTS Berset_David_info1a_164_2023;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS Berset_David_info1a_164_2023;

-- Utilisation de cette base de donnée

USE Berset_David_info1a_164_2023;
-- --------------------------------------------------------
-- --------------------------------------------------------
-- Hôte :                        localhost
-- Version du serveur:           5.1.72-community - MySQL Community Server (GPL)
-- SE du serveur:                Win32
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Export de la structure de la base pour berset_david_info1a_164_2023
DROP DATABASE IF EXISTS `berset_david_info1a_164_2023`;
CREATE DATABASE IF NOT EXISTS `berset_david_info1a_164_2023` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `berset_david_info1a_164_2023`;

-- Export de la structure de la table berset_david_info1a_164_2023. t_adresse
DROP TABLE IF EXISTS `t_adresse`;
CREATE TABLE IF NOT EXISTS `t_adresse` (
  `id_adresse` int(11) NOT NULL AUTO_INCREMENT,
  `nom_rue_adresse` varchar(50) DEFAULT NULL,
  `ville_adresse` varchar(50) DEFAULT NULL,
  `npa_adresse` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_adresse`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_adresse : ~4 rows (environ)
/*!40000 ALTER TABLE `t_adresse` DISABLE KEYS */;
INSERT INTO `t_adresse` (`id_adresse`, `nom_rue_adresse`, `ville_adresse`, `npa_adresse`) VALUES
	(1, 'chemin de la Buchile 48', 'Villarsiviriaux', 1694),
	(2, 'Route de Bocheferra 3', 'Romont', 1680),
	(3, 'Rte du Tir Fédéral 18', 'Givisiez', 1762),
	(4, 'Route de l\'ancienne ferme 2', 'Romont', 1694);
/*!40000 ALTER TABLE `t_adresse` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_adresse_etre_fournisseur
DROP TABLE IF EXISTS `t_adresse_etre_fournisseur`;
CREATE TABLE IF NOT EXISTS `t_adresse_etre_fournisseur` (
  `id_adresse_etre_fournisseur` int(11) NOT NULL AUTO_INCREMENT,
  `fk_adresse` int(11) DEFAULT NULL,
  `fk_fournisseur` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_adresse_etre_fournisseur`),
  KEY `FK_t_adresse_etre_fournisseur_t_adresse` (`fk_adresse`),
  KEY `FK_t_adresse_etre_fournisseur_t_fournisseur` (`fk_fournisseur`),
  CONSTRAINT `FK_t_adresse_etre_fournisseur_t_adresse` FOREIGN KEY (`fk_adresse`) REFERENCES `t_adresse` (`id_adresse`),
  CONSTRAINT `FK_t_adresse_etre_fournisseur_t_fournisseur` FOREIGN KEY (`fk_fournisseur`) REFERENCES `t_fournisseur` (`id_fournisseur`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_adresse_etre_fournisseur : ~3 rows (environ)
/*!40000 ALTER TABLE `t_adresse_etre_fournisseur` DISABLE KEYS */;
INSERT INTO `t_adresse_etre_fournisseur` (`id_adresse_etre_fournisseur`, `fk_adresse`, `fk_fournisseur`) VALUES
	(1, 2, 1),
	(2, 3, 2),
	(3, 4, 3);
/*!40000 ALTER TABLE `t_adresse_etre_fournisseur` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_boisson
DROP TABLE IF EXISTS `t_boisson`;
CREATE TABLE IF NOT EXISTS `t_boisson` (
  `id_boisson` int(11) NOT NULL AUTO_INCREMENT,
  `nom_boisson` varchar(50) DEFAULT NULL,
  `type_boisson` varchar(50) DEFAULT NULL,
  `prix_vente_boisson` float DEFAULT NULL,
  `code_barre_boisson` text,
  `cover_link_boisson` text,
  PRIMARY KEY (`id_boisson`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_boisson : ~1 rows (environ)
/*!40000 ALTER TABLE `t_boisson` DISABLE KEYS */;
INSERT INTO `t_boisson` (`id_boisson`, `nom_boisson`, `type_boisson`, `prix_vente_boisson`, `code_barre_boisson`, `cover_link_boisson`) VALUES
	(1, 'Super bock', 'Bière', 4, NULL, NULL);
/*!40000 ALTER TABLE `t_boisson` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_boisson_acheter_fournisseur
DROP TABLE IF EXISTS `t_boisson_acheter_fournisseur`;
CREATE TABLE IF NOT EXISTS `t_boisson_acheter_fournisseur` (
  `id_boisson_acheter_fournisseur` int(11) NOT NULL AUTO_INCREMENT,
  `fk_boisson` int(11) DEFAULT NULL,
  `fk_fournisseur` int(11) DEFAULT NULL,
  `date_acheter` date DEFAULT NULL,
  `prix_acheter` float DEFAULT NULL,
  `nombre_boisson_acheter` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_boisson_acheter_fournisseur`),
  KEY `FK_t_boisson_acheter_fournisseur_t_boisson` (`fk_boisson`),
  KEY `FK_t_boisson_acheter_fournisseur_t_fournisseur` (`fk_fournisseur`),
  CONSTRAINT `FK_t_boisson_acheter_fournisseur_t_fournisseur` FOREIGN KEY (`fk_fournisseur`) REFERENCES `t_fournisseur` (`id_fournisseur`),
  CONSTRAINT `FK_t_boisson_acheter_fournisseur_t_boisson` FOREIGN KEY (`fk_boisson`) REFERENCES `t_boisson` (`id_boisson`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_boisson_acheter_fournisseur : ~1 rows (environ)
/*!40000 ALTER TABLE `t_boisson_acheter_fournisseur` DISABLE KEYS */;
INSERT INTO `t_boisson_acheter_fournisseur` (`id_boisson_acheter_fournisseur`, `fk_boisson`, `fk_fournisseur`, `date_acheter`, `prix_acheter`, `nombre_boisson_acheter`) VALUES
	(1, 1, 2, '2023-04-04', 10, 12);
/*!40000 ALTER TABLE `t_boisson_acheter_fournisseur` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_boisson_commander_fournisseur
DROP TABLE IF EXISTS `t_boisson_commander_fournisseur`;
CREATE TABLE IF NOT EXISTS `t_boisson_commander_fournisseur` (
  `id_boisson_commander_fournisseur` int(11) NOT NULL AUTO_INCREMENT,
  `fk_boisson` int(11) DEFAULT NULL,
  `fk_fournisseur` int(11) DEFAULT NULL,
  `date_commande` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `prix_achat_commander` float DEFAULT NULL,
  `nombre_boisson_commander` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_boisson_commander_fournisseur`),
  KEY `FK_t_boisson_commander_fournisseur_t_boisson` (`fk_boisson`),
  KEY `FK_t_boisson_commander_fournisseur_t_fournisseur` (`fk_fournisseur`),
  CONSTRAINT `FK_t_boisson_commander_fournisseur_t_boisson` FOREIGN KEY (`fk_boisson`) REFERENCES `t_boisson` (`id_boisson`),
  CONSTRAINT `FK_t_boisson_commander_fournisseur_t_fournisseur` FOREIGN KEY (`fk_fournisseur`) REFERENCES `t_fournisseur` (`id_fournisseur`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_boisson_commander_fournisseur : ~1 rows (environ)
/*!40000 ALTER TABLE `t_boisson_commander_fournisseur` DISABLE KEYS */;
INSERT INTO `t_boisson_commander_fournisseur` (`id_boisson_commander_fournisseur`, `fk_boisson`, `fk_fournisseur`, `date_commande`, `prix_achat_commander`, `nombre_boisson_commander`) VALUES
	(1, 1, 1, '2023-03-15 10:13:07', 10, 6);
/*!40000 ALTER TABLE `t_boisson_commander_fournisseur` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_boisson_livrer_fournisseur
DROP TABLE IF EXISTS `t_boisson_livrer_fournisseur`;
CREATE TABLE IF NOT EXISTS `t_boisson_livrer_fournisseur` (
  `id_boisson_livrer_fournisseur` int(11) NOT NULL AUTO_INCREMENT,
  `fk_boisson` int(11) DEFAULT NULL,
  `fk_fournisseur` int(11) DEFAULT NULL,
  `date_livrer` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `nombre_boisson_livrer` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_boisson_livrer_fournisseur`),
  KEY `FK_t_boisson_livrer_fournisseur_t_boisson` (`fk_boisson`),
  KEY `FK_t_boisson_livrer_fournisseur_t_fournisseur` (`fk_fournisseur`),
  CONSTRAINT `FK_t_boisson_livrer_fournisseur_t_boisson` FOREIGN KEY (`fk_boisson`) REFERENCES `t_boisson` (`id_boisson`),
  CONSTRAINT `FK_t_boisson_livrer_fournisseur_t_fournisseur` FOREIGN KEY (`fk_fournisseur`) REFERENCES `t_fournisseur` (`id_fournisseur`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_boisson_livrer_fournisseur : ~1 rows (environ)
/*!40000 ALTER TABLE `t_boisson_livrer_fournisseur` DISABLE KEYS */;
INSERT INTO `t_boisson_livrer_fournisseur` (`id_boisson_livrer_fournisseur`, `fk_boisson`, `fk_fournisseur`, `date_livrer`, `nombre_boisson_livrer`) VALUES
	(1, 1, 1, '2023-03-15 10:13:32', 6);
/*!40000 ALTER TABLE `t_boisson_livrer_fournisseur` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_boisson_retourner_fournisseur
DROP TABLE IF EXISTS `t_boisson_retourner_fournisseur`;
CREATE TABLE IF NOT EXISTS `t_boisson_retourner_fournisseur` (
  `id_boisson_retourner_fournisseur` int(11) NOT NULL AUTO_INCREMENT,
  `fk_boisson` int(11) DEFAULT NULL,
  `fk_fournisseur` int(11) DEFAULT NULL,
  `date_retourner` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `prix_achat_retourner` float DEFAULT NULL,
  `nombre_boisson_retourner` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_boisson_retourner_fournisseur`),
  KEY `FK_t_boisson_retourner_fournisseur_t_boisson` (`fk_boisson`),
  KEY `FK_t_boisson_retourner_fournisseur_t_fournisseur` (`fk_fournisseur`),
  CONSTRAINT `FK_t_boisson_retourner_fournisseur_t_boisson` FOREIGN KEY (`fk_boisson`) REFERENCES `t_boisson` (`id_boisson`),
  CONSTRAINT `FK_t_boisson_retourner_fournisseur_t_fournisseur` FOREIGN KEY (`fk_fournisseur`) REFERENCES `t_fournisseur` (`id_fournisseur`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_boisson_retourner_fournisseur : ~1 rows (environ)
/*!40000 ALTER TABLE `t_boisson_retourner_fournisseur` DISABLE KEYS */;
INSERT INTO `t_boisson_retourner_fournisseur` (`id_boisson_retourner_fournisseur`, `fk_boisson`, `fk_fournisseur`, `date_retourner`, `prix_achat_retourner`, `nombre_boisson_retourner`) VALUES
	(1, 1, 1, '2023-03-15 10:13:56', 1, 6);
/*!40000 ALTER TABLE `t_boisson_retourner_fournisseur` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_boisson_stocker_contenance
DROP TABLE IF EXISTS `t_boisson_stocker_contenance`;
CREATE TABLE IF NOT EXISTS `t_boisson_stocker_contenance` (
  `id_boisson_stocker_contenance` int(11) NOT NULL AUTO_INCREMENT,
  `fk_boisson` int(11) DEFAULT NULL,
  `fk_contenance` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_boisson_stocker_contenance`),
  KEY `FK_t_boisson_stocker_contenance_t_boisson` (`fk_boisson`),
  KEY `FK_t_boisson_stocker_contenance_t_contenance` (`fk_contenance`),
  CONSTRAINT `FK_t_boisson_stocker_contenance_t_boisson` FOREIGN KEY (`fk_boisson`) REFERENCES `t_boisson` (`id_boisson`),
  CONSTRAINT `FK_t_boisson_stocker_contenance_t_contenance` FOREIGN KEY (`fk_contenance`) REFERENCES `t_contenance` (`id_contenance`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_boisson_stocker_contenance : ~1 rows (environ)
/*!40000 ALTER TABLE `t_boisson_stocker_contenance` DISABLE KEYS */;
INSERT INTO `t_boisson_stocker_contenance` (`id_boisson_stocker_contenance`, `fk_boisson`, `fk_contenance`) VALUES
	(1, 1, 1);
/*!40000 ALTER TABLE `t_boisson_stocker_contenance` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_caisse
DROP TABLE IF EXISTS `t_caisse`;
CREATE TABLE IF NOT EXISTS `t_caisse` (
  `id_caisse` int(11) NOT NULL AUTO_INCREMENT,
  `date` timestamp NULL DEFAULT NULL,
  `caisse_avant_fete` float DEFAULT NULL,
  `caisse_apres_fete` float DEFAULT NULL,
  PRIMARY KEY (`id_caisse`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_caisse : 0 rows
/*!40000 ALTER TABLE `t_caisse` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_caisse` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_contenance
DROP TABLE IF EXISTS `t_contenance`;
CREATE TABLE IF NOT EXISTS `t_contenance` (
  `id_contenance` int(11) NOT NULL AUTO_INCREMENT,
  `type_contenance` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_contenance`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_contenance : ~2 rows (environ)
/*!40000 ALTER TABLE `t_contenance` DISABLE KEYS */;
INSERT INTO `t_contenance` (`id_contenance`, `type_contenance`) VALUES
	(1, 'Bouteille'),
	(2, 'Canette');
/*!40000 ALTER TABLE `t_contenance` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_contenance_stocker_lieu
DROP TABLE IF EXISTS `t_contenance_stocker_lieu`;
CREATE TABLE IF NOT EXISTS `t_contenance_stocker_lieu` (
  `id_contenance_stocker_lieu` int(11) NOT NULL AUTO_INCREMENT,
  `fk_contenance` int(11) DEFAULT NULL,
  `fk_lieu` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_contenance_stocker_lieu`),
  KEY `FK_t_contenance_stocker_lieu_t_contenance` (`fk_contenance`),
  KEY `FK_t_contenance_stocker_lieu_t_lieu` (`fk_lieu`),
  CONSTRAINT `FK_t_contenance_stocker_lieu_t_contenance` FOREIGN KEY (`fk_contenance`) REFERENCES `t_contenance` (`id_contenance`),
  CONSTRAINT `FK_t_contenance_stocker_lieu_t_lieu` FOREIGN KEY (`fk_lieu`) REFERENCES `t_lieu` (`id_lieu`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_contenance_stocker_lieu : ~1 rows (environ)
/*!40000 ALTER TABLE `t_contenance_stocker_lieu` DISABLE KEYS */;
INSERT INTO `t_contenance_stocker_lieu` (`id_contenance_stocker_lieu`, `fk_contenance`, `fk_lieu`) VALUES
	(1, 1, 1);
/*!40000 ALTER TABLE `t_contenance_stocker_lieu` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_fournisseur
DROP TABLE IF EXISTS `t_fournisseur`;
CREATE TABLE IF NOT EXISTS `t_fournisseur` (
  `id_fournisseur` int(11) NOT NULL AUTO_INCREMENT,
  `nom_fournisseur` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_fournisseur`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_fournisseur : ~3 rows (environ)
/*!40000 ALTER TABLE `t_fournisseur` DISABLE KEYS */;
INSERT INTO `t_fournisseur` (`id_fournisseur`, `nom_fournisseur`) VALUES
	(1, 'Cave Romontoise'),
	(2, 'Alloboisson'),
	(3, 'Landi Romont');
/*!40000 ALTER TABLE `t_fournisseur` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_lieu
DROP TABLE IF EXISTS `t_lieu`;
CREATE TABLE IF NOT EXISTS `t_lieu` (
  `id_lieu` int(11) NOT NULL AUTO_INCREMENT,
  `emplacement_lieu` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_lieu`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_lieu : ~3 rows (environ)
/*!40000 ALTER TABLE `t_lieu` DISABLE KEYS */;
INSERT INTO `t_lieu` (`id_lieu`, `emplacement_lieu`) VALUES
	(1, 'Sous le bar'),
	(2, 'Frigo gauche'),
	(3, 'Frigo droite');
/*!40000 ALTER TABLE `t_lieu` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_mail
DROP TABLE IF EXISTS `t_mail`;
CREATE TABLE IF NOT EXISTS `t_mail` (
  `id_mail` int(11) NOT NULL AUTO_INCREMENT,
  `nom_mail` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_mail`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_mail : ~3 rows (environ)
/*!40000 ALTER TABLE `t_mail` DISABLE KEYS */;
INSERT INTO `t_mail` (`id_mail`, `nom_mail`) VALUES
	(1, 'david.berset.vx@gmail.com'),
	(2, 'secretariat@boissons-corboz.ch'),
	(3, 'info@landiromont.ch');
/*!40000 ALTER TABLE `t_mail` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_mail_avoir_fournisseur
DROP TABLE IF EXISTS `t_mail_avoir_fournisseur`;
CREATE TABLE IF NOT EXISTS `t_mail_avoir_fournisseur` (
  `id_mail_avoir_fournisseur` int(11) NOT NULL AUTO_INCREMENT,
  `fk_mail` int(11) DEFAULT NULL,
  `fk_fournisseur` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_mail_avoir_fournisseur`),
  KEY `FK_t_mail_avoir_fournisseur_t_mail` (`fk_mail`),
  KEY `FK_t_mail_avoir_fournisseur_t_fournisseur` (`fk_fournisseur`),
  CONSTRAINT `FK_t_mail_avoir_fournisseur_t_fournisseur` FOREIGN KEY (`fk_fournisseur`) REFERENCES `t_fournisseur` (`id_fournisseur`),
  CONSTRAINT `FK_t_mail_avoir_fournisseur_t_mail` FOREIGN KEY (`fk_mail`) REFERENCES `t_mail` (`id_mail`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_mail_avoir_fournisseur : ~1 rows (environ)
/*!40000 ALTER TABLE `t_mail_avoir_fournisseur` DISABLE KEYS */;
INSERT INTO `t_mail_avoir_fournisseur` (`id_mail_avoir_fournisseur`, `fk_mail`, `fk_fournisseur`) VALUES
	(1, 2, 1);
/*!40000 ALTER TABLE `t_mail_avoir_fournisseur` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_personne
DROP TABLE IF EXISTS `t_personne`;
CREATE TABLE IF NOT EXISTS `t_personne` (
  `id_personne` int(11) NOT NULL AUTO_INCREMENT,
  `nom_personne` varchar(50) DEFAULT NULL,
  `prenom_personne` varchar(50) DEFAULT NULL,
  `date_naiss_personne` date DEFAULT NULL,
  PRIMARY KEY (`id_personne`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_personne : ~3 rows (environ)
/*!40000 ALTER TABLE `t_personne` DISABLE KEYS */;
INSERT INTO `t_personne` (`id_personne`, `nom_personne`, `prenom_personne`, `date_naiss_personne`) VALUES
	(1, 'Berset', 'David', '2006-11-04'),
	(2, 'Liechti', 'Matthieu', NULL),
	(3, 'Marchon', 'Lisa', NULL);
/*!40000 ALTER TABLE `t_personne` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_pers_avoir_mail
DROP TABLE IF EXISTS `t_pers_avoir_mail`;
CREATE TABLE IF NOT EXISTS `t_pers_avoir_mail` (
  `id_pers_avoir_mail` int(11) NOT NULL AUTO_INCREMENT,
  `fk_personne` int(11) DEFAULT NULL,
  `fk_mail` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_pers_avoir_mail`),
  KEY `FK_t_pers_avoir_mail_t_personne` (`fk_personne`),
  KEY `FK_t_pers_avoir_mail_t_mail` (`fk_mail`),
  CONSTRAINT `FK_t_pers_avoir_mail_t_mail` FOREIGN KEY (`fk_mail`) REFERENCES `t_mail` (`id_mail`),
  CONSTRAINT `FK_t_pers_avoir_mail_t_personne` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_pers_avoir_mail : ~1 rows (environ)
/*!40000 ALTER TABLE `t_pers_avoir_mail` DISABLE KEYS */;
INSERT INTO `t_pers_avoir_mail` (`id_pers_avoir_mail`, `fk_personne`, `fk_mail`) VALUES
	(1, 1, 1);
/*!40000 ALTER TABLE `t_pers_avoir_mail` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_pers_avoir_telephone
DROP TABLE IF EXISTS `t_pers_avoir_telephone`;
CREATE TABLE IF NOT EXISTS `t_pers_avoir_telephone` (
  `id_pers_avoir_telephone` int(11) NOT NULL AUTO_INCREMENT,
  `fk_personne` int(11) DEFAULT NULL,
  `fk_telephone` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_pers_avoir_telephone`),
  KEY `FK_t_pers_avoir_telephone_t_personne` (`fk_personne`),
  KEY `FK_t_pers_avoir_telephone_t_telephone` (`fk_telephone`),
  CONSTRAINT `FK_t_pers_avoir_telephone_t_personne` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`),
  CONSTRAINT `FK_t_pers_avoir_telephone_t_telephone` FOREIGN KEY (`fk_telephone`) REFERENCES `t_telephone` (`id_telephone`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_pers_avoir_telephone : ~1 rows (environ)
/*!40000 ALTER TABLE `t_pers_avoir_telephone` DISABLE KEYS */;
INSERT INTO `t_pers_avoir_telephone` (`id_pers_avoir_telephone`, `fk_personne`, `fk_telephone`) VALUES
	(1, 1, 1);
/*!40000 ALTER TABLE `t_pers_avoir_telephone` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_pers_entrer_boisson
DROP TABLE IF EXISTS `t_pers_entrer_boisson`;
CREATE TABLE IF NOT EXISTS `t_pers_entrer_boisson` (
  `id_pers_entrer_boisson` int(11) NOT NULL AUTO_INCREMENT,
  `fk_personne` int(11) DEFAULT NULL,
  `fk_boisson` int(11) DEFAULT NULL,
  `nombre_boisson_entrer` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_pers_entrer_boisson`),
  KEY `FK_t_pers_entrer_boisson_t_personne` (`fk_personne`),
  KEY `FK_t_pers_entrer_boisson_t_boisson` (`fk_boisson`),
  CONSTRAINT `FK_t_pers_entrer_boisson_t_boisson` FOREIGN KEY (`fk_boisson`) REFERENCES `t_boisson` (`id_boisson`),
  CONSTRAINT `FK_t_pers_entrer_boisson_t_personne` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_pers_entrer_boisson : ~1 rows (environ)
/*!40000 ALTER TABLE `t_pers_entrer_boisson` DISABLE KEYS */;
INSERT INTO `t_pers_entrer_boisson` (`id_pers_entrer_boisson`, `fk_personne`, `fk_boisson`, `nombre_boisson_entrer`) VALUES
	(1, 1, 1, 6);
/*!40000 ALTER TABLE `t_pers_entrer_boisson` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_pers_etre_adresse
DROP TABLE IF EXISTS `t_pers_etre_adresse`;
CREATE TABLE IF NOT EXISTS `t_pers_etre_adresse` (
  `id_pers_etre_adresse` int(11) NOT NULL AUTO_INCREMENT,
  `fk_personne` int(11) DEFAULT NULL,
  `fk_adresse` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_pers_etre_adresse`),
  KEY `FK_t_pers_etre_adresse_t_personne` (`fk_personne`),
  KEY `FK_t_pers_etre_adresse_t_adresse` (`fk_adresse`),
  CONSTRAINT `FK_t_pers_etre_adresse_t_adresse` FOREIGN KEY (`fk_adresse`) REFERENCES `t_adresse` (`id_adresse`),
  CONSTRAINT `FK_t_pers_etre_adresse_t_personne` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_pers_etre_adresse : ~1 rows (environ)
/*!40000 ALTER TABLE `t_pers_etre_adresse` DISABLE KEYS */;
INSERT INTO `t_pers_etre_adresse` (`id_pers_etre_adresse`, `fk_personne`, `fk_adresse`) VALUES
	(1, 1, 1);
/*!40000 ALTER TABLE `t_pers_etre_adresse` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_pers_sortie_boisson
DROP TABLE IF EXISTS `t_pers_sortie_boisson`;
CREATE TABLE IF NOT EXISTS `t_pers_sortie_boisson` (
  `id_pers_sortie_boisson` int(11) NOT NULL AUTO_INCREMENT,
  `fk_personne` int(11) DEFAULT NULL,
  `fk_boisson` int(11) DEFAULT NULL,
  `nombre_boisson_sortie` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_pers_sortie_boisson`),
  KEY `FK_t_pers_sortie_boisson_t_personne` (`fk_personne`),
  KEY `FK_t_pers_sortie_boisson_t_boisson` (`fk_boisson`),
  CONSTRAINT `FK_t_pers_sortie_boisson_t_boisson` FOREIGN KEY (`fk_boisson`) REFERENCES `t_boisson` (`id_boisson`),
  CONSTRAINT `FK_t_pers_sortie_boisson_t_personne` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_pers_sortie_boisson : ~1 rows (environ)
/*!40000 ALTER TABLE `t_pers_sortie_boisson` DISABLE KEYS */;
INSERT INTO `t_pers_sortie_boisson` (`id_pers_sortie_boisson`, `fk_personne`, `fk_boisson`, `nombre_boisson_sortie`) VALUES
	(1, 1, 1, 6);
/*!40000 ALTER TABLE `t_pers_sortie_boisson` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_telephone
DROP TABLE IF EXISTS `t_telephone`;
CREATE TABLE IF NOT EXISTS `t_telephone` (
  `id_telephone` int(11) NOT NULL AUTO_INCREMENT,
  `num_telephone` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_telephone`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_telephone : ~4 rows (environ)
/*!40000 ALTER TABLE `t_telephone` DISABLE KEYS */;
INSERT INTO `t_telephone` (`id_telephone`, `num_telephone`) VALUES
	(1, '077 511 35 67'),
	(2, '026 652 00 60'),
	(3, '079 889 64 65'),
	(4, '079 869 78 33');
/*!40000 ALTER TABLE `t_telephone` ENABLE KEYS */;

-- Export de la structure de la table berset_david_info1a_164_2023. t_telephone_avoir_fournisseur
DROP TABLE IF EXISTS `t_telephone_avoir_fournisseur`;
CREATE TABLE IF NOT EXISTS `t_telephone_avoir_fournisseur` (
  `id_telephone_avoir_fournisseur` int(11) NOT NULL AUTO_INCREMENT,
  `fk_telephone` int(11) DEFAULT NULL,
  `fk_fournisseur` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_telephone_avoir_fournisseur`),
  KEY `FK_t_telephone_avoir_fournisseur_t_telephone` (`fk_telephone`),
  KEY `FK_t_telephone_avoir_fournisseur_t_fournisseur` (`fk_fournisseur`),
  CONSTRAINT `FK_t_telephone_avoir_fournisseur_t_fournisseur` FOREIGN KEY (`fk_fournisseur`) REFERENCES `t_fournisseur` (`id_fournisseur`),
  CONSTRAINT `FK_t_telephone_avoir_fournisseur_t_telephone` FOREIGN KEY (`fk_telephone`) REFERENCES `t_telephone` (`id_telephone`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Export de données de la table berset_david_info1a_164_2023.t_telephone_avoir_fournisseur : ~1 rows (environ)
/*!40000 ALTER TABLE `t_telephone_avoir_fournisseur` DISABLE KEYS */;
INSERT INTO `t_telephone_avoir_fournisseur` (`id_telephone_avoir_fournisseur`, `fk_telephone`, `fk_fournisseur`) VALUES
	(1, 2, 1);
/*!40000 ALTER TABLE `t_telephone_avoir_fournisseur` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
