# Testing Guide - Personal Memory Maps

## Quick Start Testing

### 1. Start the Backend

```bash
# Make sure you're in the project root
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### 2. Start the Frontend

Open a **new terminal** and run:

```bash
cd frontend
npm run dev
```

You should see:
```
VITE ready in XXXms
Local: http://localhost:5173/
```

### 3. Open the App

Navigate to `http://localhost:5173` in your browser

## Testing Checklist

### ✅ Map Management
- [ ] Create a new map
- [ ] See the map in the gallery
- [ ] Open the map
- [ ] Edit map visibility (public/private)
- [ ] Delete a map
- [ ] Search for maps

### ✅ Feature Creation
- [ ] Draw a point (marker)
- [ ] Draw a line (polyline)
- [ ] Draw a polygon
- [ ] Draw a rectangle
- [ ] See features appear on map

### ✅ Feature Editing
- [ ] Click a feature to see popup
- [ ] Click "Edit" to open editor
- [ ] Change title and description
- [ ] Add a category
- [ ] Save changes
- [ ] Verify changes persist

### ✅ Content Management
- [ ] Add a story to a feature
- [ ] Add multiple stories
- [ ] Upload a photo
- [ ] Add photo caption
- [ ] Remove a story
- [ ] Remove a photo

### ✅ File Import
- [ ] Click "Import" button
- [ ] Select a GeoJSON file
- [ ] See features imported
- [ ] Try a KML file
- [ ] Verify imported features are editable

### ✅ Data Persistence
- [ ] Create some features
- [ ] Refresh the page
- [ ] Verify features are still there
- [ ] Close browser
- [ ] Reopen and check data persists

### ✅ Drawing Tools
- [ ] Use edit mode to drag vertices
- [ ] Move a marker
- [ ] Reshape a polygon
- [ ] Delete features via drawing controls

## Common Issues & Solutions

### Backend Not Starting

**Issue:** `ModuleNotFoundError` or import errors

**Solution:**
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Frontend Not Starting

**Issue:** `npm` command not found

**Solution:**
```bash
# Install Node.js from nodejs.org
# Then install dependencies
cd frontend
npm install
```

### CORS Errors

**Issue:** Browser console shows CORS errors

**Solution:** Check `memory_maps_project/settings/base.py`:
```python
CORS_ALLOW_ALL_ORIGINS = True  # For development
```

### Database Errors

**Issue:** `relation does not exist` errors

**Solution:**
```bash
# Run migrations
python manage.py migrate
```

### Features Not Saving

**Issue:** Features disappear after refresh

**Solution:**
1. Check Django console for errors
2. Verify backend is running
3. Check browser console for API errors
4. Verify `.env` file has correct API_URL

## Testing with Sample Data

### Create Test User

```bash
python manage.py createsuperuser
# Follow prompts to create admin user
```

### Access Django Admin

Navigate to `http://localhost:8000/admin`
- Login with superuser credentials
- Create test maps and features
- View data in database

### Test API Directly

```bash
# Get all maps
curl http://localhost:8000/api/maps/

# Get all features
curl http://localhost:8000/api/features/
```

## Performance Testing

### Test with Many Features

1. Import a large GeoJSON file
2. Verify map renders smoothly
3. Test zooming and panning
4. Check feature popups work

### Test with Photos

1. Upload multiple photos
2. Verify thumbnails load
3. Check photo captions display
4. Test photo removal

## Browser Testing

Test in multiple browsers:
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari
- [ ] Mobile browsers

## Mobile Testing

1. Open on mobile device
2. Test touch interactions
3. Verify responsive design
4. Test drawing on touch screen

## Next Steps After Testing

Once basic functionality works:

1. **Authentication** - Add user login/registration
2. **Photo Storage** - Configure S3 for photo uploads
3. **Performance** - Optimize for large datasets
4. **Deployment** - Deploy to production server

## Reporting Issues

If you find bugs:

1. Check browser console for errors
2. Check Django console for backend errors
3. Note steps to reproduce
4. Check if issue persists after refresh
5. Try in different browser

## Success Criteria

The app is working correctly when:

✅ Maps persist across sessions
✅ Features save to database
✅ Photos upload successfully
✅ Stories are saved
✅ Import works for GeoJSON/KML
✅ Edit mode works smoothly
✅ No console errors
✅ Data loads quickly
✅ UI is responsive

## Development Workflow

1. Make changes to code
2. Frontend auto-reloads (HMR)
3. Backend requires restart for Python changes
4. Test changes in browser
5. Check console for errors
6. Commit working changes

Happy testing! 🗺️
