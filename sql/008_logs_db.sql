DROP TABLE IF EXISTS `Log`;

CREATE TABLE
    `Log` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Type` text NOT NULL,
        `Object_id` int(11) NOT NULL,
        `Action` text NOT NULL,
        `Admin_id` int(11) NOT NULL,
        `Date` datetime NOT NULL,
        PRIMARY KEY (`ID`),
        KEY `Admin_id` (`Admin_id`),
        CONSTRAINT `Log_ibfk_1` FOREIGN KEY (`Admin_id`) REFERENCES `Admin` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = latin1;