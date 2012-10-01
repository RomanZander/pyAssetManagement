-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.5.27 - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL version:             7.0.0.4053
-- Date/time:                    2012-10-01 21:29:25
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
  `type` enum('File','Sequence') NOT NULL COMMENT 'media type',
  `size` bigint(20) unsigned DEFAULT NULL COMMENT 'media size in bytes',
  `mtime` bigint(20) unsigned DEFAULT NULL COMMENT 'media modification time',
  `thumb` mediumblob COMMENT 'media thumbnail (PNG embedded in BLOB)',
  `comment` text COMMENT 'media user comment (text)',
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'record update timestamp',
  `wtf` text COMMENT 'alarm message',
  UNIQUE KEY `pathname_UNIQUE` (`name`(255),`path`(255)),
  KEY `type_KEY` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table test.media: ~20 rows (approximately)
/*!40000 ALTER TABLE `media` DISABLE KEYS */;
INSERT INTO `media` (`path`, `name`, `type`, `size`, `mtime`, `thumb`, `comment`, `updated`, `wtf`) VALUES
	('D:dev.GitpyAssetManagement	est5проверка', '1', 'File', 100, 123456789, NULL, NULL, '2012-09-29 22:00:11', NULL),
	('D:dev.GitpyAssetManagement	est5проверка', '2', 'File', 100, 123456789, NULL, NULL, '2012-09-29 22:00:11', NULL),
	('D:dev.GitpyAssetManagement	est5проверка', '3', 'File', 100, 123456789, NULL, NULL, '2012-09-29 22:00:11', NULL),
	('D:dev.GitpyAssetManagement	est5проверка', '4', 'File', 100, 123456789, NULL, NULL, '2012-09-29 22:00:11', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test1', 'test-0-mediaFile.mov', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:23:56', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test1', 'test-1-mediaFile.Mov', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:23:56', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test1', 'test-2-mediaFile.MOV', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:23:56', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test1', 'test-3-mediaFile.ext', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:23:56', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test1', 'test-4-mediaFile.mov', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:23:56', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test3', 'subfolder', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:24:04', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test3', 'test-0-mediaFile.mov', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:24:04', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test3', 'test-1-mediaFile.Mov', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:24:04', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test3', 'test-2-mediaFile.MOV', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:24:04', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test3', 'test-3-mediaFile.ext', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:24:04', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test3', 'test-4-mediaFile.mov', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:24:04', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test4', '17. Everlast - Love, War and the Ghost of Whitey Ford - Saving Grace (Saving Grace `TV Series` OST, 2007).mp3', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:24:08', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test4', 'Copy of \'test-name\'.mov', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:24:08', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test4', 'Copy of Copy»©«¬.mov', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:24:08', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test4', 'test-name-~!@#$%^&()_+=-{}[];\'`.mov', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:24:08', NULL),
	('D:\\dev.Git\\pyAssetManagement\\test4', 'test-name-проверочное имя.mov', 'File', 100, 123456789, NULL, NULL, '2012-10-01 20:24:08', NULL);
/*!40000 ALTER TABLE `media` ENABLE KEYS */;
/*!40014 SET FOREIGN_KEY_CHECKS=1 */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
