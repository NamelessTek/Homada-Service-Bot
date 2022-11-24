DROP TABLE IF EXISTS `Client`;

CREATE TABLE
    `Client` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Name` text NOT NULL,
        `Phone` text NOT NULL,
        `Email` text NOT NULL,
        `Status` tinyint(4) NOT NULL,
        `Creation_date` date NOT NULL,
        `Last_update` timestamp NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;