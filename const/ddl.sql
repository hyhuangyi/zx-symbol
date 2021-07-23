DROP TABLE IF EXISTS `stock`;
CREATE TABLE `stock` (
  `ts_code` varchar(255) DEFAULT NULL,
  `symbol` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `industry` varchar(255) DEFAULT NULL,
  `list_date` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

