-- MySQL dump 10.13  Distrib 8.0.26, for macos11 (x86_64)
--
-- Host: localhost    Database: football
-- ------------------------------------------------------
-- Server version	8.0.26

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
-- Table structure for table `Cities`
--

DROP TABLE IF EXISTS `Cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Cities` (
  `ID` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cities`
--

LOCK TABLES `Cities` WRITE;
/*!40000 ALTER TABLE `Cities` DISABLE KEYS */;
INSERT INTO `Cities` VALUES (1,'Kraków'),(2,'Wrocław'),(3,'Nowy York'),(4,'Tokio'),(5,'Gdańsk'),(6,'Pekin'),(7,'Poznań'),(8,'Szanghaj'),(9,'Waszyngton'),(10,'Chicago'),(11,'Kyoto'),(12,'Łódź'),(13,'Miami'),(14,'Toronto'),(15,'Wuhan'),(16,'Szczecin');
/*!40000 ALTER TABLE `Cities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Leagues`
--

DROP TABLE IF EXISTS `Leagues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Leagues` (
  `ID` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Leagues`
--

LOCK TABLES `Leagues` WRITE;
/*!40000 ALTER TABLE `Leagues` DISABLE KEYS */;
INSERT INTO `Leagues` VALUES (1,'Ekstraklasa'),(2,'American League'),(3,'Asian League');
/*!40000 ALTER TABLE `Leagues` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Players`
--

DROP TABLE IF EXISTS `Players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Players` (
  `ID` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `surname` varchar(45) DEFAULT NULL,
  `team` int DEFAULT NULL,
  `salary` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `team3_idx` (`team`),
  CONSTRAINT `team3` FOREIGN KEY (`team`) REFERENCES `Teams` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Players`
--

LOCK TABLES `Players` WRITE;
/*!40000 ALTER TABLE `Players` DISABLE KEYS */;
INSERT INTO `Players` VALUES (1,'Tom','Brown',6,14000),(2,'Angel','Herrera',8,8500),(3,'Mario','Sherone',10,15400),(4,'Jacek','Damiluk',12,6600),(5,'Fryderyk','Buk',1,24000),(6,'Jerry','Duck',3,16600),(7,'Nicolas','Stone',5,13000),(8,'Maciej','Sieroń',7,12000),(9,'Kamil','Kapusta',2,7400),(10,'Tom','Lee',4,4400),(11,'Gerard','Reto',9,9800),(12,'Damian','Kara',11,23000),(13,'Wojtek','Wódz',20,15400),(14,'Sergio','DaVinci',13,14600),(15,'Harry','Potter',15,28400),(16,'Sebastian','Czekaj',19,6000),(17,'Dorian','Rydz',14,7100),(18,'Lukas','Podolski',18,3200),(19,'Robert','Lewandowski',16,11800),(20,'John','Hood',17,14400);
/*!40000 ALTER TABLE `Players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Stadiums`
--

DROP TABLE IF EXISTS `Stadiums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Stadiums` (
  `ID` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `team` int DEFAULT NULL,
  `city` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `City_idx` (`city`),
  KEY `team2_idx` (`team`),
  CONSTRAINT `city` FOREIGN KEY (`city`) REFERENCES `Cities` (`ID`),
  CONSTRAINT `team2` FOREIGN KEY (`team`) REFERENCES `Teams` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Stadiums`
--

LOCK TABLES `Stadiums` WRITE;
/*!40000 ALTER TABLE `Stadiums` DISABLE KEYS */;
INSERT INTO `Stadiums` VALUES (1,'MagicPlace',6,1),(2,'Arena3',9,2),(3,'BigArea',1,3),(4,'Arena1',2,4),(5,'DDLSport',8,5),(6,'Arena2',4,15),(7,'FootStation',3,6),(8,'SPZSport',7,8),(9,'StadionWKS',19,7),(10,'KRKArena',5,10),(11,'FootStadium',10,9),(12,'BallPlace',20,14),(13,'FootPlace',11,11),(14,'SBMSport',15,13),(15,'QQSport',16,12),(16,'BORSport',17,12),(17,'CapitolDC',18,13),(18,'WWArea',12,14),(19,'FootballPalace',13,11),(20,'JuventusArea',14,15);
/*!40000 ALTER TABLE `Stadiums` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Teams`
--

DROP TABLE IF EXISTS `Teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Teams` (
  `ID` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `trainer` int DEFAULT NULL,
  `league` int DEFAULT NULL,
  `stadium` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `trainer_idx` (`trainer`),
  KEY `league_idx` (`league`),
  KEY `stadium_idx` (`stadium`),
  CONSTRAINT `league` FOREIGN KEY (`league`) REFERENCES `Leagues` (`ID`),
  CONSTRAINT `stadium` FOREIGN KEY (`stadium`) REFERENCES `Stadiums` (`ID`),
  CONSTRAINT `trainer` FOREIGN KEY (`trainer`) REFERENCES `Trainers` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Teams`
--

LOCK TABLES `Teams` WRITE;
/*!40000 ALTER TABLE `Teams` DISABLE KEYS */;
INSERT INTO `Teams` VALUES (1,'WKS',4,1,1),(2,'Juventus',20,2,2),(3,'FC Tokyo',1,3,3),(4,'AC Kyoto',19,1,4),(5,'Cracovia',2,2,5),(6,'AC Washington',17,3,6),(7,'Real Madrid',3,2,7),(8,'FC Pekin',18,3,8),(9,'Chicago Bulls',10,3,9),(10,'Miami Beach',11,1,10),(11,'FC Berlin',12,1,11),(12,'AC Wien',13,2,12),(13,'AC Szanghaj',5,2,14),(14,'Lechia Gdańsk',6,3,13),(15,'Lech Poznań',7,1,15),(16,'Wuhan Covid',8,2,16),(17,'Toronto Club',14,3,17),(18,'NYC Club',15,2,18),(19,'Wisła Kraków',9,1,19),(20,'FC Barcelona',16,2,20);
/*!40000 ALTER TABLE `Teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Trainers`
--

DROP TABLE IF EXISTS `Trainers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Trainers` (
  `ID` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `surname` varchar(45) DEFAULT NULL,
  `team` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `Team_idx` (`team`),
  CONSTRAINT `team` FOREIGN KEY (`team`) REFERENCES `Teams` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Trainers`
--

LOCK TABLES `Trainers` WRITE;
/*!40000 ALTER TABLE `Trainers` DISABLE KEYS */;
INSERT INTO `Trainers` VALUES (1,'Dawid','Szynol',3),(2,'Justin','Bieber',20),(3,'Dominik','Kot',1),(4,'Bartosz','Kula',2),(5,'Michał','Matczak',19),(6,'Dany','Doom',6),(7,'Robert','Makłowicz',16),(8,'Sławomir','Peszko',5),(9,'Ray','Filly',4),(10,'Tommy','Cash',17),(11,'Darek','Gwóźdź',18),(12,'Johny','Deep',7),(13,'Willy','Roy',10),(14,'Billy','Boy',11),(15,'Walter','White',13),(16,'Kacper','Czarny',14),(17,'Emma','Watson',12),(18,'Emily','Rose',15),(19,'Sebastian','Czekaj',8),(20,'Kuba','Wojewódzki',9);
/*!40000 ALTER TABLE `Trainers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'football'
--
/*!50003 DROP PROCEDURE IF EXISTS `increase_salary` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `increase_salary`(IN how_much INT)
BEGIN
UPDATE Players 
SET salary = salary + how_much;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-09-19 21:55:09
