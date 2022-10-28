DROP TABLE IF EXISTS `Relation_table_client_booking`;

CREATE TABLE
    `Relation_table_client_booking` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Client_id` int(11) NOT NULL,
        `Booking_id` int(11) NOT NULL,
        PRIMARY KEY (`ID`),
        KEY `client_id` (`Client_id`),
        KEY `booking_id` (`Booking_id`),
        CONSTRAINT `Relation_table_client_booking_ibfk_1` FOREIGN KEY (`Client_id`) REFERENCES `Client` (`ID`),
        CONSTRAINT `Relation_table_client_booking_ibfk_2` FOREIGN KEY (`Booking_id`) REFERENCES `Booking` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;