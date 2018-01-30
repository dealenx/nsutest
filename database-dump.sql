-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: pythonweb
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `s_lang`
--

DROP TABLE IF EXISTS `s_lang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `s_lang` (
  `id` int(6) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `s_lang`
--

LOCK TABLES `s_lang` WRITE;
/*!40000 ALTER TABLE `s_lang` DISABLE KEYS */;
INSERT INTO `s_lang` VALUES (1,'C++');
/*!40000 ALTER TABLE `s_lang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `s_tasks`
--

DROP TABLE IF EXISTS `s_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `s_tasks` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `lang` int(6) DEFAULT NULL,
  `time` datetime NOT NULL,
  `state` varchar(50) DEFAULT NULL,
  `client_out` varchar(256) DEFAULT NULL,
  `source` varchar(10000) DEFAULT NULL,
  `file_name` varchar(128) DEFAULT NULL,
  `json_data` varchar(9000) DEFAULT NULL,
  `uid` int(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `s_tasks`
--

LOCK TABLES `s_tasks` WRITE;
/*!40000 ALTER TABLE `s_tasks` DISABLE KEYS */;
INSERT INTO `s_tasks` VALUES (1,1,'2018-01-30 05:29:58',NULL,NULL,NULL,NULL,NULL,NULL),(2,2,'2018-01-30 05:30:31',NULL,NULL,NULL,NULL,NULL,NULL),(4,1,'2018-01-30 06:05:07',NULL,NULL,NULL,NULL,NULL,NULL),(5,1,'2018-01-30 06:05:50',NULL,NULL,NULL,NULL,NULL,NULL),(6,1,'2018-01-30 06:05:50',NULL,NULL,NULL,NULL,NULL,NULL),(10,3,'2018-01-30 06:07:23',NULL,NULL,NULL,NULL,NULL,NULL),(11,3,'2018-01-30 06:21:07',NULL,NULL,NULL,NULL,NULL,NULL),(12,5,'2018-01-30 06:21:30',NULL,NULL,NULL,NULL,NULL,NULL),(13,2,'2018-01-30 06:43:02','wait',NULL,'void main()','void main()',NULL,1),(14,1,'2018-01-30 06:51:31','wait',NULL,'void main()','main.cpp',NULL,1),(15,1,'2018-01-30 06:58:56','wait',NULL,'void main()','main.cpp',NULL,1),(16,1,'2018-01-30 06:59:03','wait',NULL,'void main()','main.cpp',NULL,1),(17,1,'2018-01-30 07:26:01','wait',NULL,'void main()','main.cpp',NULL,1);
/*!40000 ALTER TABLE `s_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `s_users`
--

DROP TABLE IF EXISTS `s_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `s_users` (
  `id` int(6) DEFAULT NULL,
  `login` varchar(256) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `s_users`
--

LOCK TABLES `s_users` WRITE;
/*!40000 ALTER TABLE `s_users` DISABLE KEYS */;
INSERT INTO `s_users` VALUES (1,'admin');
/*!40000 ALTER TABLE `s_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-30  8:52:49
