# 📚 Book Store Web Application

A professional, fully responsive web application built with Python and Flask. This project is a comprehensive digital bookstore platform featuring internationalization (i18n), a robust MySQL database, and full Docker containerization for seamless deployment.

![Book Store Banner](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## ✨ Key Features

- **🌐 Internationalization (i18n):** Multi-language support right out of the box. Currently supports **English, Arabic (RTL), French, and German**.
- **🐳 Dockerized Environment:** Production-ready containerization. The application and database are fully orchestrated using Docker and Docker Compose.
- **🗄️ MySQL Database Engine:** Reliable and scalable data storage powered by MySQL 8.0, managed via `Flask-SQLAlchemy`.
- **🔐 Secure Authentication:** User registration and login system with password hashing using `Flask-Bcrypt` and session management via `Flask-Login`.
- **📱 Responsive UI/UX:** Clean, modern, and mobile-friendly interface styled with a custom green-themed design and Bootstrap 5.
- **⭐ Review System:** Authenticated users can write, edit, and delete reviews for the store.
- **🔍 Search & Filtering:** Easily browse books by category or search by title/author.

## 🛠️ Technology Stack

- **Backend:** Python 3.11, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, PyMySQL
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (for i18n), Bootstrap 5, FontAwesome
- **Database:** MySQL 8.0
- **DevOps:** Docker, Docker Compose, Gunicorn

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose installed on your machine.

### Running with Docker (Recommended)

The easiest way to get the application up and running is by using Docker Compose.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Zeus62/bookstore.git
   cd bookstore
   ```

2. **Build and start the containers:**
   ```bash
   docker compose up --build -d
   ```

3. **Access the application:**
   Open your web browser and navigate to:
   [http://localhost:3000](http://localhost:3000)

4. **Stopping the application:**
   ```bash
   docker compose down
   ```

### Running Locally (Without Docker)

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the Database URI (Optional):**
   By default, the app expects a MySQL connection. You can set it as an environment variable:
   ```bash
   export DATABASE_URI="mysql+pymysql://username:password@localhost/dbname"
   ```

4. **Run the Flask application:**
   ```bash
   python app.py
   ```

## 📂 Project Structure

```text
.
├── Book_Store/              # Main Application Package
│   ├── Main/                # Core routes (Home, Books, About)
│   ├── reviews/             # Review system routes
│   ├── users/               # Authentication routes
│   ├── static/              # CSS, JS, and i18n JSON files
│   ├── templates/           # Jinja2 HTML templates
│   ├── __init__.py          # App factory and configuration
│   └── models.py            # SQLAlchemy database models
├── Dockerfile               # Docker configuration for the web app
├── docker-compose.yml       # Multi-container orchestration (Web + MySQL)
├── requirements.txt         # Python package dependencies
└── app.py                   # Application entry point
```

## 🐳 Docker Hub Repository

The pre-built Docker image for this application is available on Docker Hub:
**[ahmeesmat/bookstore](https://hub.docker.com/r/ahmeesmat/bookstore)**

To pull and run the image directly:
```bash
docker pull ahmeesmat/bookstore:latest
docker run -p 3000:3000 ahmeesmat/bookstore:latest
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/Zeus62/bookstore/issues).

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
