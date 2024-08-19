# 42Evaluators Setup Guide

This guide will help you set up the local development environment. Follow the steps below to get started.

## 1. Clone the Repository

First, clone the project repository to your local machine using Git.

```bash
git clone https://github.com/PepeSegura/OSS-42evaluators.git
cd OSS-42evaluators
```

## 2. Create and Activate a Virtual Environment
It's recommended to create a virtual environment to isolate your project dependencies.

On macOS/Linux:
```bash
python3 -m venv new-env
source new-env/bin/activate
```
On Windows:
```bash
python -m venv new-env
new-env\Scripts\activate
```
This command will create a new virtual environment in a directory named new-env and activate it

## 3. Install Dependencies
Once your virtual environment is activated, install the required packages using pip:

```bash
pip install -r requirements.txt
```
This command installs all the packages listed in the requirements.txt file.

## 4. Apply Database Migrations
Before running the server, you need to apply the database migrations to set up your database schema:

```bash
python manage.py migrate
```
This command will apply all the necessary migrations to your database.

## 5. Create a Superuser
If you want to access the Django admin interface, you'll need to create a superuser:

```bash
python manage.py createsuperuser
```
You'll be prompted to enter a username, email, and password.

## 6. Run the Development Server
Now you're ready to run the Django development server:

```bash
python manage.py runserver
```
By default, the server will start on http://127.0.0.1:8000/. You can open this URL in your browser to see the project running locally.

## 7. Accessing the Admin Interface
If you've created a superuser, you can access the Django admin interface at:

```bash
http://127.0.0.1:8000/admin/
```
Log in with the superuser credentials you created earlier.

## 8. Populate the Database

Once the server is running, you'll see the website, but it won't have any users. To populate the database, log into the admin panel and add 2 keys into the key database.

To obtain the necessary `UID` and `SECRET`, you need to register a new application at [42 Intra OAuth Applications](https://profile.intra.42.fr/oauth/applications). After registering, you'll receive a UID and SECRET for your application.

They can be the same, but one of them needs to be called `1_LOGIN`.

- **Key 1:**
  - **Name:** 1_LOGIN
  - **UID:** `Your UID from the 42 Intra`
  - **SECRET:** `Your SECRET from the 42 Intra`

- **Key 2:**
  - **Name:** name
  - **UID:** `Your UID from the 42 Intra`
  - **SECRET:** `Your SECRET from the 42 Intra`

After setting the keys, you need to populate the database by running the update script. Navigate to `update_database/schedule_update.py` and modify the `start()` function:

- **For the first-time setup in development:**
  - Set `updateDatabase` to 1 minute
  - Set `updateLocations` to 5 minutes

- **After you have some data in the database:**
  - Set `updateDatabase` to 30 minutes (or disable it)
  - Set `updateLocations` to 10 minutes (or disable it)


## 9. Restart the Server
After the keys are set, quit the server by pressing CONTROL-C. Then, run the server again with:

```bash
python manage.py runserver
```
Now your setup should be complete, and the website should be fully functional with the populated database.
