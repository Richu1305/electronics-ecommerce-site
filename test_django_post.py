import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newproject.settings')
django.setup()

client = Client()
response = client.post('/category', {'Name': 'Test', 'Description': 'Test Desc'})
print(f"Status Code: {response.status_code}")
