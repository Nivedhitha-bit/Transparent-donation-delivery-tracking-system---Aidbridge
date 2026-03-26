CREATE DATABASE  IF NOT EXISTS `aid_bridge` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `aid_bridge`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: aid_bridge
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `accounts_donorprofile`
--

DROP TABLE IF EXISTS `accounts_donorprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_donorprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total_donations` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_donorprofile_user_id_4e31ebcb_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_donorprofile`
--

LOCK TABLES `accounts_donorprofile` WRITE;
/*!40000 ALTER TABLE `accounts_donorprofile` DISABLE KEYS */;
INSERT INTO `accounts_donorprofile` VALUES (4,2,11),(5,1,12),(6,4,18),(7,0,20);
/*!40000 ALTER TABLE `accounts_donorprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_ngoprofile`
--

DROP TABLE IF EXISTS `accounts_ngoprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_ngoprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `organization_name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `address` longtext NOT NULL,
  `city` varchar(100) NOT NULL,
  `pincode` varchar(10) NOT NULL,
  `website` varchar(200) NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `approved_at` datetime(6) DEFAULT NULL,
  `approval_email_sent` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_ngoprofile_user_id_e769ad51_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_ngoprofile`
--

LOCK TABLES `accounts_ngoprofile` WRITE;
/*!40000 ALTER TABLE `accounts_ngoprofile` DISABLE KEYS */;
INSERT INTO `accounts_ngoprofile` VALUES (4,'Hope Foundation','Providing food and clothes','','New York','10001','',1,NULL,0,13),(5,'Care Network','Medical and education support','','Boston','02115','',1,NULL,0,14),(6,'ABC Foundations','Customized test NGO','','Salem','636001','',1,NULL,0,17),(7,'Charity_care','Charity_care is the active ngo in coimbatore helping 1000s of  lives','','coimbatore','641001','',1,'2026-03-26 06:08:14.797000',0,21),(8,'xyz_foundations','we having running our organisation in t nagar ','','chennai','600017','',1,'2026-03-26 06:45:36.088000',0,22),(9,'xyz_organisations','xyz orgnaization is in salem','','Salem','636005','',1,'2026-03-26 09:39:22.858000',0,23);
/*!40000 ALTER TABLE `accounts_ngoprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_passwordresettoken`
--

DROP TABLE IF EXISTS `accounts_passwordresettoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_passwordresettoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `used` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `accounts_passwordresettoken_user_id_2789bc5c_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `accounts_passwordresettoken_user_id_2789bc5c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_passwordresettoken`
--

LOCK TABLES `accounts_passwordresettoken` WRITE;
/*!40000 ALTER TABLE `accounts_passwordresettoken` DISABLE KEYS */;
INSERT INTO `accounts_passwordresettoken` VALUES (1,'41578ab6-111a-482c-b6d6-a309dc7e7681','2026-03-26 05:54:37.731000',0,17),(2,'4997722a-a8fd-48d3-a01b-ea544a1514dc','2026-03-26 05:55:47.730000',0,18);
/*!40000 ALTER TABLE `accounts_passwordresettoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `city` varchar(100) NOT NULL,
  `pincode` varchar(10) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$600000$pV8rIlVwqz8GfirjbTH0vg$1v1w4oLy7eEQ4/WJYkjSjX223cTys/eDzGU5fgYtg4g=','2026-03-26 05:42:37.154000',1,'admin','','','admin@example.com',1,1,'2026-03-26 02:03:30.623000','donor','','','',0,'','2026-03-26 02:03:30.851000'),(11,'pbkdf2_sha256$600000$2Mi7vthWmD2Yj3liaZ0KQ8$g3OLWB0IEvi2VSUArcbuXlV4v7vxFvAcGFC/W32FMIc=',NULL,0,'donor1','Alice','Donor','donor1@example.com',0,1,'2026-03-26 03:34:04.767000','donor','','New York','10001',0,'','2026-03-26 03:34:05.674000'),(12,'pbkdf2_sha256$600000$WwIM2znv2T4QooPBQ11CcJ$UCx4MtGIyMmCRwR/8wz3T5H3H0ac5IlqwJkumt5fykM=',NULL,0,'donor2','Bob','Giver','donor2@example.com',0,1,'2026-03-26 03:34:05.746000','donor','','New York','10001',0,'','2026-03-26 03:34:06.989000'),(13,'pbkdf2_sha256$600000$fcDtNfhsPyYIl8ppS8vzbV$6UAXs1/CAXGoiRPT+7rr0XEmBAv729idpJoZm51hVwk=',NULL,0,'ngo_hope','Hope','Org','hope@ngo.org',0,1,'2026-03-26 03:34:07.163000','ngo','','New York','',1,'','2026-03-26 03:34:08.336000'),(14,'pbkdf2_sha256$600000$wyKNNUu343JxXb3ScrYrE4$j+A9DGkclZe4OK4pXtWvyJmbXxpHmuRiMmLJp9F/g7w=',NULL,0,'ngo_care','Care','Group','care@ngo.org',0,1,'2026-03-26 03:34:08.382000','ngo','','Boston','',1,'','2026-03-26 03:34:09.502000'),(15,'pbkdf2_sha256$600000$w1oou3kFjdUpc3RFmAtpoB$AGLs74wfOqyLqM0zJBeaWEZxhP9/2aF9UPESwPEo9gs=',NULL,0,'vol_john','John','Doe','john@vol.com',0,1,'2026-03-26 03:34:09.744000','volunteer','','New York','',0,'','2026-03-26 03:34:10.720000'),(16,'pbkdf2_sha256$600000$bY4c0MJ4vXnXm6xQn6xn6k$e54zuaqH6YyT6Kkmt7L76f0c7fPaOQDCyDSdhrx++n8=',NULL,0,'vol_sarah','Sarah','Connor','sarah@vol.com',0,1,'2026-03-26 03:34:10.799000','volunteer','','New York','',0,'','2026-03-26 03:34:11.433000'),(17,'pbkdf2_sha256$600000$IzcnWsu0YrMItCDWQmNxGd$D9SmqN2hTR7vxCWhRP/eZ6v9C1dsKbTWUYvsibnyx08=','2026-03-26 09:40:15.115000',0,'abc_foundations','ABC','Foundations','rashmim9566@gmail.com',0,1,'2026-03-26 03:45:32.861000','ngo','','','',1,'','2026-03-26 03:45:33.116000'),(18,'pbkdf2_sha256$600000$52JQodEnyWHYlwCoiYxAcL$AnRR8LXAfWMXzAs/A7G9Ud40F7NXdZItQV1++8KL9eU=','2026-03-26 16:43:08.947509',0,'nithya','Nithya','S','nivedhithas994@gmail.com',0,1,'2026-03-26 03:45:33.132000','donor','','Karur','639001',0,'','2026-03-26 03:45:33.439000'),(19,'pbkdf2_sha256$600000$0t3DX4840PGH5Man94w3it$YH0gme3MhWZI+qe7IPPC8et0YfCDmzXdKVvNpsYjYW8=','2026-03-26 14:14:49.565000',0,'preethi','Preethi','S','preethipri44@gmail.com',0,1,'2026-03-26 03:45:33.457000','volunteer','9345813374','Salem','636001',0,'','2026-03-26 03:45:33.706000'),(20,'pbkdf2_sha256$600000$fiNkEq8SdT8L2kSPeZ63Rc$RwnE5If3sZvI9dYdGHfqoZaT4Wz4Y4AQx4Q3JeIk35I=','2026-03-26 06:01:37.900000',0,'pradhikshamohankumar2005','pradhiksha','','pradhikshamohankumar2005@gmail.com',0,1,'2026-03-26 06:00:51.638000','donor','','coimbatore','641001',0,'','2026-03-26 06:00:52.819000'),(21,'pbkdf2_sha256$600000$LmiGqEpOH6tO4FedvVNVpq$9fS1h21G6+kUK/etdIdzfphOCn1Ok9fdpMek69adpkg=','2026-03-26 06:09:25.032000',0,'preethipri1999','Charity_care','','preethipri1999@gmail.com',0,1,'2026-03-26 06:06:56.158000','ngo','','coimbatore','641001',1,'','2026-03-26 06:06:57.488000'),(22,'pbkdf2_sha256$600000$mrPEJ8Mh1tTJ4K4N0gGhrZ$A0/RZ9c8ItbwT0GDjFNW94cSqX9wRVaNHAW2M+nP6Oo=',NULL,0,'xyz','xyz_foundations','','xyz@gmail.com',0,1,'2026-03-26 06:43:29.247000','ngo','','chennai','600017',1,'','2026-03-26 06:43:33.400000'),(23,'pbkdf2_sha256$600000$B3Nj1QWgcNwZM4xYOqs5tg$GNly3egeDzDgJauBoSlybxJJQeaAQ9Twu78jLUJ3NDk=',NULL,0,'xyze','xyz_organisations','','xyze@gmail.com',0,1,'2026-03-26 09:37:42.341000','ngo','','Salem','636005',1,'','2026-03-26 09:37:42.942000');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_volunteerprofile`
--

DROP TABLE IF EXISTS `accounts_volunteerprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_volunteerprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_available` tinyint(1) NOT NULL,
  `city` varchar(100) NOT NULL,
  `pincode` varchar(10) NOT NULL,
  `total_tasks` int NOT NULL,
  `completed_tasks` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_volunteerprofile_user_id_06845d71_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteerprofile`
--

LOCK TABLES `accounts_volunteerprofile` WRITE;
/*!40000 ALTER TABLE `accounts_volunteerprofile` DISABLE KEYS */;
INSERT INTO `accounts_volunteerprofile` VALUES (4,1,'New York','10001',2,1,15),(5,1,'New York','10001',0,0,16),(6,1,'Salem','636001',3,2,19);
/*!40000 ALTER TABLE `accounts_volunteerprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add volunteer profile',7,'add_volunteerprofile'),(26,'Can change volunteer profile',7,'change_volunteerprofile'),(27,'Can delete volunteer profile',7,'delete_volunteerprofile'),(28,'Can view volunteer profile',7,'view_volunteerprofile'),(29,'Can add password reset token',8,'add_passwordresettoken'),(30,'Can change password reset token',8,'change_passwordresettoken'),(31,'Can delete password reset token',8,'delete_passwordresettoken'),(32,'Can view password reset token',8,'view_passwordresettoken'),(33,'Can add ngo profile',9,'add_ngoprofile'),(34,'Can change ngo profile',9,'change_ngoprofile'),(35,'Can delete ngo profile',9,'delete_ngoprofile'),(36,'Can view ngo profile',9,'view_ngoprofile'),(37,'Can add donor profile',10,'add_donorprofile'),(38,'Can change donor profile',10,'change_donorprofile'),(39,'Can delete donor profile',10,'delete_donorprofile'),(40,'Can view donor profile',10,'view_donorprofile'),(41,'Can add donation',11,'add_donation'),(42,'Can change donation',11,'change_donation'),(43,'Can delete donation',11,'delete_donation'),(44,'Can view donation',11,'view_donation'),(45,'Can add volunteer assignment',12,'add_volunteerassignment'),(46,'Can change volunteer assignment',12,'change_volunteerassignment'),(47,'Can delete volunteer assignment',12,'delete_volunteerassignment'),(48,'Can view volunteer assignment',12,'view_volunteerassignment'),(49,'Can add notification',13,'add_notification'),(50,'Can change notification',13,'change_notification'),(51,'Can delete notification',13,'delete_notification'),(52,'Can view notification',13,'view_notification'),(53,'Can add donation request',14,'add_donationrequest'),(54,'Can change donation request',14,'change_donationrequest'),(55,'Can delete donation request',14,'delete_donationrequest'),(56,'Can view donation request',14,'view_donationrequest');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (10,'accounts','donorprofile'),(9,'accounts','ngoprofile'),(8,'accounts','passwordresettoken'),(6,'accounts','user'),(7,'accounts','volunteerprofile'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(11,'ngo','donation'),(14,'ngo','donationrequest'),(13,'ngo','notification'),(12,'ngo','volunteerassignment'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-03-26 16:24:02.760998'),(2,'contenttypes','0002_remove_content_type_name','2026-03-26 16:24:02.917430'),(3,'auth','0001_initial','2026-03-26 16:24:03.248969'),(4,'auth','0002_alter_permission_name_max_length','2026-03-26 16:24:03.359882'),(5,'auth','0003_alter_user_email_max_length','2026-03-26 16:24:03.366675'),(6,'auth','0004_alter_user_username_opts','2026-03-26 16:24:03.377885'),(7,'auth','0005_alter_user_last_login_null','2026-03-26 16:24:03.384854'),(8,'auth','0006_require_contenttypes_0002','2026-03-26 16:24:03.416006'),(9,'auth','0007_alter_validators_add_error_messages','2026-03-26 16:24:03.426679'),(10,'auth','0008_alter_user_username_max_length','2026-03-26 16:24:03.443114'),(11,'auth','0009_alter_user_last_name_max_length','2026-03-26 16:24:03.461411'),(12,'auth','0010_alter_group_name_max_length','2026-03-26 16:24:03.492309'),(13,'auth','0011_update_proxy_permissions','2026-03-26 16:24:03.505216'),(14,'auth','0012_alter_user_first_name_max_length','2026-03-26 16:24:03.519050'),(15,'accounts','0001_initial','2026-03-26 16:24:04.305127'),(16,'admin','0001_initial','2026-03-26 16:24:04.493690'),(17,'admin','0002_logentry_remove_auto_add','2026-03-26 16:24:04.504473'),(18,'admin','0003_logentry_add_action_flag_choices','2026-03-26 16:24:04.518586'),(19,'ngo','0001_initial','2026-03-26 16:24:05.199332'),(20,'sessions','0001_initial','2026-03-26 16:24:05.271434');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('637osjy2rm6y9bjckkwwr7ffglcf51d3','.eJxVjEsOwiAUAO_C2hDoe_xcuu8ZCI-PVA1NSrsy3t2QdKHbmcm8mQ_HXv3R8-aXxK5MGnb5hRTiM7dh0iO0-8rj2vZtIT4SftrO5zXl1-1s_wY19Dq-AiCSjsUJRGWFMSBtljZJEFNGNEKXoiSCE7pYpxIRahdNVJAmS8A-X9B3NsA:1w5eUm:DclP1lCJIbXF0gPnnvwbrRmMugtx1FliGwl5fCuJC4E','2026-03-27 06:47:08.143000'),('6y6yrefs7ru2loda29ed80yktm4dvs6f','.eJxVjMsOwiAQAP-FsyFdaJfFo_d-A1leUjU0Ke3J-O-GpAe9zkzmLRwfe3FHS5tborgKLS6_zHN4ptpFfHC9rzKsdd8WL3siT9vkvMb0up3t36BwK30LySrIqDGYDNbmmCcmYg1kKRMxg0JjsmE_TIjsx0CoTVB2ABxDEp8v1AE3Yw:1w5bbs:UjYi1VLIkkWwUpmfnWiwQ6bWRG8LcKlHXN-9UrUdLtQ','2026-03-27 03:42:16.805000'),('74fw6sk4dxvkqhf759m2pu7uvqiny0bk','.eJxVjMsKwjAQAP9lzxJM1nSbHr37DWVfmKq00MdJ_Hcp9KDXmWHe0PO21n5bfO4Hgw5igdMvFNanj7uxB4_3Keg0rvMgYU_CYZdwm8xf16P9G1ReKnSAhUkwkbori7uSO7WloAjRhdSz8xk1WZM5W1siYtvkJiVTk-gIny83MTjZ:1w5hKB:cJRpajlD-97N80XUMitLoWfj53oKiszDKhdnzAuN5Og','2026-03-27 09:48:23.502000'),('anztyraekftj2x7in5cviooff7cyla7e','.eJxVjMsOwiAQAP-FsyFdaJfFo_d-A1leUjU0Ke3J-O-GpAe9zkzmLRwfe3FHS5tborgKLS6_zHN4ptpFfHC9rzKsdd8WL3siT9vkvMb0up3t36BwK30LySrIqDGYDNbmmCcmYg1kKRMxg0JjsmE_TIjsx0CoTVB2ABxDEp8v1AE3Yw:1w5baQ:-hLPhYqu-Vz3B2GiBQbDjycXGNEteEVISb0G2vuDCYU','2026-03-27 03:40:46.203000'),('fw0nko5yqtwj34jh9b0orxsu02x7vdkr','.eJxVjEsOwiAUAO_C2hDoe_xcuu8ZCI-PVA1NSrsy3t2QdKHbmcm8mQ_HXv3R8-aXxK5MGnb5hRTiM7dh0iO0-8rj2vZtIT4SftrO5zXl1-1s_wY19Dq-AiCSjsUJRGWFMSBtljZJEFNGNEKXoiSCE7pYpxIRahdNVJAmS8A-X9B3NsA:1w5eUp:pz2U7ZRK8UFHp4ao-h8_0MCF3G8eDvWLcBf9cjRogGU','2026-03-27 06:47:11.269000'),('hd650uvbcwyuybkm6yq5qyq4y5e7tqc0','.eJxVjMsKwjAQAP9lzxJM1nSbHr37DWVfmKq00MdJ_Hcp9KDXmWHe0PO21n5bfO4Hgw5igdMvFNanj7uxB4_3Keg0rvMgYU_CYZdwm8xf16P9G1ReKnSAhUkwkbori7uSO7WloAjRhdSz8xk1WZM5W1siYtvkJiVTk-gIny83MTjZ:1w5eYy:itZ_-8Mgt3So-YpgFCODaQsFYnWXs9uJseRHTq0PLb4','2026-03-27 06:51:28.844000'),('jkhyody4bgwqc8980ze1zg72qocp501t','.eJxVjMsOwiAQAP9lz4bwrKVH7_0GsuyCVA0kpT0Z_9006UGvM5N5Q8B9K2HvaQ0LwwRqhMsvjEjPVA_DD6z3JqjVbV2iOBJx2i7mxul1O9u_QcFeYIKEVnHEweBgjaJsdJYSI0fvnUNMSlImtsq5fJXaJDYjak_WZM2WMMLnCyssOQE:1w5nnZ:HJydtqdj3y3Jal_slUixb_eu7c-Y5_hP0bKxhn_O2ME','2026-03-27 16:43:09.005515'),('ogfl1gftkgjmxmml5r1ffml7o89emwd9','.eJxVjEsOwiAUAO_C2hDoe_xcuu8ZCI-PVA1NSrsy3t2QdKHbmcm8mQ_HXv3R8-aXxK5MGnb5hRTiM7dh0iO0-8rj2vZtIT4SftrO5zXl1-1s_wY19Dq-AiCSjsUJRGWFMSBtljZJEFNGNEKXoiSCE7pYpxIRahdNVJAmS8A-X9B3NsA:1w5eUr:EuA65d2Ogf9w7X6w-8YpBr_rXiaAey5wqa_bRlp6ECc','2026-03-27 06:47:13.091000'),('oif3je51xmslqe4dp97yvyolqdcd1aap','.eJxVjMsKwjAQAP9lzxJM1nSbHr37DWVfmKq00MdJ_Hcp9KDXmWHe0PO21n5bfO4Hgw5igdMvFNanj7uxB4_3Keg0rvMgYU_CYZdwm8xf16P9G1ReKnSAhUkwkbori7uSO7WloAjRhdSz8xk1WZM5W1siYtvkJiVTk-gIny83MTjZ:1w5f0x:EXTvfRcuU8zr18XpwIX-x6pMbGT0-vt1usVJCAGhjlM','2026-03-27 07:20:23.741000'),('oon8bt328gthdusabqj1zz0a9nvd5v2w','.eJxVjMsOwiAQAP-FsyFdaJfFo_d-A1leUjU0Ke3J-O-GpAe9zkzmLRwfe3FHS5tborgKLS6_zHN4ptpFfHC9rzKsdd8WL3siT9vkvMb0up3t36BwK30LySrIqDGYDNbmmCcmYg1kKRMxg0JjsmE_TIjsx0CoTVB2ABxDEp8v1AE3Yw:1w5bbi:ajnDme4cfN3X-dYYhvSga7uWTBO8DJX2CJkt-lBs0pc','2026-03-27 03:42:06.853000'),('stx1deypkiktofkzkwu88l1qguui7167','.eJxVjEsOwiAUAO_C2hDoe_xcuu8ZCI-PVA1NSrsy3t2QdKHbmcm8mQ_HXv3R8-aXxK5MGnb5hRTiM7dh0iO0-8rj2vZtIT4SftrO5zXl1-1s_wY19Dq-AiCSjsUJRGWFMSBtljZJEFNGNEKXoiSCE7pYpxIRahdNVJAmS8A-X9B3NsA:1w5cR3:81w5gOOj-X-xDwhE23Pd0iX2K9yybOzCoonD2v3x2PI','2026-03-27 04:35:09.724000'),('z4kictxhg9k2fr6tyl1ppn9ox4ow3ni4','.eJxVjEsOwiAUAO_C2hDoe_xcuu8ZCI-PVA1NSrsy3t2QdKHbmcm8mQ_HXv3R8-aXxK5MGnb5hRTiM7dh0iO0-8rj2vZtIT4SftrO5zXl1-1s_wY19Dq-AiCSjsUJRGWFMSBtljZJEFNGNEKXoiSCE7pYpxIRahdNVJAmS8A-X9B3NsA:1w5eUp:pz2U7ZRK8UFHp4ao-h8_0MCF3G8eDvWLcBf9cjRogGU','2026-03-27 06:47:11.474000');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ngo_donation`
--

DROP TABLE IF EXISTS `ngo_donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ngo_donation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_name` varchar(200) NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `unit` varchar(20) NOT NULL,
  `message` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `donor_id` bigint NOT NULL,
  `request_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ngo_donation_request_id_359eb747_fk_ngo_donationrequest_id` (`request_id`),
  KEY `ngo_donation_donor_id_0d02dfac_fk_accounts_user_id` (`donor_id`),
  CONSTRAINT `ngo_donation_donor_id_0d02dfac_fk_accounts_user_id` FOREIGN KEY (`donor_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `ngo_donation_request_id_359eb747_fk_ngo_donationrequest_id` FOREIGN KEY (`request_id`) REFERENCES `ngo_donationrequest` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ngo_donation`
--

LOCK TABLES `ngo_donation` WRITE;
/*!40000 ALTER TABLE `ngo_donation` DISABLE KEYS */;
INSERT INTO `ngo_donation` VALUES (4,'Rice Sacks',10.00,'kg','Hope this helps!','picked_up','2026-03-26 03:34:11.677000','2026-03-26 03:34:11.677000',11,4),(5,'Warm Blankets',5.00,'pieces','Freshly washed.','pledged','2026-03-26 03:34:11.712000','2026-03-26 03:34:11.712000',12,5),(6,'Dal',5.00,'kg','','delivered','2026-03-26 03:34:11.754000','2026-03-26 03:34:11.755000',11,4),(7,'Wheat Flour',5.00,'kg','Here is the wheat flour!','picked_up','2026-03-26 03:45:33.750000','2026-03-26 03:45:33.750000',18,7),(8,'Used but clean clothes',10.00,'pieces','Hope it helps.','completed','2026-03-26 03:45:33.758000','2026-03-26 09:44:05.235000',18,8),(9,'Note Books',50.00,'pieces','Pledging 50 notebooks','pledged','2026-03-26 03:45:33.764000','2026-03-26 03:45:33.764000',18,10),(10,'First Aid Kits',10.00,'packs','Happy to supply these kits!','completed','2026-03-26 04:27:24.029000','2026-03-26 04:37:37.948000',18,12),(11,'Emergency First Aid Kits',10.00,'packs','','approved','2026-03-26 06:20:13.974000','2026-03-26 09:41:55.731000',18,12),(12,'Emergency First Aid Kits',5.00,'packs','','approved','2026-03-26 09:20:40.901000','2026-03-26 09:42:37.073000',18,12),(13,'Kids Clothes',4.00,'pieces','','pledged','2026-03-26 09:46:32.946000','2026-03-26 09:46:32.946000',18,8);
/*!40000 ALTER TABLE `ngo_donation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ngo_donationrequest`
--

DROP TABLE IF EXISTS `ngo_donationrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ngo_donationrequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_category` varchar(50) NOT NULL,
  `item_name` varchar(200) NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `unit` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `location` varchar(300) NOT NULL,
  `city` varchar(100) NOT NULL,
  `pincode` varchar(10) NOT NULL,
  `status` varchar(30) NOT NULL,
  `quantity_received` decimal(10,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `ngo_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ngo_donationrequest_ngo_id_ed10eec5_fk_accounts_user_id` (`ngo_id`),
  CONSTRAINT `ngo_donationrequest_ngo_id_ed10eec5_fk_accounts_user_id` FOREIGN KEY (`ngo_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ngo_donationrequest`
--

LOCK TABLES `ngo_donationrequest` WRITE;
/*!40000 ALTER TABLE `ngo_donationrequest` DISABLE KEYS */;
INSERT INTO `ngo_donationrequest` VALUES (4,'food','Rice and Groceries',100.00,'kg','','123 Main St','New York','10001','active',15.00,'2026-03-26 03:34:11.553000','2026-03-26 03:34:11.553000',13),(5,'clothing','Winter Blankets',50.00,'pieces','','123 Main St','New York','10001','active',0.00,'2026-03-26 03:34:11.598000','2026-03-26 03:34:11.598000',13),(6,'medical','First Aid Supplies',20.00,'packs','','45 Health Ave','Boston','','active',0.00,'2026-03-26 03:34:11.640000','2026-03-26 03:34:11.641000',14),(7,'food','Wheat Flour (Atta)',50.00,'kg','','Salem Hub','Salem','636001','active',5.00,'2026-03-26 03:45:33.724000','2026-03-26 03:45:33.724000',17),(8,'clothing','Kids Clothes',30.00,'pieces','','Salem Hub','Salem','636001','active',20.00,'2026-03-26 03:45:33.730000','2026-03-26 09:44:05.330000',17),(9,'hygiene','Soap and Toothpaste',100.00,'packs','','Salem Hub','Salem','','active',0.00,'2026-03-26 03:45:33.736000','2026-03-26 03:45:33.736000',17),(10,'educational','Note Books',200.00,'pieces','','Salem Hub','Salem','','active',0.00,'2026-03-26 03:45:33.743000','2026-03-26 03:45:33.743000',17),(11,'medical','Emergency First Aid Kits',10.00,'packs','Urgent need for first aid kits','Salem Hub','Salem','636001','active',0.00,'2026-03-26 04:04:30.823000','2026-03-26 04:04:30.823000',17),(12,'medical','Emergency First Aid Kits',50.00,'packs','','Main Hospital Road','Salem','636001','active',20.00,'2026-03-26 04:27:23.678000','2026-03-26 09:41:23.389000',17);
/*!40000 ALTER TABLE `ngo_donationrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ngo_notification`
--

DROP TABLE IF EXISTS `ngo_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ngo_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `link` varchar(300) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ngo_notification_user_id_c245cefb_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `ngo_notification_user_id_c245cefb_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ngo_notification`
--

LOCK TABLES `ngo_notification` WRITE;
/*!40000 ALTER TABLE `ngo_notification` DISABLE KEYS */;
INSERT INTO `ngo_notification` VALUES (1,'Donation Picked Up','Your donation \"Rice Sacks\" has been picked up by volunteer John.',0,'2026-03-26 03:34:12.649000','/donor/my-donations/',11),(2,'Donation Delivered','Your donation \"Dal\" was successfully delivered to Hope Foundation.',0,'2026-03-26 03:34:12.693000','/donor/my-donations/',11),(3,'Donation Pledged','Your pledge for \"Warm Blankets\" has been registered. An NGO representative will approve it soon.',0,'2026-03-26 03:34:12.730000','/donor/my-donations/',12),(4,'New Pledge Received','Bob pledged 5 pieces of Warm Blankets.',0,'2026-03-26 03:34:12.771000','/ngo/donation-management/',13),(5,'Successful Delivery','Volunteer John delivered Dal.',0,'2026-03-26 03:34:12.817000','/ngo/dashboard/',13),(6,'Profile Approved','Your NGO profile has been approved! You can now receive donations.',0,'2026-03-26 03:34:12.858000','/ngo/dashboard/',14),(7,'New Assignment','You have been assigned to pick up Rice Sacks.',0,'2026-03-26 03:34:12.901000','/volunteer/tasks/',15),(8,'Task Completed','You successfully delivered Dal. Great job!',0,'2026-03-26 03:34:12.927000','/volunteer/history/',15),(9,'Welcome Volunteer','Welcome to AidBridge! Browse tasks near you to get started.',0,'2026-03-26 03:34:12.951000','/volunteer/browse-tasks/',16),(10,'New Donation Pledged','Donor Nithya pledged 50 Note Books.',1,'2026-03-26 03:45:33.790000','/ngo/donation-management/',17),(11,'Items Delivered','Volunteer Preethi successfully delivered Kids Clothes.',1,'2026-03-26 03:45:33.798000','/ngo/dashboard/',17),(12,'Donation Picked Up','Your Wheat Flour donation has been collected by Volunteer Preethi.',1,'2026-03-26 03:45:33.803000','/donor/my-donations/',18),(13,'Donation Reached NGO','Thank you! Your donation of Kids Clothes has reached ABC Foundations safely.',1,'2026-03-26 03:45:33.810000','/donor/my-donations/',18),(14,'Pledge Registered','Your pledge for Note Books has been registered successfully.',1,'2026-03-26 03:45:33.816000','/donor/my-donations/',18),(15,'New Item to Pick Up','You are assigned to pick up Wheat Flour from Nithya.',1,'2026-03-26 03:45:33.821000','/volunteer/tasks/',19),(16,'Delivery Confirmed','The NGO confirmed your delivery of Kids Clothes. Great work!',1,'2026-03-26 03:45:33.827000','/volunteer/history/',19),(17,'New Pledge Received','Nithya pledged 10 packs of First Aid Kits.',1,'2026-03-26 04:27:24.124000','/ngo/donation-management/',17),(18,'Donation Picked Up','Your First Aid Kits have been picked up!',1,'2026-03-26 04:27:24.826000','/donor/my-donations/',18),(19,'Items Delivered','Volunteer Preethi successfully delivered First Aid Kits.',1,'2026-03-26 04:27:25.788000','/ngo/dashboard/',17),(20,'? Donation Completed!','Your donation of First Aid Kits has been successfully delivered and confirmed!',1,'2026-03-26 04:37:39.337000','/donor/my-donations/',18),(21,'Task Completed!','Your delivery task for First Aid Kits has been confirmed. Thank you!',1,'2026-03-26 04:37:40.471000','/volunteer/tasks/',19),(22,'New Donation Received!','Nithya S pledged 10 packs of Emergency First Aid Kits.',1,'2026-03-26 06:20:14.150000','/ngo/donation-management/',17),(23,'New Donation Received!','Nithya S pledged 5 packs of Emergency First Aid Kits.',1,'2026-03-26 09:20:41.040000','/ngo/donation-management/',17),(24,'Donation Approved!','Your donation of 5.00 packs of Emergency First Aid Kits has been approved by ABC Foundations.',1,'2026-03-26 09:41:34.524000','/donor/my-donations/',18),(25,'Donation Approved!','Your donation of 10.00 packs of Emergency First Aid Kits has been approved by ABC Foundations.',1,'2026-03-26 09:41:55.816000','/donor/my-donations/',18),(26,'New Delivery Task!','You have been assigned to deliver Emergency First Aid Kits for ABC Foundations.',1,'2026-03-26 09:42:37.234000','/volunteer/tasks/',19),(27,'? Donation Completed!','Your donation of Used but clean clothes has been successfully delivered and confirmed!',1,'2026-03-26 09:44:05.424000','/donor/my-donations/',18),(28,'Task Completed!','Your delivery task for Used but clean clothes has been confirmed. Thank you!',1,'2026-03-26 09:44:05.508000','/volunteer/tasks/',19),(29,'New Donation Received!','Nithya S pledged 4 pieces of Kids Clothes.',0,'2026-03-26 09:46:33.106000','/ngo/donation-management/',17);
/*!40000 ALTER TABLE `ngo_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ngo_volunteerassignment`
--

DROP TABLE IF EXISTS `ngo_volunteerassignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ngo_volunteerassignment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) NOT NULL,
  `pickup_location` varchar(300) NOT NULL,
  `delivery_location` varchar(300) NOT NULL,
  `proof_image` varchar(100) DEFAULT NULL,
  `notes` longtext NOT NULL,
  `assigned_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `donation_id` bigint NOT NULL,
  `ngo_id` bigint NOT NULL,
  `volunteer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `donation_id` (`donation_id`),
  KEY `ngo_volunteerassignment_ngo_id_1023f7ad_fk_accounts_user_id` (`ngo_id`),
  KEY `ngo_volunteerassignm_volunteer_id_8b19608c_fk_accounts_` (`volunteer_id`),
  CONSTRAINT `ngo_volunteerassignm_volunteer_id_8b19608c_fk_accounts_` FOREIGN KEY (`volunteer_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `ngo_volunteerassignment_donation_id_bb24b4d4_fk_ngo_donation_id` FOREIGN KEY (`donation_id`) REFERENCES `ngo_donation` (`id`),
  CONSTRAINT `ngo_volunteerassignment_ngo_id_1023f7ad_fk_accounts_user_id` FOREIGN KEY (`ngo_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ngo_volunteerassignment`
--

LOCK TABLES `ngo_volunteerassignment` WRITE;
/*!40000 ALTER TABLE `ngo_volunteerassignment` DISABLE KEYS */;
INSERT INTO `ngo_volunteerassignment` VALUES (1,'picked_up','Uptown NY','123 Main St','','','2026-03-26 03:34:11.795000','2026-03-26 03:34:11.795000',4,13,15),(2,'delivered','Downtown NY','123 Main St','','','2026-03-26 03:34:12.603000','2026-03-26 03:34:12.603000',6,13,15),(3,'picked_up','Karur Main','Salem Hub','','Met donor at main junction.','2026-03-26 03:45:33.776000','2026-03-26 03:45:33.776000',7,17,19),(4,'completed','Karur Main','Salem Hub','','Delivered successfully.','2026-03-26 03:45:33.784000','2026-03-26 09:44:05.094000',8,17,19),(5,'completed','Karur Main','Main Hospital Road','','Delivered safely to NGO.','2026-03-26 04:27:24.712000','2026-03-26 04:37:37.600000',10,17,19),(6,'assigned','Karur','Salem','','','2026-03-26 09:42:36.905000','2026-03-26 09:42:36.912000',12,17,19);
/*!40000 ALTER TABLE `ngo_volunteerassignment` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-26 22:36:23
