SET NAMES utf8;

DROP TABLE IF EXISTS `Uploads`;

CREATE TABLE
    `Uploads` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `URL` text NOT NULL,
        `File_name` text NOT NULL,
        `Document` text NOT NULL,
        `Status` tinyint(4) NOT NULL,
        `Creation_date` datetime NOT NULL,
        `Last_update` timestamp NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = latin1;