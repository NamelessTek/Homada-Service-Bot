SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `Questions`;

CREATE TABLE
    `Questions` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Question` varchar(250) NOT NULL,
        `Type_Question` varchar(50) NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;

INSERT INTO
    `Questions` (
        `ID`,
        `Question`,
        `Type_Question`
    )
VALUES (
        1,
        '¿Cuál es el teléfono del cliente?',
        'Reserva'
    ), (
        2,
        '¿Cuál es el nombre del cliente?',
        'Reserva'
    ), (
        3,
        '¿Cuál es el email del cliente, en caso de no tenerlo escribir "no"?',
        'Reserva'
    ), (
        4,
        '¿Cuál es el número de reservación del cliente?',
        'Reserva'
    ), (
        5,
        '¿Cuál es el dí­a de llegada del cliente? Formato dia-mes-año',
        'Reserva'
    ), (
        6,
        '¿Cuál es el día de salida del cliente? Formato dia-mes-año',
        'Reserva'
    ), (
        7,
        '¿Cuál es la ubicación en la que se hospedara el cliente?',
        'Reserva'
    ), (
        8,
        '¿Cuál es el número de la reserva?',
        'Cancelacion'
    ), (
        9,
        'Por favor envíe tu constancia fiscal en formato pdf.',
        'Factura'
    ), (
        10,
        'Ingrese el correo electrónico al que desee recibir la factura',
        'Factura'
    );