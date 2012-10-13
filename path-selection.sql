SELECT DISTINCT
t1.path as path1, t2.path, t2.name, t2.size, t2.mtime, t2.updated
FROM am_media as t1, am_media as t2
where 
(t2.path like concat(t1.path, '/', '%')) 
or
(t2.path = t1.path) 
ORDER by t1.path
#GROUP by t1.path