import csv
import io
import re
from rest_framework import serializers

from .models import User

class CsvFileValidaterSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        
        # Check the content type is csv
        if value.content_type not in ['text/csv', 'application/vnd.ms-excel']:
            raise serializers.ValidationError("Invalid file type. Please upload a CSV file.")

        return value
    
    def validate_csv_datas(self, file):
        """
        Read and validates CSV file contects
        validates : name, email and age
        """
        decoded_file = file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded_file))
        
        valid_records = [] # Keep valid user model records for bulk create.
        errors = []
                
        for index, row in enumerate(reader, start = 1):
            row_errors = {}
            
            # name validation
            name = row.get('name', '').strip()
            if not name:
                row_errors['name'] = "Name cannot be empty."

            # email validation
            email = row.get('email', '').strip()
            if not email:
                row_errors['email'] = "Email cannot be empty."
            elif not self.email_validator(email):
                row_errors['email'] = "Invalid email address."
             # Skip this record if email exists
            elif User.objects.filter(email = email).exists():
                continue

            # age validation
            age = row.get('age', '').strip()
            try:
                age = int(age)
                if age < 0 or age > 120:
                    row_errors['age'] = "Age must be between 0 and 120."
            except ValueError:
                row_errors['age'] = "Age must be a valid integer."

            if row_errors:
                errors.append({"row": index, "errors": row_errors})
            else:
                valid_records.append(User(name=name, email=email, age=age))

        return valid_records, errors

    @staticmethod
    def email_validator(email):
        """
        Validates an email using regex.
        Returns True if valid, False otherwise.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))