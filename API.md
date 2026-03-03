📚 API Documentation & Deployment Guide

Now that your API is fully tested and working, it's time to document it for your frontend collaborator and deploy it so they can access it live.
📝 1. Create API Documentation

Your frontend developer needs a clear reference of all endpoints, request/response formats, and authentication requirements. You can provide this as a Markdown file in your repository (e.g., API.md) or share a Postman collection.
📄 Example API.md Structure
markdown

# Community TaskForce API Documentation

**Base URL:** `http://localhost:5000` (development) / `https://your-app.pythonanywhere.com` (production)

## Authentication

Most endpoints require authentication. After login, the server sets a session cookie; include it in subsequent requests.

### Register
- **URL:** `/api/auth/register`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "full_name": "string?",
    "phone": "string?"
  }

    Success: 201 Created with user object.

Login

    URL: /api/auth/login

    Method: POST

    Body:
    json

    {
      "email": "string",
      "password": "string"
    }

    Success: 200 OK with user object and session cookie.

Logout

    URL: /api/auth/logout

    Method: POST

    Success: 200 OK

Get Current User

    URL: /api/auth/me

    Method: GET

    Auth: Required

    Success: 200 OK with user object.

Projects
List All Projects

    URL: /api/projects/

    Method: GET

    Query Params: ?status=active (optional)

    Success: 200 OK with array of projects (each includes completion_percentage).

Get Single Project

    URL: /api/projects/<id>

    Method: GET

    Success: 200 OK with project object.

Create Project

    URL: /api/projects/

    Method: POST

    Auth: Required

    Body:
    json

    {
      "title": "string",
      "description": "string",
      "location": "string?",
      "start_date": "YYYY-MM-DD?",
      "end_date": "YYYY-MM-DD?"
    }

    Success: 201 Created with project object.

Update Project

    URL: /api/projects/<id>

    Method: PUT

    Auth: Required (creator or admin)

    Body: Any of title, description, location, start_date, end_date, status.

    Success: 200 OK with updated project.

Delete Project

    URL: /api/projects/<id>

    Method: DELETE

    Auth: Required (creator or admin)

    Success: 200 OK with message.

Tasks
Get Project Tasks

    URL: /api/tasks/project/<project_id>

    Method: GET

    Query Params: ?status=pending (optional)

    Success: 200 OK with array of tasks.

Get Single Task

    URL: /api/tasks/<task_id>

    Method: GET

    Success: 200 OK with task (includes assignee/creator names, project title).

Create Task

    URL: /api/tasks/project/<project_id>

    Method: POST

    Auth: Required

    Body:
    json

    {
      "title": "string",
      "description": "string?",
      "assigned_to": "user_id?",
      "priority": "low|medium|high|urgent",
      "due_date": "YYYY-MM-DD?"
    }

    Success: 201 Created with task object.

Update Task

    URL: /api/tasks/<task_id>

    Method: PUT

    Auth: Required (creator, assignee, or admin)

    Body: Any of title, description, assigned_to, priority, status, due_date.

    Success: 200 OK with updated task.

Mark Task Complete

    URL: /api/tasks/<task_id>/complete

    Method: PUT

    Auth: Required

    Success: 200 OK with task (status becomes completed, completed_at set).

Get My Assigned Tasks

    URL: /api/tasks/assigned

    Method: GET

    Auth: Required

    Success: 200 OK with array of tasks assigned to current user (excluding completed).

Delete Task

    URL: /api/tasks/<task_id>

    Method: DELETE

    Auth: Required (creator or admin)

    Success: 200 OK with message.

Error Responses

    400 Bad Request – Invalid input (e.g., missing field, wrong data type).

    401 Unauthorized – Not logged in.

    403 Forbidden – Insufficient permissions.

    404 Not Found – Resource doesn't exist.

    500 Internal Server Error – Something broke on the server.

text


### 📬 Share Postman Collection

You can export your Postman collection (with all saved requests) as a JSON file and share it. Your collaborator can import it and have all endpoints ready to test.

---

## ☁️ 2. Deploy to the Cloud

Your frontend developer needs a live URL to connect to. Here are two easy options:

### Option A: PythonAnywhere (Recommended for Beginners)

PythonAnywhere offers a free tier with a MySQL database and supports Flask.

**Steps:**

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com) (free account).
2. **Open a Bash console** from the Dashboard.
3. **Clone your GitHub repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/community-taskforce-api.git
   cd community-taskforce-api

    Create a virtual environment and install dependencies:
    bash

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    Set up MySQL database:

        Go to the Databases tab and create a new MySQL database (name it, e.g., yourusername$community).

        Note the host, username, password, and database name.

        In the MySQL console, run your CREATE TABLE statements (from earlier) to create the schema.

    Configure environment variables:

        Create a .env file in your project folder with the database credentials:
        text

        DB_HOST=yourusername.mysql.pythonanywhere-services.com
        DB_USER=yourusername
        DB_PASSWORD=yourpassword
        DB_NAME=yourusername$community
        SECRET_KEY=your-secret-key
        DEBUG=False

    Configure the WSGI file:

        Go to the Web tab and add a new web app.

        Choose Manual configuration (not a quickstart) and select Python version.

        Edit the WSGI configuration file (link provided). Replace its contents with:
        python

        import sys
        import os

        path = '/home/yourusername/community-taskforce-api'
        if path not in sys.path:
            sys.path.append(path)

        from app import app as application  # noqa

    Reload the app from the Web tab.

    Your API is now live at https://yourusername.pythonanywhere.com.
