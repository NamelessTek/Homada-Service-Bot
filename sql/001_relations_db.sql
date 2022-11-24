-- Adminer 4.8.1 MySQL 5.7.40 dump

SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `Relation_booking_document_table`;

CREATE TABLE
    `Relation_booking_document_table` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Upload_id` int(11) NOT NULL,
        `Booking_id` int(11) NOT NULL,
        PRIMARY KEY (`ID`),
        KEY `Upload_id` (`Upload_id`),
        KEY `Cliente_id` (`Booking_id`),
        CONSTRAINT `Relation_client_document_table_ibfk_1` FOREIGN KEY (`Upload_id`) REFERENCES `Uploads` (`ID`),
        CONSTRAINT `Relation_client_document_table_ibfk_2` FOREIGN KEY (`Booking_id`) REFERENCES `Booking` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = latin1;