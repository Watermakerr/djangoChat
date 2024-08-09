# Introduction

A simple chat app web using Django.  
The frontend can be found [here](https://github.com/Watermakerr/vueChat).

# Getting Started

## Prerequisites

- Python 3.x
- pip (Python package installer)
- Docker (for running Redis server)

## Setup

### 1. Clone the Repository

Clone the repository from GitHub:

```sh
git clone https://github.com/Watermakerr/chatapp.git
```

### 2. Create and Activate Virtual Environment

Create a virtual environment for your project:

```sh
python -m venv venv
```
Activate the virtual environment:

```sh
.\venv\Scripts\activate
```

### 3. Install Dependencies
Install project dependencies:

```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the root directory of your project and add the following variables:

```sh
# Email configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password

# Django secret key
SECRET_KEY=your_secret_key_here
```
You can use the provided env.example file as a template:
```sh
cp env.example .env
```

### 5. Apply Migrations
Navigate to the Django project directory and apply the migrations:

```sh
cd djangoChat
python manage.py migrate
```

### 6. Run Redis Server
Run the Redis server using Docker:

```sh
docker run --rm -p 6379:6379 redis:7
```

### 7. Run the Development Server
You can now run the development server:

```sh
python manage.py runserver
```
## Additional Information
For more details on how to use the frontend, visit the [frontend repository](https://github.com/Watermakerr/vueChat).
