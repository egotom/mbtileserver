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


-- 导出 bing2 的数据库结构
DROP DATABASE IF EXISTS `bing2`;
CREATE DATABASE IF NOT EXISTS `bing2` /*!40100 DEFAULT CHARACTER SET utf8mb3 */;
USE `bing2`;

-- 导出  表 bing2.error 结构
DROP TABLE IF EXISTS `error`;
CREATE TABLE IF NOT EXISTS `error` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `z` int(10) unsigned DEFAULT NULL,
  `x` int(10) unsigned DEFAULT NULL,
  `y` int(10) unsigned DEFAULT NULL,
  `quad` bigint(20) unsigned NOT NULL,
  `status_code` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52030 DEFAULT CHARSET=utf8mb3;

-- 正在导出表  bing2.error 的数据：~0 rows (大约)
DELETE FROM `error`;
/*!40000 ALTER TABLE `error` DISABLE KEYS */;
/*!40000 ALTER TABLE `error` ENABLE KEYS */;

-- 导出  表 bing2.info 结构
DROP TABLE IF EXISTS `info`;
CREATE TABLE IF NOT EXISTS `info` (
  `z` varchar(50) DEFAULT NULL,
  `p` varchar(50) DEFAULT NULL,
  `p2` varchar(50) DEFAULT NULL,
  `url` text DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `info` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 正在导出表  bing2.info 的数据：~100 rows (大约)
DELETE FROM `info`;
/*!40000 ALTER TABLE `info` DISABLE KEYS */;
INSERT INTO `info` (`z`, `p`, `p2`, `url`, `name`, `info`) VALUES
	('13,18', '116.0959,40.0000', '116.3500,39.4459', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,北京市'),
	('13,18', '121.0959,31.2002', '121.4003,31.0003', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,上海市'),
	('13,18', '114.0458,22.3101', '113.5000,22.3501', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,深圳市'),
	('13,18', '113.1300,23.1001', '113.2059,23.0300', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,广州市'),
	('13,18', '119.5959,30.2504', '120.1957,30.1001', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,杭州市'),
	('13,18', '118.3500,32.1000', '118.5500,31.5000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,南京市'),
	('13,18', '120.3000,31.1500', '120.4500,31.1500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,苏州市'),
	('13,18', '103.5000,30.5000', '104.1500,30.3000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,成都市'),
	('13,18', '114.0000,35.4500', '114.3000,30.3000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,武汉市'),
	('13,18', '120.2400,31.2800', '120.1400,31.3400', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,无锡市'),
	('13,18', '106.1500,29.4000', '106.4500,29.1500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,重庆市'),
	('13,18', '112.4500,28.2000', '113.1000,28.0500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,长沙市'),
	('13,18', '116.5959,39.1500', '117.3000,38.4501', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,天津市'),
	('13,18', '113.3000,34.5000', '113.5000,34.3500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,郑州市'),
	('13,18', '117.0006,36.4519', '117.1457,36.3019', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,济南市'),
	('13,18', '121.1500,30.0000', '121.4500,29.4500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,宁波市'),
	('13,18', '108.4958,34.2004', '109.0459,34.0959', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,西安市'),
	('13,18', '120.1458,36.1507', '120.3954,36.0010', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,青岛市'),
	('13,18', '117.0500,32.0000', '117.3000,31.4000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,合肥市'),
	('13,18', '119.0000,26.1500', '119.3000,25.4500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,福州市'),
	('13,18', '113.1000,22.5500', '113.0000,23.1000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,佛山市'),
	('13,18', '121.3000,39.0000', '121.4500,38.5000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,大连市'),
	('13,18', '123.1000,42.0000', '123.3500,41.4000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,沈阳市'),
	('13,18', '118.0300,24.3300', '118.1200,24.2500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,厦门市'),
	('13,18', '102.3500,25.0000', '102.5500,24.5000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,昆明市'),
	('13,18', '114.1459,38.1504', '114.4500,37.4500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,石家庄市'),
	('13,18', '126.3000,46.0002', '126.4456,45.3008', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,哈尔滨市'),
	('13,18', '113.3300,23.0400', '114.000,22.5000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,东莞市'),
	('13,18', '125.1000,45.0500', '125.2400,43.4500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,长春市'),
	('13,18', '112.2500,38.0000', '112.4000,37.4500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,太原市'),
	('13,18', '120.3000,37.3000', '121.3000,37.0000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,烟台市'),
	('13,18', '115.4000,28.5000', '116.0400,28.3000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,南昌市'),
	('13,18', '118.3800,24.5400', '118.4100,24.5100', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,泉州市'),
	('13,18', '106.3000,26.5000', '106.5000,26.2500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,贵阳市'),
	('13,18', '120.3000,28.1000', '120.5000,27.5000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,温州市'),
	('13,18', '87.1900,44.0000', '87.4500,43.4000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,乌鲁木齐市'),
	('13,18', '119.2000,32.3000', '119.3500,32.2000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,扬州市'),
	('13,18', '111.3000,40.5500', '111.4900,40.4500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,呼和浩特市'),
	('13,18', '90.5200,29.4300', '91.1400,29.3500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,拉萨市'),
	('13,18', '90.5500,29.4500', '104.0000,35.5800', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,兰州市'),
	('13,18', '110.1300,20.0100', '110.0900,20.0400', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,海口市'),
	('13,18', '101.3900,36.40000', '101.5400,36.3300', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,西宁市'),
	('13,18', '108.1000,22.5500', '108.3000,22.4500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,南宁市'),
	('13,18', '113.5000,22.3344', '114.2500,22.1000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '中国,香港'),
	('13,18', '125.4100,39.0500', '125.4900,38.5800', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '朝鲜民主主义人民共和国,平壤'),
	('13,18', '126.5400,37.3900', '127.0700,37.2800', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '大韩民国,首尔'),
	('13,18', '144.4500,-37.4000', '145.1500,-38.0000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '澳大利亚,墨尔本'),
	('13,18', '152.5500,-27.2000', '153.2000,-27.4000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '澳大利亚,布里斯班'),
	('13,18', '150.3000,-33.3500', '151.2000,-34.0500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '澳大利亚,悉尼'),
	('13,18', '147.0915,-35.1630', '149.0815,-35.1715', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '澳大利亚,堪培拉'),
	('13,18', '-58.3000,-34.3400', '-58.20,-34.3900', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '阿根廷共和国,布宜诺斯艾利斯'),
	('13,18', '100.1941,13.4800', '100.4000,13.4000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '泰国,曼谷'),
	('13,18', '101.3600,3.1400', '101.4500,3.0317', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '马来西亚,吉隆坡'),
	('13,18', '103.4000,1.2500', '104.0000,1.1500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '新加坡共和国,新加坡'),
	('13,18', '120.5628,14.3800', '121.0000,14.3400', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '菲律宾共和国,马尼拉'),
	('13,18', '35.1100,31.4700', '35.1500,31.4400', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '巴勒斯坦国,耶路撒冷'),
	('13,18', '4.4400,52.2600', '5.0100,52.1700', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '荷兰,阿姆斯特丹'),
	('13,18', '-47.5800,-15.4400', '-47.4900,-15.5000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '巴西联邦共和国,巴西利亚'),
	('13,18', '-43.5000,-23.0500', '-43.0500,-22.4500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '巴西联邦共和国,里约热内卢'),
	('13,18', '11.2600,48.1300', '11.4100,48.0500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '德意志联邦共和国,慕尼黑'),
	('13,18', '13.1000,52.3500', '13.4000,52.2500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '德意志联邦共和国,柏林'),
	('13,18', '16.1600,48.1500', '16.2800,48.0900', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '奥地利共和国,维也纳'),
	('13,18', '-123.1300,49.1700', '-123.1300,49.1200', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '加拿大,温哥华'),
	('13,18', '-79.1800,43.3630', '-79.2600,24.5000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '加拿大,多伦多'),
	('13,18', '-74.0000,45.2500', '-73.2500,45.4500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '加拿大,蒙特利尔'),
	('13,18', '12.2800,41.5600', '12.3200,41.5200', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '意大利,罗马'),
	('13,18', '9.0700,45.3100', '9.1500,45.2600', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '意大利,米兰'),
	('13,18', '-0.1419,51.3500', '-0,51.2554', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '英国,伦敦'),
	('13,18', '2.2400,48.5000', '2.1700,48.5300', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '法国,巴黎'),
	('13,18', '30.3000,59.5000', '30.0900,60.0000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '俄罗斯,圣彼得堡'),
	('13,18', '37.5000,55.3000', '37.2400,55.5200', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '俄罗斯,莫斯科'),
	('13,18', '139.44,35.4200', '139.4700,35.4000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '日本,东京'),
	('13,18', '139.4400,35.1800', '139.2800,35.3600', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '日本,横滨'),
	('13,18', '135.2800,34.4300', '135.35,34.3516', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '日本,大阪'),
	('13,18', '54.5350,24.5434', '55.3500,25.2000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '阿联酋,迪拜'),
	('13,18', '2.0700,41.2500', '2.1200,41.2200', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '西班牙,巴塞罗那'),
	('13,18', '-3.5000,40.3000', '-3.3500,40.2000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '西班牙,马德里'),
	('13,18', '-74.1522,40.2931', '-74.4203,40.5500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '美国,纽约'),
	('13,18', '-118.1900,34.0500', '-118.1132,34.0000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '美国,洛杉矶'),
	('13,18', '-77.0711,38.5948', '-76.5700,38.5200', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '美国,华盛顿'),
	('13,18', '-87.5000,42.0000', '-87.3134,41.3841', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '美国,芝加哥'),
	('13,18', '-121.3100,37.4842', '-122.2100,37.4233', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '美国,旧金山'),
	('13,18', '-70.5500,42.1300', '-71.1200,42.2400', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '美国,波士顿'),
	('13,18', '72.4652,19.1530', '72.6000,19.0000', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '印度,孟买'),
	('13,18', '106.4000,-6.0500', '106.5900,-6.2300', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '印度,雅加达'),
	('13,18', '14.2300,57.0700', '14.3600,50.0100', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '捷克,布拉格'),
	('13,18', '105.4700,21.0300', '105.5241,20.5930', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '越南社会主义共和国,河内'),
	('13,18', '106.2000,11.1000', '107.0200,10.2200', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '越南社会主义共和国,胡志明市'),
	('13,18', '105.0000,11.4500', '104.4200,11.2500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '柬埔寨王国,金边'),
	('13,18', '95.5900,17.0600', '96.2200,16.3500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '缅甸联邦,仰光'),
	('13,18', '5.4000,50.1500', '6.3500,49.2500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '卢森堡大公国,卢森堡'),
	('13,18', '-6.2700,53.2600', '-6.0100,53.1300', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '爱尔兰,都柏林'),
	('13,18', '8.2500,47.2600', '8.3800,47.1900', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '瑞士联邦,苏黎世'),
	('13,18', '7.1700,46.5500', '7.2930,46.5930', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '瑞士联邦,伯尔尼'),
	('13,18', '30.1400,50.3600', '30.5000,50.1300', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '乌克兰,基辅'),
	('13,18', '37.2800,47.0000', '37.4200,47.1300', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '乌克兰,马里乌波尔'),
	('13,18', '4.2630,50.4730', '4.1900,50.5500', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '比利时,布鲁塞尔'),
	('13,18', '23.4100,37.5700', '23.4733,38.0200', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '希腊,雅典'),
	('13,18', '12.2700,55.4400', '12.4000,55.3700', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '丹麦,哥本哈根'),
	('13,18', '19.2000,47.2100', '18.5300,47.3700', 'https://t{}.dynamic.tiles.ditu.live.com/comp/ch/{}?mkt=zh-cn&n=z&it=A&src=o&og=503', 'bing2', '匈牙利,布达佩斯');
/*!40000 ALTER TABLE `info` ENABLE KEYS */;

-- 导出  表 bing2.progress 结构
DROP TABLE IF EXISTS `progress`;
CREATE TABLE IF NOT EXISTS `progress` (
  `done` enum('Y','N') DEFAULT NULL,
  `z` int(10) unsigned NOT NULL,
  `x` int(10) unsigned NOT NULL,
  `worker_mac` bigint(20) unsigned DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  KEY `row` (`x`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 正在导出表  bing2.progress 的数据：~0 rows (大约)
DELETE FROM `progress`;
/*!40000 ALTER TABLE `progress` DISABLE KEYS */;
/*!40000 ALTER TABLE `progress` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
