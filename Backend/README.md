# KMA ASSIGNMENT

## Requirement
    Python version 3.10 or higher
## Setup environment
    sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

## Set up to run project
    1. pip install -r requirements.txt
    2. python3 manage.py makemigrations
    3. python3 manage.py migrate
    4. python3 manage.py runserver 

## Create admin account
    python3 manage.py createadminuser --username=admin --email=at150536@actvn.edu.vn --password=admin
