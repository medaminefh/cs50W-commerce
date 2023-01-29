from sys import argv
from os import system

if len(argv) != 1 and argv[1] == 'dev':
    system('pip install -r requirements.txt')
    system('python3 manage.py makemigrations')
    system('python3 manage.py migrate')
    system('python3 manage.py migrate')
    system('python3 manage.py runserver')
elif len(argv) != 1 and argv[1] == 'test':
    system("python3 manage.py test")
else:
    print("Nooo prod")