# Backend Integration Guide

## Overview

The frontend is now integrated with the Django REST API backend. All data operations (maps, features, stories, photos) are persisted to the database.

## API Service

Located in `src/services/api.js`, provides:

### Map Operations
- `mapAPI.getAll()` - Get all accessible maps
- `mapAPI.getMyMaps()` - Get user's maps only
- `mapAPI.getPublicMaps()` - Get public maps only
- `mapAPI.getById(id)` - Get single map
- `mapAPI.create(data)` - Create new map
- `mapAPI.update(id, data)` - Update map
- `mapAPI.delete(id)` - Delete map
- `mapAPI.getFeatures(mapId)` - Get map's features

### Feature Operations
- `featureAPI.getAll(params)` - Get all features with filters
- `featureAPI.getById(id)` - Get single feature
- `featureAPI.create(data)` - Create new feature
- `featureAPI.update(id, data)` - Update feature
- `featureAPI.delete(id)` - Delete feature
- `featureAPI.getContent(id)` - Get feature's stories & photos

### Story Operations
- `storyAPI.create(data)` - Create story
- `storyAPI.update(id, data)` - Update story
- `storyAPI.delete(id)` - Delete story

### Photo Operations
- `photoAPI.upload(featureId, file, caption)` - Upload photo
- `photoAPI.update(id, data)` - Update photo metadata
- `photoAPI.delete(id)` - Delete photo

### Import Operations
- `importAPI.importGeoJSON(mapId, file)` - Import GeoJSON
- `importAPI.importKML(mapId, file)` - Import KML/KMZ
- `importAPI.importCoordinates(mapId, file, options)` - Import CSV

## Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000/api
VITE_ENV=development
```

### CORS Setup

The Django backend must allow CORS requests from the frontend. In `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:5174",
    "http://localhost:3000",
]

# Or for development:
CORS_ALLOW_ALL_ORIGINS = True
```

## Running the Full Stack

### 1. Start Django Backend

```bash
# In project root
python manage.py runserver
```

Backend will run on `http://localhost:8000`

### 2. Start React Frontend

```bash
# In frontend directory
npm run dev
```

Frontend will run on `http://localhost:5173` or `5174`

### 3. Access the Application

Open `http://localhost:5173` in your browser

## Authentication

Currently using token-based authentication (placeholder).

### Login Flow (Future)
1. User enters credentials
2. Frontend calls `authAPI.login(username, password)`
3. Token stored in localStorage
4. Token automatically included in all API requests

### Current Behavior
- App works without authentication
- All maps/features are accessible
- Need to implement user registration/login

## Data Flow

### Creating a Map
1. User fills MapCreator form
2. `handleMapCreate()` calls `mapAPI.create()`
3. Backend creates map in database
4. Frontend receives map object with ID
5. Map added to local state
6. User redirected to map view

### Creating a Feature
1. User draws on map
2. `handleFeatureCreated()` calls `featureAPI.create()`
3. Backend creates feature with geometry
4. Frontend receives feature object
5. Feature added to local state
6. FeatureEditor opens automatically

### Saving Feature Content
1. User edits feature in FeatureEditor
2. `handleFeatureSave()` updates feature
3. Creates new stories via `storyAPI.create()`
4. Uploads new photos via `photoAPI.upload()`
5. Reloads features to get updated data

## Offline Mode

The app gracefully handles API failures:

- Shows error banner when API unavailable
- Keeps existing data in state
- Allows continued interaction with loaded data
- Retries on next action

## Error Handling

All API calls wrapped in try/catch:

```javascript
try {
  const data = await mapAPI.getAll();
  setMaps(data);
} catch (err) {
  console.error('Error:', err);
  setError('Failed to load maps');
  // Keep existing data
}
```

## API Response Format

### List Responses
```json
{
  "count": 10,
  "next": "http://api/maps/?page=2",
  "previous": null,
  "results": [...]
}
```

### Single Object
```json
{
  "id": 1,
  "title": "My Map",
  "description": "...",
  ...
}
```

### Error Response
```json
{
  "detail": "Error message",
  "field_errors": {
    "title": ["This field is required"]
  }
}
```

## Testing with Backend

### 1. Create Test User

```bash
python manage.py createsuperuser
```

### 2. Create Test Data

Use Django admin at `http://localhost:8000/admin`

### 3. Test API Endpoints

```bash
# Get maps
curl http://localhost:8000/api/maps/

# Create map (requires auth)
curl -X POST http://localhost:8000/api/maps/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"title":"Test Map","center_lat":37.7749,"center_lng":-122.4194,"zoom_level":10}'
```

## Next Steps

1. ✅ API service layer created
2. ✅ App integrated with API
3. ✅ Loading states added
4. ✅ Error handling implemented
5. ⏳ Authentication UI needed
6. ⏳ Photo upload to S3 needed
7. ⏳ Real-time updates (WebSocket)
8. ⏳ Offline sync capability

## Troubleshooting

### CORS Errors
- Check Django CORS settings
- Verify frontend URL in CORS_ALLOWED_ORIGINS
- Check browser console for specific error

### 404 Errors
- Verify Django server is running
- Check API_BASE_URL in .env
- Verify URL patterns in Django urls.py

### Authentication Errors
- Check token in localStorage
- Verify token is valid
- Check Authorization header format

### Data Not Loading
- Check browser console for errors
- Verify Django migrations are applied
- Check database has data
- Test API endpoints directly

## Development Tips

- Use browser DevTools Network tab to inspect API calls
- Check Django console for backend errors
- Use `console.log()` to debug data flow
- Test API endpoints with curl or Postman first
