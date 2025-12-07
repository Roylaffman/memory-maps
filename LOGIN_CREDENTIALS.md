# Login Credentials

## Test User Account

**Username:** `testuser`  
**Password:** `testpass123`  
**Email:** `test@example.com`

## How to Login

### Via Web Interface (http://localhost:5173)

1. Open your browser to http://localhost:5173
2. Click the "Sign In" button in the top right
3. Enter the credentials:
   - Username: `testuser`
   - Password: `testpass123`
4. Click "Login"

### Via API (for testing)

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

## Troubleshooting

### If login doesn't work:

1. **Recreate the test user:**
   ```bash
   python create_test_user.py
   ```

2. **Check backend is running:**
   - Backend should be at: http://localhost:8000
   - Test: http://localhost:8000/api/auth/login/

3. **Check frontend is running:**
   - Frontend should be at: http://localhost:5173

4. **Clear browser cache:**
   - Press Ctrl+Shift+Delete
   - Clear cached images and files
   - Reload the page

5. **Check browser console:**
   - Press F12 to open developer tools
   - Look for any error messages in the Console tab
   - Check the Network tab for failed requests

### Common Issues

**"Invalid credentials"**
- Make sure you're typing the password exactly: `testpass123`
- Username is case-sensitive: `testuser` (all lowercase)

**"Network error"**
- Backend server might not be running
- Check that http://localhost:8000 is accessible

**"CORS error"**
- Backend CORS settings should allow localhost:5173
- Check memory_maps_project/settings/development.py

## Creating Additional Users

### Via Django Admin

1. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

2. Access admin at: http://localhost:8000/admin/

3. Create new users through the admin interface

### Via Python Script

Create a new user programmatically:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memory_maps_project.settings.development')
django.setup()

from django.contrib.auth.models import User

user = User.objects.create_user(
    username='newuser',
    email='newuser@example.com',
    password='newpassword123'
)
print(f"Created user: {user.username}")
```

## Current Status

✅ Test user created and verified
✅ Backend authentication working
✅ JWT tokens being generated correctly
✅ Ready to login via web interface

## Quick Test

Run this to verify login works:
```bash
python -c "import requests; r = requests.post('http://localhost:8000/api/auth/login/', json={'username': 'testuser', 'password': 'testpass123'}); print('✓ Login works!' if r.status_code == 200 else '✗ Login failed')"
```
