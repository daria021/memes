Перед запуском необходимо выполнить следующие операции:

1. Заполнить файл private/.env по примеру из private/example.env, поля access_key и secret_key заполните любым символом
2. Запустите MinIO с помощью следующей команды: `docker compose up --build minio`
3. Пройдите по ссылке http://localhost:9001/, войдите в локальный аккаунт, используя информацию из private/.env
4. Получите Access Key и Secret Key и заполните ими private/.env
5. Заполните public/.env по примеру из public/example.env
6. Перезапустите проект: `docker compose up --build`