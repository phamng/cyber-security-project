# Cyber Security Project

This project is focused on identifying and mitigating common security flaws in
web applications. It includes a demo application (`mysite`) and a collection of
screenshots that document various security flaws and their fixes.

- **mysite/**: A Django-based web application used for testing and showcasing
  security vulnerabilities.
  - `db.sqlite3`: The database file for the Django application.
  - `manage.py`: The entry point for managing the Django application.
  - `polls/`: A sample app within the Django project.
- **screenshots/**: A collection of images showing before-and-after states of
  identified security flaws.

## How to Run the Project

1. Navigate to the `mysite` directory:

   ```bash
   cd cyber-security-project
   cd mysite

   ```

2. Run the Django development server:

   ```bash
   python manage.py runserver

   ```

3. Open your browser and go to http://127.0.0.1:8000/ to access the application.
