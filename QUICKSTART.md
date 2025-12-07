# Quick Start Guide - Personal Memory Maps

## Get Up and Running in 5 Minutes

### Prerequisites
- Python 3.8+ with virtual environment
- Node.js 16+ with npm
- PostgreSQL with PostGIS extension
- GDAL library installed

### 1. Start the Backend (Terminal 1)

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Start Django server
python manage.py runserver 8000
```

Backend will be available at: `http://localhost:8000`

### 2. Start the Frontend (Terminal 2)

```bash
# Navigate to frontend directory
cd frontend

# Start Vite dev server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

### 3. Create Test User (Terminal 3)

```bash
# Activate virtual environment
venv\Scripts\activate

# Create test user
python create_test_user.py
```

Test credentials:
- **Username**: testuser
- **Password**: testpass123

### 4. Open the Application

1. Open browser to `http://localhost:5173`
2. Click "Sign In" button
3. Login with test credentials
4. Click "Create New Map"
5. Fill in map details and click "Create Map"
6. Use drawing tools to add features:
   - 📍 Point marker
   - ⬜ Polygon
   - 📏 Line
7. Click features to view/edit attributes
8. Add stories and photos to features

## Quick Test

Run the automated integration test:

```bash
python test_feature_integration.py
```

Expected output:
```
============================================================
✓ ALL TESTS PASSED!
============================================================
```

## Common Tasks

### Create a Point Feature
1. Click the marker icon in drawing toolbar
2. Click on map where you want the point
3. Feature editor opens automatically
4. Add title, description, category
5. Click "Save Changes"

### Add a Story
1. Click an existing feature on the map
2. Click "Edit" in the popup
3. Click "+ Add Story" button
4. Enter story title and content
5. Click "Save Story"
6. Click "Save Changes" to close editor

### Upload Photos
1. Click feature and click "Edit"
2. Click "📷 Add Photos" button
3. Select one or more images
4. Add captions (optional)
5. Click "Save Changes"

### Create a Polygon
1. Click the polygon icon in drawing toolbar
2. Click points on map to define corners
3. Click first point again to close polygon
4. Feature editor opens automatically
5. Add details and save

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running
- Verify database connection in `.env`
- Run migrations: `python manage.py migrate`

### Frontend won't start
- Check Node.js version: `node --version`
- Reinstall dependencies: `npm install`
- Clear cache: `npm run build --force`

### Can't login
- Verify test user exists: `python create_test_user.py`
- Check backend is running on port 8000
- Check browser console for errors

### Features not appearing
- Check browser console for errors
- Verify you're logged in
- Refresh the page
- Check backend logs for errors

## API Endpoints

### Authentication
- Login: `POST /api/auth/login/`
- Get User: `GET /api/auth/user/`
- Logout: `POST /api/auth/logout/`

### Maps
- List: `GET /api/v1/memory-maps/maps/`
- Create: `POST /api/v1/memory-maps/maps/`
- Get: `GET /api/v1/memory-maps/maps/{id}/`
- Update: `PATCH /api/v1/memory-maps/maps/{id}/`
- Delete: `DELETE /api/v1/memory-maps/maps/{id}/`

### Features
- Create: `POST /api/v1/memory-maps/features/`
- Get: `GET /api/v1/memory-maps/features/{id}/`
- Update: `PATCH /api/v1/memory-maps/features/{id}/`
- Delete: `DELETE /api/v1/memory-maps/features/{id}/`

### Content
- Create Story: `POST /api/v1/memory-maps/stories/`
- Upload Photo: `POST /api/v1/memory-maps/photos/`

## File Structure

```
memory-maps/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API service layer
│   │   └── App.jsx          # Main app component
│   └── package.json
├── memory_maps/             # Django app
│   ├── models.py           # Database models
│   ├── views.py            # API views
│   ├── serializers.py      # DRF serializers
│   └── urls.py             # URL routing
├── memory_maps_project/     # Django project
│   ├── settings/           # Settings files
│   └── urls.py             # Main URL config
├── manage.py               # Django management
└── requirements.txt        # Python dependencies
```

## Key Features

✅ **Interactive Map**: Leaflet-based map with drawing tools
✅ **Spatial Features**: Points, lines, and polygons
✅ **Rich Attributes**: Title, description, category for each feature
✅ **Content Attachment**: Stories and photos linked to features
✅ **User Authentication**: Secure JWT-based auth
✅ **Permission Control**: Public/private maps, owner-only editing
✅ **Real-time Updates**: Changes reflect immediately
✅ **Responsive Design**: Works on desktop and mobile

## Development Workflow

1. Make changes to backend code
2. Django auto-reloads (no restart needed)
3. Make changes to frontend code
4. Vite hot-reloads (instant updates)
5. Test in browser
6. Run integration tests
7. Commit changes

## Documentation

- **Feature Creation Guide**: `FEATURE_CREATION_GUIDE.md`
- **Integration Verification**: `INTEGRATION_VERIFICATION.md`
- **Testing Guide**: `TESTING_GUIDE.md`
- **Project Summary**: `PROJECT_SUMMARY.md`

## Support

For issues or questions:
1. Check browser console for errors
2. Check Django server logs
3. Review documentation files
4. Run integration test to verify setup

## What's Working

✅ User authentication and session management
✅ Map creation and management
✅ Feature creation (points, lines, polygons)
✅ Attribute editing (title, description, category)
✅ Story creation and display
✅ Photo upload and display
✅ Feature popups with full details
✅ Map gallery with search
✅ Public/private map sharing
✅ Permission-based access control

## Next Features

The following features are planned but not yet implemented:
- File import (GeoJSON, KML, CSV)
- AWS deployment
- Performance optimization
- External tile services

## Tips

- Use Ctrl+Z to undo drawing actions
- Click features to see their attributes
- Use the search bar to filter maps
- Toggle map visibility with the eye icon
- Photos are limited to 10MB each
- Polygons must be closed (first point = last point)

## Happy Mapping! 🗺️
