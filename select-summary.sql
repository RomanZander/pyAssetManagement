select 
t1.path as path1, t1.name as name1, t1.size as size1,
t2.path as path, t2.name as name, t2.size as size, t2.mtime as mtime, t2.updated #, sum(t2.size) as sumsize
FROM test.mediatest t1, test.mediatest t2
where 
(t2.path like concat(t1.path, '/%')) or
((t2.path = t1.path) and (t2.name = t1.name))
#GROUP by path1
ORDER by path1





