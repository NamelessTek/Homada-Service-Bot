SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';


DROP DATABASE IF EXISTS `Homada_DB`;
CREATE DATABASE IF NOT EXISTS `Homada_DB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `Homada_DB`;

DROP TABLE IF EXISTS `Ubicacion`;
CREATE TABLE `Ubicacion` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Ubicacion` text COLLATE latin1_spanish_ci NOT NULL,
  `URL` text COLLATE latin1_spanish_ci NOT NULL,
  `Direccion` text COLLATE latin1_spanish_ci NOT NULL,
  `SSID` text COLLATE latin1_spanish_ci,
  `Clave` int(11) DEFAULT NULL,
  `Mascotas` bit(1) NOT NULL,
  `status` bit(1) NOT NULL,
  `Creation_date` datetime NOT NULL,
  `Last_update` timestamp NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
