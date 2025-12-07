"""
Create a test user for integration testing.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memory_maps_project.settings.development')
django.setup()

from django.contrib.auth.models import User

# Create test user
username = "testuser"
password = "testpass123"
email = "test@example.com"

# Delete if exists
User.objects.filter(username=username).delete()

# Create new user
user = User.objects.create_user(
    username=username,
    email=email,
    password=password
)

print(f"✓ Test user created:")
print(f"  Username: {username}")
print(f"  Password: {password}")
print(f"  Email: {email}")
