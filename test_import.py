import sys
import os

print("Starting import test...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newproject.settings')

import django
django.setup()

print("Django setup done. Importing urls...")

from newproject import urls

print("Successfully imported urls!")
