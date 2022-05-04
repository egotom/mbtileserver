-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        10.6.5-MariaDB - mariadb.org binary distribution
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 导出 mapbox 的数据库结构
DROP DATABASE IF EXISTS `mapbox`;
CREATE DATABASE IF NOT EXISTS `mapbox` /*!40100 DEFAULT CHARACTER SET utf8mb3 */;
USE `mapbox`;

-- 导出  表 mapbox.file_alias 结构
DROP TABLE IF EXISTS `file_alias`;
CREATE TABLE IF NOT EXISTS `file_alias` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fn_id` int(10) unsigned DEFAULT NULL,
  `alias` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fn` (`fn_id`),
  CONSTRAINT `fn` FOREIGN KEY (`fn_id`) REFERENCES `file_name` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1181 DEFAULT CHARSET=utf8mb3;

-- 正在导出表  mapbox.file_alias 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `file_alias` DISABLE KEYS */;
/*!40000 ALTER TABLE `file_alias` ENABLE KEYS */;

-- 导出  表 mapbox.file_name 结构
DROP TABLE IF EXISTS `file_name`;
CREATE TABLE IF NOT EXISTS `file_name` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fs` int(10) unsigned DEFAULT NULL,
  `fn` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8mb3;

-- 正在导出表  mapbox.file_name 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `file_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `file_name` ENABLE KEYS */;

-- 导出  表 mapbox.info 结构
DROP TABLE IF EXISTS `info`;
CREATE TABLE IF NOT EXISTS `info` (
  `z` int(10) unsigned DEFAULT NULL,
  `x` int(10) unsigned DEFAULT NULL,
  `y` int(10) unsigned DEFAULT NULL,
  `url` text DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 正在导出表  mapbox.info 的数据：~1 rows (大约)
/*!40000 ALTER TABLE `info` DISABLE KEYS */;
INSERT INTO `info` (`z`, `x`, `y`, `url`, `name`) VALUES
	(15, 32767, 29287, 'https://b.tiles.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token={}', 'mapbox');
/*!40000 ALTER TABLE `info` ENABLE KEYS */;

-- 导出  表 mapbox.progress 结构
DROP TABLE IF EXISTS `progress`;
CREATE TABLE IF NOT EXISTS `progress` (
  `done` enum('Y','N') DEFAULT NULL,
  `z` int(10) unsigned NOT NULL,
  `x` int(10) unsigned NOT NULL,
  `y` int(10) unsigned DEFAULT NULL,
  `worker_mac` bigint(20) unsigned DEFAULT NULL,
  `create_at` datetime NOT NULL,
  `update_at` datetime NOT NULL,
  KEY `row` (`x`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 正在导出表  mapbox.progress 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `progress` DISABLE KEYS */;
/*!40000 ALTER TABLE `progress` ENABLE KEYS */;

-- 导出  表 mapbox.worker 结构
DROP TABLE IF EXISTS `worker`;
CREATE TABLE IF NOT EXISTS `worker` (
  `mac` bigint(20) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `mapbox_token` text DEFAULT NULL,
  `url` text DEFAULT NULL,
  `create_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 正在导出表  mapbox.worker 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `worker` DISABLE KEYS */;
/*!40000 ALTER TABLE `worker` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
