SET @pathtofind = 'D:\\dev.Git\\pyAssetManagement\\test1';
#SELECT `path`,`name`
#FROM `media`
#WHERE 
#   (`path` = @pathtofind) OR
#   (`path` LIKE BINARY  QUOTE(@pathtofind)); # ,'\\\\%'
   
SELECT quote(QUOTE(@pathtofind));
SELECT REPLACE('\'D:\\\\dev.Git\\\\pyAssetManagement\\\\test1\'', '\'', '');
