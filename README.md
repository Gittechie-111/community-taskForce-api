# Community TaskForce API

A RESTful API for managing community projects and tasks. Built with Flask and MySQL, it provides endpoints for user authentication, project management, and task assignment.

## 🚀 Features

- User registration & login (session‑based authentication)
- Create, read, update, and delete projects
- Create, read, update, delete, and assign tasks
- Track task status (pending, in progress, completed)
- Automatically record completion timestamps
- Filter projects by status, tasks by status
- Get progress statistics per project

## 🛠️ Technologies Used

- **Backend:** Python, Flask, Flask‑CORS
- **Database:** MySQL
- **Authentication:** Session cookies, bcrypt for password hashing
- **Deployment:** Ready for PythonAnywhere / Render

## 📦 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Gittechie-111/community-taskForce-api.git
cd community-taskForce-api

2. Create and activate a virtual environment
bash

python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install dependencies
bash

pip install -r requirements.txt

4. Set up the database

    Make sure MySQL is installed and running.

    Create a database named community_taskforce.

    Run the SQL schema (provided in schema.sql or create tables manually using the statements in the code).

5. Configure environment variables

Create a .env file in the root directory:
env

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=community_taskforce
SECRET_KEY=your-secret-key
DEBUG=True

6. Run the application
bash

python app.py

The API will be available at http://localhost:5000.
