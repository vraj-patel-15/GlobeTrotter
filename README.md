# 🌍 GlobeTrotters

> **Personalized Travel Planning & Expense Management Platform**

GlobeTrotters is a web-based travel planning platform that helps users **discover destinations, build multi-city itineraries, estimate trip expenses, visualize travel plans, and share itineraries with the community.**

The platform combines personalized trip planning with dynamic destination information and structured expense management to make travel planning easier and more organized.

---

## ✨ Features

Personalized Dashboard
City & Destination Exploration
Trip Builder
Budget & Expense Management
Itinerary & Calendar
Community
User Profile
Admin Panel
Application Screens

The application is organized around the following screens:

1. **Loading / Landing Page**
2. **Login**
3. **Registration**
4. **Dashboard**
5. **Create New Trip**
6. **Build Itinerary**
7. **My Trips**
8. **City Search**
9. **Activity Search**
10. **Itinerary View**
11. **Budget View**
12. **Calendar View**
13. **Community**
14. **User Profile**
15. **Admin Panel**

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │       USER          │
                         │     Web Browser     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FRONTEND       │
                         │     HTML + CSS      │
                         │    JavaScript       │
                         └──────────┬──────────┘
                                    │
                              HTTP Requests
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    FLASK BACKEND    │
                         │       Python        │
                         │                     │
                         │ Authentication      │
                         │ Trip Management     │
                         │ Itinerary           │
                         │ Search              │
                         │ Budget              │
                         │ Community           │
                         └──────────┬──────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
              ┌──────────────────┐   ┌──────────────────┐
              │    PostgreSQL    │   │  External APIs   │
              │     Database     │   │ Dynamic Data     │
              └──────────────────┘   └──────────────────┘
```

---

# 🛠️ Tech Stack

| Layer           | Technology                    |
| --------------- | ----------------------------- |
| Frontend        | HTML5, CSS3, JavaScript       |
| Backend         | Python, Flask                 |
| Database        | PostgreSQL                    |
| ORM             | SQLAlchemy / Flask-SQLAlchemy |
| Authentication  | Flask-based authentication    |
| Version Control | Git & GitHub                  |
| External Data   | Dynamic APIs                  |

---

# 📁 Project Structure

```text
GlobeTrotter/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── trip.py
│   │   ├── city.py
│   │   ├── activity.py
│   │   ├── itinerary.py
│   │   └── expense.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── trips.py
│   │   ├── itinerary.py
│   │   ├── search.py
│   │   ├── budget.py
│   │   ├── community.py
│   │   └── admin.py
│   │
│   ├── services/
│   │   ├── city_service.py
│   │   ├── activity_service.py
│   │   └── budget_service.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── loading.html
│   │   │
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── trips/
│   │   ├── itinerary/
│   │   ├── search/
│   │   ├── budget/
│   │   ├── profile/
│   │   ├── community/
│   │   └── admin/
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
├── migrations/
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

---

# 🚀 Getting Started

Follow the steps below to run GlobeTrotters locally.

## 1. Clone the Repository

```bash
git clone https://github.com/vraj-patel-15/GlobeTrotter.git
cd GlobeTrotter
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🐘 PostgreSQL Database Setup

GlobeTrotters uses **PostgreSQL**, so the project does **not** use a `.db` file like SQLite.

You need to have PostgreSQL installed and running on your computer.

Create a database:

```sql
CREATE DATABASE globetrotter;
```

Then create a PostgreSQL user if required:

```sql
CREATE USER globetrotter_user WITH PASSWORD 'your_password';
```

Grant access:

```sql
GRANT ALL PRIVILEGES ON DATABASE globetrotter TO globetrotter_user;
```

---

# 🔐 Environment Variables

Create a `.env` file in the root directory:

```text
DATABASE_URL=postgresql://globetrotter_user:your_password@localhost:5432/globetrotter
SECRET_KEY=your-secret-key
```

### `.env.example`

The repository contains a `.env.example` file so that other developers know which environment variables are required:

```text
DATABASE_URL=
SECRET_KEY=
```

> **Never commit your actual `.env` file to GitHub.**

Make sure `.gitignore` contains:

```text
.env
venv/
__pycache__/
*.pyc
```

---

# 🗄️ Database Initialization

After PostgreSQL is running and your `.env` file is configured, initialize the database using the project's database/migration setup.

For example:

```bash
flask db upgrade
```

If migrations are not being used yet, the application can create the required tables during initial setup.

---

# ▶️ Running the Application

Start the Flask development server:

```bash
python run.py
```

Or, if your project uses Flask's CLI:

```bash
flask run
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

---

# 🔄 Development Workflow

GlobeTrotters is developed collaboratively using Git branches.

```text
                    master
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 feature/backend   feature/frontend   feature/itinerary
        │              │              │
        └──────────────┼──────────────┘
                       │
                  Pull Request
                       │
                       ▼
                    master
```

Each team member works on a separate feature branch.

### Create a branch

```bash
git checkout -b feature/your-feature
```

### Save changes

```bash
git add .
git commit -m "feat: add trip creation"
```

### Push the branch

```bash
git push -u origin feature/your-feature
```

### Merge

Create a Pull Request on GitHub and merge the completed feature into `master`.

Before starting new work, always update your local branch:

```bash
git checkout master
git pull origin master
```

---

# 🧑‍💻 Team Responsibilities

| Role               | Responsibilities                                                       |
| ------------------ | ---------------------------------------------------------------------- |
| Backend            | Flask application, routes, authentication, business logic              |
| Database           | PostgreSQL schema, relationships, migrations, database testing         |
| Frontend           | HTML, CSS, JavaScript, UI/UX and responsive screens                    |
| Integration & APIs | External APIs, search, budget visualization, community and integration |

All four roles contribute to the **same application, backend and PostgreSQL database**.

---

# 🔗 Core Data Relationships

```text
User
 │
 └───< Trips
          │
          ├───< Trip Stops >─── City
          │                       │
          │                       └───< Activities
          │
          ├───< Expenses
          │
          └───< Itinerary Activities
```

This relational structure allows users to maintain multiple trips, multiple destinations per trip, activities within destinations, and expenses associated with their journeys.

---

# 📊 Main Application Flow

```text
Login / Registration
        ↓
    Dashboard
        ↓
   Create Trip
        ↓
  Add Destinations
        ↓
  Add Activities
        ↓
 Build Itinerary
        ↓
 ┌──────┼─────────┐
 ↓      ↓         ↓
Budget Calendar  Share
        ↓
   Complete Trip
```

---

# 🧪 Testing

Run the project's tests using:

```bash
pytest
```

Tests should cover important functionality such as:

* User registration and login
* Trip creation
* Trip editing/deletion
* Adding and removing destinations
* Adding activities
* Budget calculations
* Itinerary generation
* Public trip sharing

---

# 🔒 Security

The following information should never be committed to the repository:

* Database passwords
* Secret keys
* API keys
* Personal credentials
* `.env` files

Use environment variables for sensitive configuration.

---

# 📌 Important Note About Database Files

GlobeTrotters uses **PostgreSQL**, not SQLite.

Therefore, you will **not normally have a file such as**:

```text
database.db
```

Instead, PostgreSQL stores the database separately as a database server.

For sharing the database structure/data with another developer, use one of these approaches:

### Option 1 — Recommended for development

Use migrations:

```bash
flask db upgrade
```

### Option 2 — PostgreSQL backup

Create a SQL dump:

```bash
pg_dump -U globetrotter_user globetrotter > database.sql
```

Another developer can restore it with:

```bash
psql -U globetrotter_user -d globetrotter < database.sql
```

Do **not** commit database passwords or private production data into `database.sql`.

---

# 🎯 Project Goal

GlobeTrotters aims to make travel planning more organized by bringing together:

**Discover → Plan → Budget → Visualize → Share**

in one platform.

---

## 👥 Contributors

Built collaboratively by the GlobeTrotters hackathon team.

* **Vraj Patel** — Backend 
* **Purvil Patel** — Database
* **Het Patel** — Frontend 1
* **Meet Patel** — Frontend 2

---

## 📄 License

This project was developed as part of a hackathon project.

---
