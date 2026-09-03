# Django TodoApp

A task management web application built with **Python and Django**, developed as a hands-on project to build practical experience with Django backend development.

The application provides user authentication, user-specific task management, full CRUD operations, a responsive Bootstrap interface, and Docker-based development and deployment configuration.

## 🚀 Live Demo

**Live Application:**
https://django-todoapp-vh84.onrender.com/

## 📦 Source Code

**GitHub Repository:**
https://github.com/momeneh/Django-TodoApp

---

## ✨ Features

* User authentication
* User-specific task management
* Create, read, update, and delete tasks
* Mark tasks as completed or pending
* Django Class-Based Views
* Protected views using authentication mixins
* Django ORM for database operations
* Responsive UI with Bootstrap 5
* Environment-based configuration
* Docker and Docker Compose support
* Deployment configuration for Render

---

## 🛠️ Technologies

### Backend

* Python
* Django
* Django REST Framework
* PostgreSQL
* Django ORM

### Frontend

* HTML
* CSS
* Bootstrap 5

### DevOps & Tools

* Docker
* Docker Compose
* PostgreSQL Docker volume
* Git
* GitHub
* Render

---

## 🏗️ Project Structure

```text
Django-TodoApp/
│
├── core/
│   ├── todo/
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── ...
│   │
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── ...
│   │
│   └── manage.py
│
├── Dockerfile
├── DockerfileRender
├── docker-compose.yml
├── docker-compose-stage.yml
├── requirements.txt
└── README.md
```

---

## 🔐 Authentication & Authorization

The application uses Django's authentication system to protect task management functionality.

Authenticated users can manage their own tasks, while task queries are filtered according to the currently authenticated user.

This ensures that users only interact with tasks associated with their own accounts.

---

## 📝 Task Management

The application supports the complete task lifecycle:

1. Create a task
2. View tasks
3. Update a task
4. Delete a task
5. Mark a task as completed
6. Change a completed task back to pending

The task management functionality is implemented using Django Class-Based Views such as:

* `ListView`
* `CreateView`
* `UpdateView`
* `DeleteView`

Authentication requirements are handled using Django authentication mixins.

---
## 🔌 REST API

The application includes a versioned REST API built with Django REST Framework.

### API Features

* Versioned API under `/api/v1/`
* RESTful task management using `ModelViewSet`
* Automatic URL routing with DRF `DefaultRouter`
* Authentication with `IsAuthenticated`
* Custom object-level authorization with `IsOwner`
* User-specific querysets to isolate task data
* `ModelSerializer` for task serialization
* Automatic assignment of newly created tasks to the authenticated user

### API Endpoint

```text
/api/v1/
```

The API supports standard REST operations for tasks, including:

* `GET` — List and retrieve tasks
* `POST` — Create a task
* `PUT` — Update a task
* `PATCH` — Partially update a task
* `DELETE` — Delete a task
---
## 🗄️ Data Model

The main `Task` model contains information such as:

* Task title
* Associated user
* Creation date
* Last update date
* Completion status

The relationship between users and tasks allows each authenticated user to manage their own task list.

---
## 🧪 Testing

The project includes API tests built with **pytest** and Django REST Framework's `APIClient`.

The test suite covers authentication, authorization, CRUD operations, validation, and access control for user-owned tasks.

### Test Coverage

* Anonymous access protection
* Authenticated user access
* Task creation
* Task listing
* Task retrieval
* Task update
* Task deletion
* Invalid task IDs
* Request validation
* Object-level authorization
* Preventing users from accessing or modifying other users' tasks

### Testing Tools

* pytest
* Django test database
* Django REST Framework `APIClient`
* `pytest.mark.django_db`

### Run Tests

From the project root:

```bash
pytest
```

To run the API tests specifically:

```bash
pytest core/todo/api/v1/tests/
```
---
## 🐳 Docker

The project includes Docker configuration for containerized development and deployment.

### Run with Docker Compose

Clone the repository:

```bash
git clone https://github.com/momeneh/Django-TodoApp.git
cd Django-TodoApp
```

Build and start the containers:

```bash
docker compose up --build
```

After the containers are running, access the application through the configured local port.

To stop the containers:

```bash
docker compose down
```

---

## 💻 Local Development

### 1. Clone the repository

```bash
git clone https://github.com/momeneh/Django-TodoApp.git
cd Django-TodoApp
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Linux/macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on the provided environment configuration.

Example:

```env
DEBUG=True
SECRET_KEY=your-secret-key
```

Add the required database configuration according to your environment.

### 5. Run migrations

```bash
python core/manage.py migrate
```

### 6. Create a superuser

```bash
python core/manage.py createsuperuser
```

### 7. Start the development server

```bash
python core/manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```
---

## 🔄 CI/CD

GitHub Actions is configured to automatically run the test suite on every push and pull request.

The CI pipeline verifies:
- Python dependencies
- Django configuration
- PostgreSQL service
- API tests
  
---

## 🌐 Deployment

The application has been configured for deployment on **Render**.

The deployed application is available at:

https://django-todoapp-vh84.onrender.com/

Deployment configuration includes a dedicated Docker configuration and environment-based settings.

---

## 🎯 Project Goals

This project was developed to gain practical experience with Django backend development and to apply concepts including:

* Django project architecture
* Models and Django ORM
* Class-Based Views
* Authentication and authorization
* CRUD operations
* Form handling
* PostgreSQL database integration
* Docker containerization
* Environment configuration
* Cloud deployment

---

## 🔮 Future Improvements

Potential improvements for future versions include:

* Expanded REST API functionality
* Task priorities and categories
* Due dates and reminders
* Search functionality
* Rate limiting

---

## 👩‍💻 Author

**Momeneh Jafari**

Senior Backend Developer

Backend technologies:

`PHP` · `Laravel` · `Python` · `Django` · `REST APIs` · `MySQL` · `Docker` . `PostgreSQL`

### Connect

* GitHub: https://github.com/momeneh
* LinkedIn: https://www.linkedin.com/in/momeneh-jafari-7a177a84/

---

## 📄 License

This project is available for educational and portfolio purposes.

---
### Screenshots / API Documentation
This is a brief demo of the functionality of the project 
<p align="center">
<img src="https://github.com/momeneh/Django-TodoApp/blob/b21a5cc9dc3138e9aa4c3e2caab512074e258209/demo/toDoWeb.gif" alt="toDoWeb" width="720"/>
</p>


This is a brief demo of the functionality of the project swagger
<p align="center">
<img src="https://github.com/momeneh/Django-TodoApp/blob/b21a5cc9dc3138e9aa4c3e2caab512074e258209/demo/toDoSwagger.gif" alt="toDoWeb" width="720"/>
</p>

This is a brief demo of the functionality of the project rest framework web api
<p align="center">
<img src="https://github.com/momeneh/Django-TodoApp/blob/b21a5cc9dc3138e9aa4c3e2caab512074e258209/demo/toDoRestWebApi.gif" alt="toDoWeb" width="720"/>
</p>




