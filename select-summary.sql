select #DISTINCT
path, sum(size) as sumsize, max(mtime) as maxmtime, max(updated) as maxupdated
FROM media
GROUP by path;
