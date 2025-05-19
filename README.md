# ProjectBlog
Это первый pet-проект

сделать копию БД:
pg_dump -U username -h host -p port -Fc dbname > backup.dump
восстановить БД:
pg_restore -U username -h host -p port -d dbname --clean --if-exists backup.dump