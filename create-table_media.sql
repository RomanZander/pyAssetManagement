-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.5.27 - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL version:             7.0.0.4053
-- Date/time:                    2012-09-25 01:45:41
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
  `path` text NOT NULL COMMENT 'media location path',
  `name` text NOT NULL COMMENT 'media name representation',
  `type` enum('File','Sequence') NOT NULL,
  `size` bigint(20) unsigned DEFAULT NULL COMMENT 'media size in bytes',
  `mtime` bigint(20) unsigned DEFAULT NULL COMMENT 'media modification time',
  `thumb` mediumblob COMMENT 'media thumbnail (PNG embedded in BLOB)',
  `comment` text COMMENT 'media user comment (text)',
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'record update timestamp',
  UNIQUE KEY `pathname_UNIQUE` (`name`(255),`path`(255)),
  KEY `type_KEY` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table test.media: ~6 rows (approximately)
/*!40000 ALTER TABLE `media` DISABLE KEYS */;
INSERT INTO `media` (`path`, `name`, `type`, `size`, `mtime`, `thumb`, `comment`, `updated`) VALUES
	('D:\\dev.Git\\pyAssetManagement\\test1', 'test-0-mediaFile.mov', 'File', 128, 1345979021, NULL, NULL, '2012-09-25 01:25:19'),
	('D:\\dev.Git\\pyAssetManagement\\test1', 'test-3-mediaFile.mov', 'File', 124, 1345979022, NULL, NULL, '2012-09-25 01:25:19'),
	('D:\\dev.Git\\pyAssetManagement\\test2', 'test-13-mediaFile.mov', 'File', 3, 1345979090, NULL, NULL, '2012-09-25 01:33:45'),
	('D:\\dev.Git\\pyAssetManagement\\test2', 'test-1-mediaFile.mov', 'File', 3, 1345979090, NULL, NULL, '2012-09-25 01:44:59'),
	('D:\\dev.Git\\pyAssetManagement\\test2', 'test-2-mediaFile.MOV', 'File', 3, 1345979090, NULL, NULL, '2012-09-25 01:44:59'),
	('D:\\dev.Git\\pyAssetManagement\\test2', 'test-0-mediaFile.mov', 'File', 3, 1345979090, NULL, NULL, '2012-09-25 01:44:20');
/*!40000 ALTER TABLE `media` ENABLE KEYS */;
/*!40014 SET FOREIGN_KEY_CHECKS=1 */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
