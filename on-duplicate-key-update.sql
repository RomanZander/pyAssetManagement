INSERT INTO `media` (`path`,`name`,`size`) VALUES 
 ('D:\\1','a333',111)
ON DUPLICATE KEY UPDATE 
`size` = VALUES(`size`),
`name` = VALUES(`name`)
;

