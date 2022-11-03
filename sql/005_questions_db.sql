DROP TABLE IF EXISTS `Questions`;
CREATE TABLE `Questions` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Question` varchar(250) NOT NULL,
  `Type_Question` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `Questions` (`ID`, `Question`, `Type_Question`) VALUES
(1,	'¿Cuál es el nombre del cliente?',	'Reserva'),
(2,	' ¿Cuál es el teléfono del cliente?',	'Reserva'),
(3,	'¿Cuál es el email del cliente?',	'Reserva'),
(4,	'¿Cuál es el número de reservación del cliente?',	'Reserva'),
(5,	'¿Cuál es el día de llegada del cliente?',	'Reserva'),
(6,	'¿Cuál es el día de salida del cliente?',	'Reserva'),
(7,	'¿Cuál es la ubicación en la que se hospedara el cliente?',	'Reserva');