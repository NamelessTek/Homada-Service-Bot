-- Adminer 4.8.1 MySQL 5.7.39 dump

SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `Admin`;

set character_set_client = 'utf8';

set character_set_connection = 'utf8';

set character_set_database = 'utf8';

set character_set_results = 'utf8';

set character_set_server = 'utf8';

CREATE TABLE
    `Option` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Option` int(11) NOT NULL,
        `Value` text NOT NULL,
        `Creation_date` date NOT NULL,
        `Last_update` timestamp NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;

-- 2022-11-08 00:45:09