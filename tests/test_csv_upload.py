from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from csv_reader.models import User
import csv
import io

class CsvUploadAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/csv-reader/'
        
    def generate_csv_file(self, data):
        """
        Helper method to generate a demo CSV file for checking
        """
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['name', 'email', 'age']) 
        writer.writerows(data)
        output.seek(0)
        return SimpleUploadedFile("test.csv", output.getvalue().encode('utf-8'), content_type='text/csv')
    
    def test_valid_file_csv_upload(self):
        """
        Test uploading a valid CSV file
        """
        csv_file = self.generate_csv_file([
            ['John Doe', 'johndoe@example.com', '30'],
            ['Jane Smith', 'janesmith@example.com', '25']
        ])
        response = self.client.post(self.url, {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)
    
    def test_invalid_file_csv_upload(self):
        """
        Test uploading a invalid CSV file
        """
        invalid_file = SimpleUploadedFile("test.txt", b"Invalid content", content_type="text/plain")
        response = self.client.post(self.url, {'file': invalid_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('file', response.data)

    def test_invalid_email(self):
        """Test uploading a CSV file with an invalid email format"""
        csv_file = self.generate_csv_file([
            ['Invalid Email User', 'invalid-email', '40']
        ])
        response = self.client.post(self.url, {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.data['rejected_records'], 1)
    
    def test_invalid_age(self):
        """Test uploading a CSV file with an invalid age"""
        csv_file = self.generate_csv_file([
            ['Too Young', 'tooyoung@example.com', '-5'],  
            ['Too Old', 'tooold@example.com', '200'] 
        ])
        response = self.client.post(self.url, {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.data['rejected_records'], 2)