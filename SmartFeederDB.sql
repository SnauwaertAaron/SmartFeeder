-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: smartfeederdb
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `acties`
--

DROP TABLE IF EXISTS `acties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acties` (
  `ActieCode` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Beschrijving` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`ActieCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acties`
--

LOCK TABLES `acties` WRITE;
/*!40000 ALTER TABLE `acties` DISABLE KEYS */;
INSERT INTO `acties` VALUES ('PORTIE','Hoeveel (g) voeding bevatte de portie'),('VOEDING','Kijken of de hoeveelheid voeding onder een bepaald punt ligt'),('WATER','Kijken hoeveel water er nog in het waterreservoir aanwezig is');
/*!40000 ALTER TABLE `acties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feeders`
--

DROP TABLE IF EXISTS `feeders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feeders` (
  `FeederCode` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Feedernaam` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Bijnaam` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Wachtwoord` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`FeederCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feeders`
--

LOCK TABLES `feeders` WRITE;
/*!40000 ALTER TABLE `feeders` DISABLE KEYS */;
INSERT INTO `feeders` VALUES ('0000000000','Test','Test','f8367797ea4873ac5bf0e0a4a5dd1e85c065e837');
/*!40000 ALTER TABLE `feeders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metingen`
--

DROP TABLE IF EXISTS `metingen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metingen` (
  `MetingID` int NOT NULL AUTO_INCREMENT,
  `SensorID` int NOT NULL,
  `ActieCode` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `FeederCode` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Gemeten waarde` int DEFAULT NULL,
  `Datum` datetime DEFAULT NULL,
  PRIMARY KEY (`MetingID`),
  KEY `fk_metingen_sensoren1_idx` (`SensorID`),
  KEY `fk_metingen_acties1_idx` (`ActieCode`),
  KEY `fk_metingen_feeders1_idx` (`FeederCode`),
  CONSTRAINT `fk_metingen_acties1` FOREIGN KEY (`ActieCode`) REFERENCES `acties` (`ActieCode`),
  CONSTRAINT `fk_metingen_feeders1` FOREIGN KEY (`FeederCode`) REFERENCES `feeders` (`FeederCode`),
  CONSTRAINT `fk_metingen_sensoren1` FOREIGN KEY (`SensorID`) REFERENCES `sensoren` (`SensorID`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metingen`
--

LOCK TABLES `metingen` WRITE;
/*!40000 ALTER TABLE `metingen` DISABLE KEYS */;
INSERT INTO `metingen` VALUES (1,1,'WATER','0000000000',100,'2020-05-23 02:00:00'),(2,2,'VOEDING','0000000000',1,'2020-05-23 02:00:00'),(3,3,'VOEDING','0000000000',1,'2020-05-23 02:00:00'),(4,1,'WATER','0000000000',100,'2020-05-23 03:00:00'),(5,2,'VOEDING','0000000000',1,'2020-05-23 03:00:00'),(6,3,'VOEDING','0000000000',1,'2020-05-23 03:00:00'),(7,1,'WATER','0000000000',100,'2020-05-23 04:00:00'),(8,2,'VOEDING','0000000000',1,'2020-05-23 04:00:00'),(9,3,'VOEDING','0000000000',1,'2020-05-23 04:00:00'),(10,4,'PORTIE','0000000000',35,'2020-05-23 05:00:00'),(11,1,'WATER','0000000000',100,'2020-05-23 05:00:00'),(12,2,'VOEDING','0000000000',1,'2020-05-23 05:00:00'),(13,3,'VOEDING','0000000000',1,'2020-05-23 05:00:00'),(14,1,'WATER','0000000000',85,'2020-05-23 06:00:00'),(15,2,'VOEDING','0000000000',1,'2020-05-23 06:00:00'),(16,3,'VOEDING','0000000000',1,'2020-05-23 06:00:00'),(17,1,'WATER','0000000000',85,'2020-05-23 07:00:00'),(18,2,'VOEDING','0000000000',1,'2020-05-23 07:00:00'),(19,3,'VOEDING','0000000000',1,'2020-05-23 07:00:00'),(20,1,'WATER','0000000000',85,'2020-05-23 08:00:00'),(21,2,'VOEDING','0000000000',1,'2020-05-23 08:00:00'),(22,3,'VOEDING','0000000000',1,'2020-05-23 08:00:00'),(23,1,'WATER','0000000000',85,'2020-05-23 09:00:00'),(24,2,'VOEDING','0000000000',1,'2020-05-23 09:00:00'),(25,3,'VOEDING','0000000000',1,'2020-05-23 09:00:00'),(26,1,'WATER','0000000000',72,'2020-05-23 10:00:00'),(27,2,'VOEDING','0000000000',1,'2020-05-23 10:00:00'),(28,3,'VOEDING','0000000000',1,'2020-05-23 10:00:00'),(29,1,'WATER','0000000000',72,'2020-05-23 11:00:00'),(30,2,'VOEDING','0000000000',1,'2020-05-23 11:00:00'),(31,3,'VOEDING','0000000000',1,'2020-05-23 11:00:00'),(32,1,'WATER','0000000000',72,'2020-05-23 12:00:00'),(33,2,'VOEDING','0000000000',1,'2020-05-23 12:00:00'),(34,3,'VOEDING','0000000000',1,'2020-05-23 12:00:00'),(35,1,'WATER','0000000000',72,'2020-05-23 13:00:00'),(36,2,'VOEDING','0000000000',1,'2020-05-23 13:00:00'),(37,3,'VOEDING','0000000000',1,'2020-05-23 13:00:00'),(38,1,'WATER','0000000000',72,'2020-05-23 14:00:00'),(39,2,'VOEDING','0000000000',1,'2020-05-23 14:00:00'),(40,3,'VOEDING','0000000000',1,'2020-05-23 14:00:00'),(41,1,'WATER','0000000000',72,'2020-05-23 15:00:00'),(42,2,'VOEDING','0000000000',1,'2020-05-23 15:00:00'),(43,3,'VOEDING','0000000000',1,'2020-05-23 15:00:00'),(44,1,'WATER','0000000000',72,'2020-05-23 16:00:00'),(45,2,'VOEDING','0000000000',1,'2020-05-23 16:00:00'),(46,3,'VOEDING','0000000000',1,'2020-05-23 16:00:00'),(47,4,'PORTIE','0000000000',35,'2020-05-23 17:00:00'),(48,1,'WATER','0000000000',61,'2020-05-23 17:00:00'),(49,2,'VOEDING','0000000000',1,'2020-05-23 17:00:00'),(50,3,'VOEDING','0000000000',1,'2020-05-23 17:00:00');
/*!40000 ALTER TABLE `metingen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensoren`
--

DROP TABLE IF EXISTS `sensoren`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensoren` (
  `SensorID` int NOT NULL AUTO_INCREMENT,
  `Onderwerp` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Meetapparaat` varchar(75) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Meeteenheid` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`SensorID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensoren`
--

LOCK TABLES `sensoren` WRITE;
/*!40000 ALTER TABLE `sensoren` DISABLE KEYS */;
INSERT INTO `sensoren` VALUES (1,'Waterniveau','Ultrasone Rangefinder (HC-SR04)','%'),(2,'Voedingsniveau','Infrared Detector 1','binair'),(3,'Voedingsniveau','Infrared Detector 2','binair'),(4,'Portiegewicht','Load Cell','g');
/*!40000 ALTER TABLE `sensoren` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voedermomenten`
--

DROP TABLE IF EXISTS `voedermomenten`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `voedermomenten` (
  `VoedermomentID` int NOT NULL AUTO_INCREMENT,
  `FeederCode` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Uur` time DEFAULT NULL,
  `Gewicht` int DEFAULT NULL,
  PRIMARY KEY (`VoedermomentID`),
  KEY `fk_voedermomenten_feeders_idx` (`FeederCode`),
  CONSTRAINT `fk_voedermomenten_feeders` FOREIGN KEY (`FeederCode`) REFERENCES `feeders` (`FeederCode`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voedermomenten`
--

LOCK TABLES `voedermomenten` WRITE;
/*!40000 ALTER TABLE `voedermomenten` DISABLE KEYS */;
INSERT INTO `voedermomenten` VALUES (1,'1','05:00:00',35),(2,'1','17:00:00',35);
/*!40000 ALTER TABLE `voedermomenten` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'smartfeederdb'
--

--
-- Dumping routines for database 'smartfeederdb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-26 15:03:48
