-- Adminer 4.8.1 MySQL 5.7.39 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `Admin`;
CREATE TABLE `Admin` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` text NOT NULL,
  `Phone` text NOT NULL,
  `Email` text NOT NULL,
  `Creation_date` datetime NOT NULL,
  `Last_update` timestamp NOT NULL,
  `Status` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Booking`;
CREATE TABLE `Booking` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Booking_number` text NOT NULL,
  `Arrival` date NOT NULL,
  `Arrival_time` time NOT NULL,
  `Departure` date NOT NULL,
  `Departure_time` time NOT NULL,
  `Ubicacion_id` int(11) NOT NULL,
  `Cliente_id` int(11) NOT NULL,
  `Creation_date` datetime NOT NULL,
  `Last_update` timestamp NOT NULL,
  `Status` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Ubicacion` (`Ubicacion_id`),
  KEY `Cliente` (`Cliente_id`),
  CONSTRAINT `Booking_ibfk_1` FOREIGN KEY (`Ubicacion_id`) REFERENCES `Ubicacion` (`ID`),
  CONSTRAINT `Booking_ibfk_2` FOREIGN KEY (`Cliente_id`) REFERENCES `Client` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Client`;
CREATE TABLE `Client` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` text NOT NULL,
  `Phone` text NOT NULL,
  `Email` text NOT NULL,
  `Status` int(11) NOT NULL,
  `Creation_date` date NOT NULL,
  `Last_update` timestamp NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Option`;
CREATE TABLE `Option` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Option` int(11) NOT NULL,
  `Value` text NOT NULL,
  `Creation_date` date NOT NULL,
  `Last_update` timestamp NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Relation_table_client_booking`;
CREATE TABLE `Relation_table_client_booking` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Client_id` int(11) NOT NULL,
  `Booking_id` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `client_id` (`Client_id`),
  KEY `booking_id` (`Booking_id`),
  CONSTRAINT `Relation_table_client_booking_ibfk_1` FOREIGN KEY (`Client_id`) REFERENCES `Client` (`ID`),
  CONSTRAINT `Relation_table_client_booking_ibfk_2` FOREIGN KEY (`Booking_id`) REFERENCES `Booking` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Ubicacion`;
CREATE TABLE `Ubicacion` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Ubicacion` text NOT NULL,
  `URL` text NOT NULL,
  `Direccion` text NOT NULL,
  `SSID` text,
  `Modem` text,
  `Clave` text,
  `Mascotas` int(1) DEFAULT NULL,
  `Status` int(1) DEFAULT NULL,
  `Option` int(1) DEFAULT NULL,
  `Creation_date` datetime NOT NULL,
  `Last_update` timestamp NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 2022-11-08 00:45:09