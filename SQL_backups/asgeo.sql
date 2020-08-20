-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: asgeo
-- ------------------------------------------------------
-- Server version	5.7.30-0ubuntu0.18.04.1

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
-- Table structure for table `ases`
--

DROP TABLE IF EXISTS `ases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ases` (
  `id` int(11) NOT NULL,
  `asorg_id` int(11) DEFAULT NULL,
  `region` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asorganisations`
--

DROP TABLE IF EXISTS `asorganisations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asorganisations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner` varchar(40) DEFAULT NULL,
  `ownerid` varchar(15) DEFAULT NULL,
  `responsible` varchar(30) DEFAULT NULL,
  `address1` varchar(80) DEFAULT NULL,
  `address2` varchar(80) DEFAULT NULL,
  `country_code` varchar(3) DEFAULT NULL,
  `region` varchar(12) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `created` date DEFAULT NULL,
  `changed` date DEFAULT NULL,
  `lat` decimal(10,8) DEFAULT NULL,
  `lon` decimal(11,8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ctor`
--

DROP TABLE IF EXISTS `ctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ctor` (
  `code` varchar(2) NOT NULL,
  `name` varchar(60) DEFAULT NULL,
  `region` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `downstreams`
--

DROP TABLE IF EXISTS `downstreams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `downstreams` (
  `asn` int(11) NOT NULL,
  `company` varchar(80) DEFAULT NULL,
  `c_asn` int(11) DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inetnums`
--

DROP TABLE IF EXISTS `inetnums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inetnums` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prefix` varchar(20) DEFAULT NULL,
  `owner` int(10) unsigned DEFAULT NULL,
  `region` varchar(12) DEFAULT NULL,
  `lat` decimal(10,8) DEFAULT NULL,
  `lon` decimal(11,8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prefixes`
--

DROP TABLE IF EXISTS `prefixes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prefixes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subnet` varchar(16) DEFAULT NULL,
  `region` varchar(12) DEFAULT NULL,
  `prefix` int(10) unsigned DEFAULT NULL,
  `company` varchar(80) DEFAULT NULL,
  `as_id` int(10) unsigned DEFAULT NULL,
  `lat` decimal(10,8) DEFAULT NULL,
  `lon` decimal(11,8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2260 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `upstreams`
--

DROP TABLE IF EXISTS `upstreams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `upstreams` (
  `asn` int(11) NOT NULL,
  `company` varchar(80) DEFAULT NULL,
  `c_asn` int(11) DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-18  9:46:11
