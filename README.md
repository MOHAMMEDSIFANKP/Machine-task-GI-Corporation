README: CSV File Validation API

Project Setup

1. Create a Virtual Environment

Ubuntu/Linux/macOS:

python3 -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
venv\Scripts\activate

2. Install Dependencies

pip install -r requirements.txt

3. Create and Configure the Database

Set up your database.

Create a new .env file (You will receive the .env file via email).

4. Run Migrations
python manage.py migrate

5. Start the Server

Ubuntu/Linux/macOS:

python3 manage.py runserver

Windows:

python manage.py runserver

API Endpoint
Upload and validate CSV file

POST http://127.0.0.1:8000/api/v1/csv-reader/

The API expects a CSV file named checking_data.csv to be placed in the project directory.

File Validation Rules
The file must be a valid CSV file.

Each row must have the following fields:

name → Required, non-empty string.

email → Required, valid email format, must not already exist in the database.

age → Required, integer between 0 and 120.

Response Summary
The API will return a summary of:

Total valid records saved.

Total records rejected.

Validation errors for rejected records.

