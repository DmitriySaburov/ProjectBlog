# ProjectBlog
Это pet-проект blog

создать виртуальное окружение .venvProjectBlog
установить библиотеки из requirements.txt
pip install -r requirements.txt
для создания: pip freeze > requirements.txt


сделать копию БД:
pg_dump -U username -h host -p port -Fc dbname > backup.dump
восстановить БД:
pg_restore -U username -h host -p port -d dbname --clean --if-exists backup.dump