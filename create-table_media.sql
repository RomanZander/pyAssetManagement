-- --------------------------------------------------------
-- Host:                         mysql
-- Server version:               5.1.61 - Source distribution
-- Server OS:                    redhat-linux-gnu
-- HeidiSQL version:             7.0.0.4053
-- Date/time:                    2012-09-24 18:31:57
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;

-- Dumping database structure for test
DROP DATABASE IF EXISTS `test`;
CREATE DATABASE IF NOT EXISTS `test` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `test`;


-- Dumping structure for table test.media
DROP TABLE IF EXISTS `media`;
CREATE TABLE IF NOT EXISTS `media` (
  `path` text COMMENT 'media location path',
  `name` text NOT NULL COMMENT 'media name representation',
  `type` enum('File','Sequence') DEFAULT NULL,
  `size` bigint(20) unsigned DEFAULT NULL COMMENT 'media size in bytes',
  `mtime` bigint(20) unsigned DEFAULT NULL COMMENT 'media modification time',
  `thumb` mediumblob COMMENT 'media thumbnail (PNG embedded in BLOB)',
  `comment` text COMMENT 'media user comment (text)',
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'record update timestamp',
  UNIQUE KEY `name_UNIQUE` (`name`(255)),
  KEY `type_KEY` (`type`),
  KEY `path_KEY` (`path`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table test.media: ~2 rows (approximately)
/*!40000 ALTER TABLE `media` DISABLE KEYS */;
REPLACE INTO `media` (`path`, `name`, `type`, `size`, `mtime`, `thumb`, `comment`, `updated`) VALUES
	('D:\\dev.Git\\pyAssetManagement\\test1', 'test-0-mediaFile.mov', 'File', 10, 1345979021, NULL, 'custom', '2012-09-24 15:42:10'),
	('D:\\dev.Git\\pyAssetManagement\\test1', 'test-1-mediaFile.mov', 'File', 10, 1345979021, NULL, NULL, '2012-09-24 15:58:48');
/*!40000 ALTER TABLE `media` ENABLE KEYS */;
/*!40014 SET FOREIGN_KEY_CHECKS=1 */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
