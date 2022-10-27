SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP DATABASE IF EXISTS `Homada_DB`;

CREATE DATABASE
    IF NOT EXISTS `Homada_DB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `Homada_DB`;

DROP TABLE IF EXISTS `User`;

CREATE TABLE
    `User` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Username` text NOT NULL,
        `Email` text NOT NULL,
        `Phone` text NOT NULL,
        `Status` text NOT NULL,
        `Creation_date` datetime NOT NULL,
        `Last_update` timestamp NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;

DROP TABLE IF EXISTS `Ubicacion`;

CREATE TABLE
    `Ubicacion` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Ubicacion` text NOT NULL,
        `URL` text NOT NULL,
        `Direccion` text NOT NULL,
        `SSID` text,
        `Modem` text,
        `Clave` text,
        `Mascotas` INT(1) NULL,
        `Status` INT(1) NULL,
        `Option` INT(1) NULL,
        `Creation_date` datetime NOT NULL,
        `Last_update` timestamp NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `Option`;

CREATE TABLE
    `Option` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Option` int(11) NOT NULL,
        `Value` text NOT NULL,
        `Creation_date` date NOT NULL,
        `Last_update` timestamp NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;

DROP TABLE IF EXISTS `Client`;

DROP TABLE IF EXISTS `Client`;

CREATE TABLE
    `Client` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Name` text NOT NULL,
        `Last_name` text NOT NULL,
        `Phone` text NOT NULL,
        `Email` text NOT NULL,
        `Status` int(11) NOT NULL,
        `Creation_date` date NOT NULL,
        `Last_update` timestamp NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;

DROP TABLE IF EXISTS `Booking`;

CREATE TABLE
    `Booking` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Booking_number` text NOT NULL,
        `Arrival` date NOT NULL,
        `Arrival_time` time NOT NULL,
        `Departure` date NOT NULL,
        `Departure_time` time NOT NULL,
        `Ubicacion` int(11) NOT NULL,
        `Cliente` int(11) NOT NULL,
        `Creation_date` datetime NOT NULL,
        `Last_update` timestamp NOT NULL,
        `Status` int(11) NOT NULL,
        PRIMARY KEY (`ID`),
        KEY `Ubicacion` (`Ubicacion`),
        KEY `Cliente` (`Cliente`),
        CONSTRAINT `Booking_ibfk_1` FOREIGN KEY (`Ubicacion`) REFERENCES `Ubicacion` (`ID`),
        CONSTRAINT `Booking_ibfk_2` FOREIGN KEY (`Cliente`) REFERENCES `Client` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;