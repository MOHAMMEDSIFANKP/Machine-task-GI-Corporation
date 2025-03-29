# 📌 CSV File Validation API

## 🚀 Project Setup

### 1️⃣ Create a Virtual Environment
#### Ubuntu/Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure the Database
- Set up your database.
- Create a new `.env` file (You will receive this via email).

### 4️⃣ Run Migrations
```bash
python manage.py migrate
```

### 5️⃣ Start the Server
#### Ubuntu/Linux/macOS:
```bash
python3 manage.py runserver
```
#### Windows:
```bash
python manage.py runserver
```

---

## 🌐 API Endpoint
### Upload and Validate CSV File
**POST** `http://127.0.0.1:8000/api/v1/csv-reader/`

The API expects a CSV file named `checking_data.csv` to be placed in the project directory.

---

## 📄 File Validation Rules
The uploaded file must meet the following validation rules:
- **File Format**: Must be a valid CSV file.
- **Fields**:
  - `name` → Required, non-empty string.
  - `email` → Required, valid email format, must not already exist in the database.
  - `age` → Required, integer between 0 and 120.

---

## 📊 Response Summary
The API will return a summary containing:
- ✅ Total valid records saved.
- ❌ Total records rejected.
- ⚠️ Validation errors for rejected records.

### 📥 Example Response
```json
{
    "total_records": 3,
    "successfully_saved": 0,
    "rejected_records": 3,
    "errors": [
        {
            "row": 2,
            "errors": {
                "age": "Age must be between 0 and 120."
            }
        },
        {
            "row": 6,
            "errors": {
                "age": "Age must be between 0 and 120."
            }
        },
        {
            "row": 9,
            "errors": {
                "age": "Age must be between 0 and 120."
            }
        }
    ]
}
```

---

### ✅ Setup Complete! 🎉
