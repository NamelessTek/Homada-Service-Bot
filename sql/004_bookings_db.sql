SET NAMES utf8;

DROP TABLE IF EXISTS `Booking`;

CREATE TABLE
    `Booking` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Booking_number` text NOT NULL,
        `Arrival` date NOT NULL,
        `Departure` date NOT NULL,
        `Ubicacion_id` int(11) NOT NULL,
        `Cliente_id` int(11) NOT NULL,
        `Arrival_time` time NOT NULL,
        `Departure_time` time NOT NULL,
        `Creation_date` datetime NOT NULL,
        `Last_update` timestamp NOT NULL,
        `Status` tinyint(4) NOT NULL,
        PRIMARY KEY (`ID`),
        KEY `Ubicacion` (`Ubicacion_id`),
        KEY `Cliente` (`Cliente_id`),
        CONSTRAINT `Booking_ibfk_1` FOREIGN KEY (`Ubicacion_id`) REFERENCES `Ubicacion` (`ID`),
        CONSTRAINT `Booking_ibfk_2` FOREIGN KEY (`Cliente_id`) REFERENCES `Client` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;