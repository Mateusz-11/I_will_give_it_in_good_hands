
# I will give it in good hands App



## Introduction

The project "I will give it in good hands" it's a web application for people who want to pass their things to others.


## Run Locally


Make fork of repository & go to the project directory

```bash
  cd my-project
```

Clone the project

```bash
  git clone https://github.com/<name_of_your_Github_profile>/I_will_give_it_in_good_hands.git
```

Install dependencies

```bash
  pip install -r requirements.txt

```

Cofigure PostgreSQL database in settings

```bash
  DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<name_of_database>',
        'USER': '<username>',
        'PASSWORD': '<password_to_database>',
    }
}
```

Do migrates to database

```bash
  python manage.py migrate

```


Start the server

```bash
    python manage.py runserver
```



## 🛠 Technology

- Python

- Django 

- JavaScript

- PostgreSQL

- HTML

- Bootstrap

