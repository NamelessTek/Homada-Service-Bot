SET NAMES utf8;

DROP TABLE IF EXISTS `Admin`;

CREATE TABLE
    `Admin` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Name` text NOT NULL,
        `Phone` text NOT NULL,
        `Email` text NOT NULL,
        `Creation_date` datetime NOT NULL,
        `Last_update` timestamp NOT NULL,
        `Status` tinyint(4) NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;

INSERT INTO
    `Admin` (
        `ID`,
        `Name`,
        `Phone`,
        `Email`,
        `Creation_date`,
        `Last_update`,
        `Status`
    )
VALUES (
        1,
        'Luis Cedillo',
        '+5215571967146',
        'luis.cedillo.maldonado@gmail.com',
        '2022-11-07 21:14:59',
        '2022-11-07 21:14:59',
        1
    ), (
        2,
        'Raul Gómez',
        '+5215554060855',
        'raul.gomez@gmail.com',
        '2022-11-07 21:15:42',
        '2022-11-07 21:15:42',
        1
    );