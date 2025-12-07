# Personal Memory Maps - Private Credentials
**⚠️ CONFIDENTIAL - Keep this file secure and private**

---

## 🗄️ PostgreSQL Database Credentials

### Master PostgreSQL Account
**Username:** `postgres`  
**Password:** `password`  
**Access:** All PostgreSQL databases on the system

### Memory Maps Database User
**Username:** `rlafferty`  
**Password:** `laceyjones29`  
**Database:** `memory_maps`  
**Created:** December 6, 2025

**Connection String:**
```
postgresql://rlafferty:laceyjones29@localhost:5432/memory_maps
```

**Create User Command:**
```sql
psql -U postgres -c "CREATE USER rlafferty WITH PASSWORD 'laceyjones29';"
```

---

## 👤 Django Admin Accounts

### Superuser Account #1 (Primary Admin)
**Username:** `roylaffman`  
**Password:** `Laceyjones29`  
**Email:** `roylaffman@example.com`  
**Permissions:** Full superuser and staff access  
**Created:** December 6, 2025

**Access:**
- Django Admin: http://localhost:8000/admin/
- Frontend App: http://localhost:5173

---

## 🌐 Memory Maps Application Users

### User #1 - Primary Developer Account
**Username:** `roylaffman`  
**Password:** `Laceyjones20`  
**Email:** `roylaffman@gmail.com`  
**Type:** Developer/Admin account  
**Purpose:** Primary development and testing

### User #2 - Database Admin
**Username:** `rlafferty`  
**Password:** `Laceyjones29`  
**Type:** Database administrator account  
**Purpose:** Database management and operations

### User #3 - Test Account
**Username:** `testuser`  
**Password:** `testpass123`  
**Email:** `test@example.com`  
**Type:** Standard test user  
**Purpose:** Testing standard user functionality

---

## 🔗 Connection Information

### Backend API
- **Base URL:** http://localhost:8000
- **API Endpoint:** http://localhost:8000/api/v1/memory-maps/
- **Auth Endpoint:** http://localhost:8000/api/auth/
- **Admin Panel:** http://localhost:8000/admin/

### Frontend Application
- **URL:** http://localhost:5173
- **Dev Server:** Vite (React)

### Database
- **Host:** localhost
- **Port:** 5432
- **Database Name:** memory_maps
- **Type:** PostgreSQL with PostGIS extension

---

## 🔐 Account Summary Table

| Account Type | Username | Password | Email | Access Level |
|-------------|----------|----------|-------|--------------|
| PostgreSQL Master | postgres | password | - | Full DB Access |
| PostgreSQL User | rlafferty | laceyjones29 | - | memory_maps DB |
| Django Superuser | roylaffman | Laceyjones29 | roylaffman@example.com | Full Admin |
| App User (Dev) | roylaffman | Laceyjones20 | roylaffman@gmail.com | Standard User |
| App User (DB Admin) | rlafferty | Laceyjones29 | - | Standard User |
| App User (Test) | testuser | testpass123 | test@example.com | Standard User |

---

## 🚀 Quick Login Guide

### To Access Django Admin:
1. Go to http://localhost:8000/admin/
2. Username: `roylaffman`
3. Password: `Laceyjones29`

### To Access Frontend App:
1. Go to http://localhost:5173
2. Click "Sign In"
3. Use any of the app user accounts above

### To Access PostgreSQL:
```bash
# As postgres superuser
psql -U postgres -d memory_maps

# As rlafferty user
psql -U rlafferty -d memory_maps
```

---

## 🔄 Recreate Accounts

### Recreate Django Superuser
```bash
python create_superuser.py
```

### Recreate Test User
```bash
python create_test_user.py
```

### Recreate PostgreSQL User
```sql
psql -U postgres
DROP USER IF EXISTS rlafferty;
CREATE USER rlafferty WITH PASSWORD 'laceyjones29';
GRANT ALL PRIVILEGES ON DATABASE memory_maps TO rlafferty;
```

---

## 🛠️ Troubleshooting Connection Issues

### "Failed to fetch" Error

**Possible Causes:**
1. Backend server not running
2. Frontend connecting to wrong URL
3. CORS configuration issue
4. Old browser cache

**Solutions:**

1. **Verify Backend is Running:**
```bash
curl http://localhost:8000/
```

2. **Check Database Connection:**
```bash
python manage.py dbshell
```

3. **Test Login API:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "roylaffman", "password": "Laceyjones29"}'
```

4. **Clear Browser Cache:**
- Press Ctrl+Shift+Delete
- Clear all cached data
- Reload page

5. **Restart All Services:**
```bash
# Stop all processes
# Then restart:
python manage.py runserver 8000
cd frontend && npm run dev
```

---

## 📝 Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://rlafferty:laceyjones29@localhost:5432/memory_maps
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api/v1/memory-maps
VITE_ENV=development
```

---

## 🔒 Security Notes

1. **Never commit this file to version control**
2. **Keep passwords secure and private**
3. **Change default passwords in production**
4. **Use environment variables for sensitive data**
5. **Enable HTTPS in production**
6. **Restrict database access by IP in production**

---

## 📊 System Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (React + Vite)         │
│         http://localhost:5173           │
└──────────────┬──────────────────────────┘
               │ HTTP/REST API
               ▼
┌─────────────────────────────────────────┐
│      Backend (Django + DRF)             │
│      http://localhost:8000              │
│                                         │
│  - JWT Authentication                   │
│  - REST API Endpoints                   │
│  - File Upload/Import                   │
└──────────────┬──────────────────────────┘
               │ PostgreSQL Connection
               ▼
┌─────────────────────────────────────────┐
│   PostgreSQL + PostGIS Database         │
│   localhost:5432/memory_maps            │
│                                         │
│  - User: rlafferty                      │
│  - Spatial data storage                 │
│  - GIS operations                       │
└─────────────────────────────────────────┘
```

---

## ✅ Verification Checklist

- [ ] PostgreSQL is running
- [ ] Database `memory_maps` exists
- [ ] User `rlafferty` has access to database
- [ ] Django migrations are applied
- [ ] Superuser `roylaffman` exists
- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Can login to Django admin
- [ ] Can login to frontend app
- [ ] API endpoints respond correctly

---

## 🔧 Maintenance Commands

### Check Database Connection
```bash
python manage.py dbshell
```

### List All Users
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()
```

### Reset User Password
```bash
python manage.py changepassword roylaffman
```

### Check Migrations
```bash
python manage.py showmigrations
```

### Create Database Backup
```bash
pg_dump -U rlafferty memory_maps > backup.sql
```

---

**Document Created:** December 7, 2025  
**Last Updated:** December 7, 2025  
**Status:** Active and Current

**⚠️ REMINDER: Keep this document secure and do not share publicly**
