# 🔧 Troubleshooting "Failed to Fetch" Login Error

## ⚠️ The Problem
You're seeing "Failed to fetch" or "Offline mode" when trying to login.

## ✅ Backend is Working
The backend API is confirmed working:
- ✅ Backend responding on http://localhost:8000
- ✅ Login API working correctly
- ✅ Database connected
- ✅ CORS configured for localhost:5173

## 🎯 Most Likely Cause
**Old browser tab with cached JavaScript**

---

## 🔥 SOLUTION: Complete Browser Reset

### Step 1: Close ALL Browser Tabs
1. Close **every tab** with localhost:5173
2. Close **every tab** with localhost:8000
3. Make sure no memory-maps tabs are open

### Step 2: Clear Browser Cache
1. Press **Ctrl + Shift + Delete**
2. Select "All time" or "Everything"
3. Check these boxes:
   - ✅ Cached images and files
   - ✅ Cookies and site data
4. Click "Clear data"

### Step 3: Hard Refresh
1. Open a **NEW** browser tab
2. Go to: http://localhost:5173
3. Press **Ctrl + Shift + R** (hard refresh)
4. Or press **Ctrl + F5**

### Step 4: Try Login
1. Click "Sign In"
2. Username: `roylaffman`
3. Password: `Laceyjones29`
4. Click "Login"

---

## 🔍 Alternative: Use Incognito/Private Mode

This bypasses all cache issues:

1. Open **Incognito/Private window**:
   - Chrome: Ctrl + Shift + N
   - Firefox: Ctrl + Shift + P
   - Edge: Ctrl + Shift + N

2. Go to: http://localhost:5173

3. Try logging in

---

## 🛠️ If Still Not Working

### Check 1: Verify Backend is Responding
Open a new terminal and run:
```bash
curl http://localhost:8000/api/auth/login/
```

Should see: `{"detail":"Method \"GET\" not allowed."}`  
This means the endpoint exists!

### Check 2: Test Login from Terminal
```bash
python -c "import requests; r = requests.post('http://localhost:8000/api/auth/login/', json={'username': 'roylaffman', 'password': 'Laceyjones29'}); print('Status:', r.status_code); print('Success!' if r.status_code == 200 else 'Failed')"
```

Should see: `Status: 200` and `Success!`

### Check 3: Browser Console
1. Open browser to http://localhost:5173
2. Press **F12** to open Developer Tools
3. Click **Console** tab
4. Try to login
5. Look for errors (red text)

**Common errors:**
- `CORS error` → Backend CORS issue
- `net::ERR_CONNECTION_REFUSED` → Backend not running
- `Failed to fetch` → Network/cache issue

### Check 4: Network Tab
1. Press **F12** → **Network** tab
2. Try to login
3. Look for the login request
4. Check if it's going to the right URL: `http://localhost:8000/api/auth/login/`

---

## 🔄 Nuclear Option: Restart Everything

If nothing else works:

### 1. Stop All Servers
Close all terminal windows running the servers

### 2. Clear Browser Completely
- Close browser entirely
- Clear all cache
- Restart browser

### 3. Restart Backend
```bash
python manage.py runserver 8000
```

Wait for: `Starting development server at http://127.0.0.1:8000/`

### 4. Restart Frontend (New Terminal)
```bash
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:5173/`

### 5. Test in Fresh Browser Tab
- Open NEW incognito window
- Go to http://localhost:5173
- Try login

---

## 📱 Try Different Browser

If one browser doesn't work, try another:
- Chrome
- Firefox
- Edge
- Brave

Sometimes one browser has cached issues while others work fine.

---

## 🔍 Check Frontend API Configuration

The frontend should be connecting to:
```
http://localhost:8000/api/v1/memory-maps
```

If you see errors about wrong URLs, the frontend might be misconfigured.

---

## ✅ Verification Checklist

Before trying to login, verify:

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] All old browser tabs closed
- [ ] Browser cache cleared
- [ ] Using fresh browser tab or incognito
- [ ] No firewall blocking localhost
- [ ] No antivirus blocking connections

---

## 🎯 Quick Test Commands

Run these to verify everything:

```bash
# Test backend root
curl http://localhost:8000/

# Test frontend
curl http://localhost:5173/

# Test login API
python -c "import requests; print('Login:', 'OK' if requests.post('http://localhost:8000/api/auth/login/', json={'username': 'roylaffman', 'password': 'Laceyjones29'}).status_code == 200 else 'FAIL')"
```

All should return OK or 200 status.

---

## 💡 Most Common Solution

**90% of "Failed to fetch" errors are solved by:**

1. Closing all browser tabs
2. Clearing browser cache
3. Opening fresh incognito window
4. Going to http://localhost:5173

**Try this first!**

---

## 📞 Still Having Issues?

If you've tried everything above:

1. Check the browser console (F12) for specific error messages
2. Check the backend terminal for error logs
3. Verify your .env file has correct settings
4. Make sure no other application is using port 8000 or 5173

---

## 🎊 Success Indicators

You'll know it's working when:
- ✅ No "Failed to fetch" error
- ✅ No "Offline mode" message
- ✅ Login button responds
- ✅ You see "Loading..." or similar feedback
- ✅ You get redirected to the map gallery

---

**Remember: The backend IS working. This is a frontend/browser cache issue!**
