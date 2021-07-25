CREATE TABLE `stock` (
  `ts_code` varchar(50) NOT NULL COMMENT 'ts_code',
  `symbol` varchar(50) NOT NULL COMMENT '代码',
  `name` varchar(50) NOT NULL COMMENT '名称',
  `area` varchar(500) DEFAULT NULL COMMENT '地域',
  `industry` varchar(50) DEFAULT NULL COMMENT '行业',
  `list_date` varchar(50) DEFAULT NULL COMMENT '上市时间',
  PRIMARY KEY (`ts_code`,`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票信息';


CREATE TABLE `stock_history` (
  `date` varchar(50) NOT NULL COMMENT '日期',
  `symbol` varchar(50) NOT NULL COMMENT '代码',
  `name` varchar(50) NOT NULL COMMENT '名称',
  `current` decimal(11,4) DEFAULT NULL COMMENT '现价',
  `percent` decimal(11,4) DEFAULT NULL COMMENT '涨幅',
  `amplitude` decimal(11,4) DEFAULT NULL COMMENT '振幅',
  `amount` decimal(11,4) DEFAULT NULL COMMENT '成交额',
  `volume_ratio` decimal(11,4) DEFAULT NULL COMMENT '量比',
  `turnover_rate` decimal(11,4) DEFAULT NULL COMMENT '换手',
  `market_capital` decimal(11,4) DEFAULT NULL COMMENT '市值',
  `current_year_percent` decimal(11,4) DEFAULT NULL COMMENT '年初至今',
  PRIMARY KEY (`date`,`symbol`),
  KEY `date` (`date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票历史记录';

