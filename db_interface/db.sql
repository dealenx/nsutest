-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: NSUtest
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.17.10.1

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
-- Table structure for table `commits`
--

DROP TABLE IF EXISTS `commits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commits` (
  `commit_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) unsigned NOT NULL,
  `task_id` bigint(20) unsigned NOT NULL,
  `compiler_id` bigint(20) unsigned NOT NULL,
  `filename` varchar(50) NOT NULL,
  `source` text NOT NULL,
  `commit_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('RAW','TESTING','FINISHED') NOT NULL DEFAULT 'RAW',
  `result` text,
  PRIMARY KEY (`commit_id`),
  UNIQUE KEY `commit_id` (`commit_id`),
  KEY `user_id` (`user_id`),
  KEY `task_id` (`task_id`),
  KEY `compiler_id` (`compiler_id`),
  CONSTRAINT `commits_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `commits_ibfk_2` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`task_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `commits_ibfk_3` FOREIGN KEY (`compiler_id`) REFERENCES `compilers` (`compiler_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commits`
--

LOCK TABLES `commits` WRITE;
/*!40000 ALTER TABLE `commits` DISABLE KEYS */;
INSERT INTO `commits` VALUES (2,1,1,3,'main.cpp','Hello, World!','2018-02-01 06:36:00','RAW',NULL),(4,2,2,2,'main2.cpp','int * a = (int*)malloc(sizeof(int))','2018-02-01 06:36:53','RAW',NULL),(7,1,2,2,'test1.c','#include <stdio.h>','2018-02-01 07:26:16','RAW',NULL),(8,1,2,2,'test1.c','#include <stdio.h>','2018-02-01 07:26:32','RAW',NULL),(9,1,2,2,'test1.c','#include <stdio.h>','2018-02-01 07:30:55','RAW',NULL),(10,1,2,2,'test1.c','#include <stdio.h>','2018-02-01 07:31:44','RAW',NULL),(12,2,1,2,'test1.c','#include <stdio.h>dsadsa','2018-02-01 07:32:53','RAW',NULL);
/*!40000 ALTER TABLE `commits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compilers`
--

DROP TABLE IF EXISTS `compilers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `compilers` (
  `compiler_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`compiler_id`),
  UNIQUE KEY `compiler_id` (`compiler_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compilers`
--

LOCK TABLES `compilers` WRITE;
/*!40000 ALTER TABLE `compilers` DISABLE KEYS */;
INSERT INTO `compilers` VALUES (1,'GCC 7.2.0'),(2,'Visual Studio C++ 2015'),(3,'Clang 5.0.0');
/*!40000 ALTER TABLE `compilers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tasks` (
  `task_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` text,
  PRIMARY KEY (`task_id`),
  UNIQUE KEY `task_id` (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1,'Bubble Sort','some kind of sort'),(2,'Binary Search','some kind of search');
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `hash` text NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Jack','qwerty12345'),(2,'Bob','azaza'),(3,'ayya','12345');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-02-01 17:08:53
