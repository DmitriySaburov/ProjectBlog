# ProjectBlog
Это pet-проект blog

создать виртуальное окружение .venvProjectBlog
установить библиотеки из requirements.txt
pip install -r requirements.txt
для создания: pip freeze > requirements.txt


сделать копию БД:
pg_dump -U username -h host -p port -Fc dbname > backup.dump
pg_dump -U blog -h 127.0.0.1 -p 5432 -Fc blog > backup.dump
восстановить БД:
pg_restore -U username -h host -p port -d dbname --clean --if-exists backup.dump
pg_restore -U blog -h 127.0.0.1 -p 5432 -d blog --clean --if-exists backup.dump