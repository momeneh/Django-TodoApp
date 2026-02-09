
<h1 align="center">Django Class Based View Todo App</h1>
<h3 align="center">A simple todo app project with class based view for learning</h3>
<p align="center">

### Overview
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Getting ready](#getting-ready)
- [options](#options)



### Features
- Django LTS
- Class Based 
- User authentication
- Black
- Responsive Design
- Bootstrap5


### Prerequisites

- Docker
- Docker Compose

### Setup
To get this repository, run the following command inside your git enabled terminal
```bash
git clone https://github.com/momeneh/Django-TodoApp.git
```

### Getting ready
```bash
cd Django-TodoApp 
docker-compose up --build -d
```

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### options
Project it self has the user creation form but still in order to use the admin you need to create a super user.you can use the createsuperuser option to make a super user.
```bash
docker-compose exec web python manage.py createsuperuser
```



Once the server is up and running, head over to http://127.0.0.1:8000 for the App.


