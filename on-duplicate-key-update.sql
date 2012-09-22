INSERT INTO `media` (`name`,`size`) 
	VALUES 
   ('a055',111),
   ('a012',111)
	ON DUPLICATE KEY UPDATE `size` = VALUES(`size`);
# SELECT * FROM `media` LIMIT 0,100;
SELECT  LEFT(`path`, 256),  `name`,  `size`,  `mtime`,  LEFT(`thumb`, 256),  LEFT(`comment`, 256),  `updated` FROM `media` ORDER BY `path` ASC, `name` ASC LIMIT 1000;