# Coderr Backend

This is the backend part of the Coderr project, built with Django to run the freelance marketplace tool in the frontend.

## Requirements

- You need to have **Python** installed to run this project.

## Getting Started

1. **Clone the Frontend and Backend Projects**
   - Clone this backend project
     ```bash
     git clone git@github.com:Kakar21/Coderr-Backend.git
     ```

2. **Create a Virtual Environment**
   - In the project root, create a virtual environment:
     ```bash
     python -m venv env
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       env\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source env/bin/activate
       ```

3. **Install Dependencies**
   - Install all the requirements listed in the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

4. **Set Up SECRET_KEY**
   - You need a unique `SECRET_KEY` for your Django instance. Generate one by running:
     ```bash
     python
     from django.core.management.utils import get_random_secret_key
     print(get_random_secret_key())
     ```
   - Create a file named `.env` in the `join_backend` folder and add your generated key as follows:
     ```plaintext
     SECRET_KEY='your_generated_secret_key'
     ```

5. **Run Migrations**
   - Apply migrations to set up the database:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

6. **Start the Server**
   - Start the Django server:
     ```bash
     python manage.py runserver
     ```

7. **Guest Login Setup**
   - To enable guest login, create a guest user with the credentials provided in the frontend project.

### You're Done!

Your backend server should now be up and running, ready to support the Coderr frontend. Enjoy exploring and customizing the project!
