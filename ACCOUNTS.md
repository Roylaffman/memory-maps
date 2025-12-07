# Personal Memory Maps - Account Information

## 🔐 Your Accounts

### Superuser Account (Full Admin Access)
**Username:** `roylaffman`  
**Password:** `Laceyjones29`  
**Email:** `roylaffman@example.com`  
**Permissions:** Full admin access, can manage all users and data

**Access:**
- Frontend: http://localhost:5173
- Django Admin: http://localhost:8000/admin/

---

### Test User Account (Standard User)
**Username:** `testuser`  
**Password:** `testpass123`  
**Email:** `test@example.com`  
**Permissions:** Standard user, can create and manage own maps

**Access:**
- Frontend: http://localhost:5173

---

## 🚀 Quick Start

### 1. Access the Application
Open your browser to: **http://localhost:5173**

### 2. Login
Click "Sign In" and use either account above.

### 3. Start Creating
- Click "Create New Map"
- Draw features (points, lines, polygons)
- Add stories and photos
- Import GeoJSON/KML/CSV files

---

## 🔧 Backend & Database

### Backend API
- **URL:** http://localhost:8000
- **API Base:** http://localhost:8000/api/v1/memory-maps/
- **Auth:** http://localhost:8000/api/auth/
- **Status:** ✅ Running

### Database
- **Type:** PostgreSQL with PostGIS
- **Connection:** Configured in `.env` file
- **Status:** ✅ Connected

---

## 📝 How to Login

### Via Web Interface
1. Go to http://localhost:5173
2. Click "Sign In" button (top right)
3. Enter username and password
4. Click "Login"

### Via Django Admin
1. Go to http://localhost:8000/admin/
2. Login with superuser credentials
3. Manage users, maps, and features

---

## 🔄 Recreate Accounts

If you need to recreate accounts:

### Recreate Superuser
```bash
python create_superuser.py
```

### Recreate Test User
```bash
python create_test_user.py
```

---

## ✅ Verification

Test that everything is working:

```bash
# Test backend is running
curl http://localhost:8000/

# Test login works
python -c "import requests; r = requests.post('http://localhost:8000/api/auth/login/', json={'username': 'roylaffman', 'password': 'Laceyjones29'}); print('✓ Login works!' if r.status_code == 200 else '✗ Login failed')"
```

---

## 🌐 Server Status

### Backend (Django)
- **Port:** 8000
- **URL:** http://localhost:8000
- **Status:** ✅ Running
- **Process ID:** Check with `python manage.py runserver 8000`

### Frontend (React + Vite)
- **Port:** 5173
- **URL:** http://localhost:5173
- **Status:** ✅ Running
- **Hot Reload:** Enabled

---

## 🐛 Troubleshooting

### "Failed to fetch" or "Offline mode"
**Problem:** Frontend can't connect to backend

**Solutions:**
1. Check backend is running:
   ```bash
   curl http://localhost:8000/
   ```

2. Restart backend:
   ```bash
   python manage.py runserver 8000
   ```

3. Check CORS settings in `memory_maps_project/settings/development.py`

### "Invalid credentials"
**Problem:** Login fails

**Solutions:**
1. Verify you're using the correct password (case-sensitive)
2. Recreate the user:
   ```bash
   python create_superuser.py
   ```

3. Check backend logs for errors

### Backend won't start
**Problem:** Port 8000 already in use

**Solutions:**
1. Kill existing process:
   ```bash
   # Find process on port 8000
   netstat -ano | findstr :8000
   # Kill it (replace PID with actual process ID)
   taskkill /PID <PID> /F
   ```

2. Use different port:
   ```bash
   python manage.py runserver 8001
   ```

---

## 📊 Current Status

✅ Backend server running on port 8000  
✅ Frontend server running on port 5173  
✅ Database connected and migrations applied  
✅ Superuser account created: `roylaffman`  
✅ Test user account created: `testuser`  
✅ Authentication working (JWT tokens)  
✅ API endpoints responding  

---

## 🎯 What You Can Do Now

1. **Create Maps** - Design custom memory maps
2. **Draw Features** - Add points, lines, and polygons
3. **Add Content** - Attach stories and photos to features
4. **Import Data** - Upload GeoJSON, KML, or CSV files
5. **Share Maps** - Make maps public or keep them private
6. **Manage Users** - Use Django admin to manage accounts

---

## 📞 Need Help?

If you encounter issues:

1. Check this document for troubleshooting steps
2. Review `QUICKSTART.md` for setup instructions
3. Check `FEATURE_CREATION_GUIDE.md` for usage details
4. Look at `INTEGRATION_VERIFICATION.md` for test results

---

**Last Updated:** December 7, 2025  
**Status:** ✅ All systems operational
