"""
Create or recreate the superuser account.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memory_maps_project.settings.development')
django.setup()

from django.contrib.auth.models import User

# Superuser credentials
username = "roylaffman"
password = "Laceyjones29"
email = "roylaffman@example.com"

# Delete if exists
User.objects.filter(username=username).delete()

# Create superuser
user = User.objects.create_superuser(
    username=username,
    email=email,
    password=password
)

print(f"✓ Superuser created:")
print(f"  Username: {username}")
print(f"  Password: {password}")
print(f"  Email: {email}")
print(f"  Is superuser: {user.is_superuser}")
print(f"  Is staff: {user.is_staff}")
print(f"\nYou can now login at:")
print(f"  Frontend: http://localhost:5173")
print(f"  Admin: http://localhost:8000/admin/")
