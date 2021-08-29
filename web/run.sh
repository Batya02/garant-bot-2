id=$(pidof -s python3);

sudo kill -9 $id;

python3 manage.py runserver