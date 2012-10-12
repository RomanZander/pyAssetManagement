select DISTINCTROW
t1.path as path1,
t2.path as path, t2.name as name, t2.size as size, t2.mtime as maxmtime, t2.updated as maxupdated
FROM test.mediatest t1, test.mediatest t2
where 
(t2.path like concat(t1.path, '/', '%')) 
or
(t2.path = t1.path)
order by path1, name