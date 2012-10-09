select 
t1.path as path1, t1.name as name1,
t2.path as path, t2.name as name, t2.size as size, sum(t2.size) as sumsize, max(t2.mtime) as maxmtime, max(t2.updated) as maxupdated
FROM test.mediatest t1, test.mediatest t2
where 
(t2.path like concat(t1.path, '/%')) or
((t2.path = t1.path) and (t2.name = t1.name))
GROUP by path1;
