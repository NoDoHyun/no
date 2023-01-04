-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: crime
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES ('광주동부경찰서',1240,1056,1223,41,813,369),('광주서부경찰서',2621,2100,2330,50,1590,690),('광주남부경찰서',1538,1147,1302,20,700,582),('광주북부경찰서',3703,2873,3250,62,2015,1173),('광주광산경찰서',2946,2360,2759,49,1754,956);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231`
--

LOCK TABLES `경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` WRITE;
/*!40000 ALTER TABLE `경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` DISABLE KEYS */;
INSERT INTO `경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` VALUES ('광주광역시경찰청','발  생  건  수',0,0,0,0,0,''),('광주광역시경찰청','검  거  건  수',0,1,85,0,18,''),('광주광역시경찰청','검  거  인  원',0,2,91,0,47,''),('광주광역시경찰청','구     속',0,2,11,0,6,''),('광주광역시경찰청','불 구 속',0,0,53,0,31,''),('광주광역시경찰청','기     타',0,0,27,0,10,''),('광주동부경찰서','발  생  건  수',2,1,66,494,677,''),('광주동부경찰서','검  거  건  수',2,1,61,350,642,''),('광주동부경찰서','검  거  인  원',2,2,60,279,880,''),('광주동부경찰서','구     속',2,2,3,13,21,''),('광주동부경찰서','불 구 속',0,0,38,241,534,''),('광주동부경찰서','기     타',0,0,19,25,325,''),('광주서부경찰서','발  생  건  수',4,3,142,1106,1366,''),('광주서부경찰서','검  거  건  수',3,3,133,731,1230,''),('광주서부경찰서','검  거  인  원',3,3,153,626,1545,''),('광주서부경찰서','구     속',2,3,6,24,15,''),('광주서부경찰서','불 구 속',0,0,91,532,967,''),('광주서부경찰서','기     타',1,0,56,70,563,''),('광주북부경찰서','발  생  건  수',2,3,146,1465,2087,''),('광주북부경찰서','검  거  건  수',4,3,120,971,1775,''),('광주북부경찰서','검  거  인  원',4,3,130,725,2388,''),('광주북부경찰서','구     속',3,2,14,27,16,''),('광주북부경찰서','불 구 속',1,1,81,598,1334,''),('광주북부경찰서','기     타',0,0,35,100,1038,''),('광주광산경찰서','발  생  건  수',1,5,125,1184,1631,''),('광주광산경찰서','검  거  건  수',1,4,98,798,1459,''),('광주광산경찰서','검  거  인  원',1,4,100,656,1998,''),('광주광산경찰서','구     속',1,2,11,24,11,''),('광주광산경찰서','불 구 속',0,2,62,561,1129,''),('광주광산경찰서','기     타',0,0,27,71,858,''),('광주남부경찰서','발  생  건  수',0,1,62,636,839,''),('광주남부경찰서','검  거  건  수',0,1,57,371,718,''),('광주남부경찰서','검  거  인  원',0,2,65,305,930,''),('광주남부경찰서','구     속',0,0,2,12,6,''),('광주남부경찰서','불 구 속',0,0,48,232,420,''),('광주남부경찰서','기     타',0,2,15,61,504,'');
/*!40000 ALTER TABLE `경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-03 18:18:07