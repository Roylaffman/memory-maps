# Feature Creation and Attribute Reading Guide

## Overview

This guide documents the complete workflow for creating map features and reading their attributes in the Personal Memory Maps application. The system has been tested end-to-end and is fully functional.

## System Status

✅ **Backend API**: Fully functional
✅ **Frontend UI**: Fully functional  
✅ **Authentication**: JWT-based auth working
✅ **Feature Creation**: Points, lines, and polygons supported
✅ **Attribute Management**: Full CRUD operations
✅ **Content Attachment**: Stories and photos supported

## Architecture

### Backend (Django + PostGIS)
- **API Base URL**: `http://localhost:8000/api/v1/memory-maps/`
- **Auth URL**: `http://localhost:8000/api/auth/`
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: PostgreSQL with PostGIS extension

### Frontend (React + Leaflet)
- **Dev Server**: `http://localhost:5173/`
- **Map Library**: Leaflet with drawing tools
- **State Management**: React hooks

## Feature Creation Workflow

### 1. User Authentication

**Login Process:**
```javascript
// Frontend API call
const response = await authAPI.login(username, password);
// Returns: { token, user }
```

**Backend Endpoint:**
- `POST /api/auth/login/`
- Request: `{ username, password }`
- Response: `{ access, refresh }` (JWT tokens)

### 2. Create a Map

**Frontend:**
```javascript
const mapData = {
  title: "My Memory Map",
  description: "A collection of special places",
  center_lat: 37.7749,
  center_lng: -122.4194,
  zoom_level: 12,
  is_public: false
};

const newMap = await mapAPI.create(mapData);
```

**Backend Endpoint:**
- `POST /api/v1/memory-maps/maps/`
- Requires authentication
- Auto-assigns owner to current user

### 3. Create Features

#### Point Feature (Marker)
```javascript
const pointFeature = {
  map: mapId,
  feature_type: "point",
  geometry: {
    type: "Point",
    coordinates: [longitude, latitude]  // Note: [lng, lat] order
  },
  title: "Golden Gate Park",
  description: "A beautiful urban park",
  category: "Park"
};

const feature = await featureAPI.create(pointFeature);
```

#### Polygon Feature
```javascript
const polygonFeature = {
  map: mapId,
  feature_type: "polygon",
  geometry: {
    type: "Polygon",
    coordinates: [[
      [lng1, lat1],
      [lng2, lat2],
      [lng3, lat3],
      [lng4, lat4],
      [lng1, lat1]  // Close the polygon
    ]]
  },
  title: "Neighborhood Area",
  description: "Residential neighborhood",
  category: "Residential"
};
```

#### Line Feature (Polyline)
```javascript
const lineFeature = {
  map: mapId,
  feature_type: "line",
  geometry: {
    type: "LineString",
    coordinates: [
      [lng1, lat1],
      [lng2, lat2],
      [lng3, lat3]
    ]
  },
  title: "Walking Trail",
  description: "Scenic trail through the park",
  category: "Trail"
};
```

**Backend Endpoint:**
- `POST /api/v1/memory-maps/features/`
- Validates user owns the map
- Stores geometry in PostGIS format

### 4. Read Feature Attributes

#### Get Single Feature
```javascript
const feature = await featureAPI.getById(featureId);

// Returns:
{
  id: 5,
  map: 3,
  feature_type: "point",
  geometry: {
    type: "Point",
    coordinates: [-122.4194, 37.7749]
  },
  title: "Golden Gate Park",
  description: "A beautiful urban park",
  category: "Park",
  story_count: 1,
  photo_count: 2,
  stories: [...],
  photos: [...],
  created_at: "2025-11-30T20:00:00Z",
  updated_at: "2025-11-30T20:05:00Z"
}
```

#### Get All Features for a Map
```javascript
const features = await mapAPI.getFeatures(mapId);
// Returns array of features
```

**Backend Endpoints:**
- `GET /api/v1/memory-maps/features/{id}/` - Single feature with full details
- `GET /api/v1/memory-maps/maps/{id}/features/` - All features for a map

### 5. Update Feature Attributes

```javascript
const updates = {
  title: "Updated Title",
  description: "Updated description",
  category: "New Category"
};

const updatedFeature = await featureAPI.update(featureId, updates);
```

**Backend Endpoint:**
- `PATCH /api/v1/memory-maps/features/{id}/`
- Only owner can update

### 6. Add Content to Features

#### Add a Story
```javascript
const story = {
  feature: featureId,
  title: "My Visit",
  content: "I visited this place on a sunny day..."
};

const newStory = await storyAPI.create(story);
```

**Backend Endpoint:**
- `POST /api/v1/memory-maps/stories/`
- Auto-assigns author to current user

#### Upload a Photo
```javascript
const formData = new FormData();
formData.append('feature', featureId);
formData.append('image', fileObject);
formData.append('caption', 'Beautiful sunset');

const photo = await photoAPI.upload(featureId, fileObject, caption);
```

**Backend Endpoint:**
- `POST /api/v1/memory-maps/photos/`
- Handles multipart/form-data
- Auto-assigns uploader to current user

### 7. Display Features on Map

The frontend automatically renders features based on their type:

**Point Features:**
- Rendered as Leaflet markers
- Click to show popup with attributes

**Polygon Features:**
- Rendered as filled polygons
- Blue outline with semi-transparent fill
- Click to show popup

**Line Features:**
- Rendered as polylines
- Blue line with configurable width
- Click to show popup

**Feature Popup Contents:**
- Title and category badge
- Description
- Photo thumbnails (up to 3 shown)
- Story previews (up to 2 shown)
- Edit and Delete buttons

## UI Components

### MapView Component
- Main map container using Leaflet
- Handles map initialization and center/zoom
- Provides context for child components

### DrawingControls Component
- Leaflet.draw integration
- Allows drawing points, lines, and polygons
- Automatically creates features on draw completion

### MapFeatures Component
- Renders all features for current map
- Handles different geometry types
- Manages feature popups

### FeatureEditor Component
- Modal form for editing feature details
- Photo upload with preview
- Story creation and management
- Saves all changes to backend

### FeaturePopup Component
- Displays feature information in popup
- Shows title, description, category
- Displays photos and stories
- Edit and delete actions

## Data Flow

```
User Action (Draw/Click)
    ↓
Frontend Component (DrawingControls/FeatureEditor)
    ↓
API Service (featureAPI.create/update)
    ↓
Django REST API (MapFeatureViewSet)
    ↓
PostGIS Database (geometry storage)
    ↓
Response with Feature Data
    ↓
Frontend State Update (setFeatures)
    ↓
Map Re-render (MapFeatures component)
    ↓
Visual Update (Leaflet markers/polygons)
```

## Testing

### Integration Test
Run the complete integration test:
```bash
python test_feature_integration.py
```

This tests:
1. Authentication
2. Map creation
3. Point feature creation
4. Polygon feature creation
5. Story attachment
6. Feature retrieval with attributes
7. Feature listing
8. Feature updates
9. Cleanup

### Manual Testing

1. **Start Backend:**
   ```bash
   python manage.py runserver 8000
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access Application:**
   - Open `http://localhost:5173/`
   - Click "Sign In" and login with test credentials
   - Create a new map
   - Use drawing tools to add features
   - Click features to view/edit attributes
   - Add stories and photos

## Test Credentials

**Username:** testuser  
**Password:** testpass123

Create test user:
```bash
python create_test_user.py
```

## API Endpoints Reference

### Authentication
- `POST /api/auth/login/` - Login (get JWT tokens)
- `POST /api/auth/refresh/` - Refresh access token
- `GET /api/auth/user/` - Get current user
- `POST /api/auth/logout/` - Logout

### Maps
- `GET /api/v1/memory-maps/maps/` - List all accessible maps
- `POST /api/v1/memory-maps/maps/` - Create new map
- `GET /api/v1/memory-maps/maps/{id}/` - Get map details
- `PATCH /api/v1/memory-maps/maps/{id}/` - Update map
- `DELETE /api/v1/memory-maps/maps/{id}/` - Delete map
- `GET /api/v1/memory-maps/maps/{id}/features/` - Get all features for map

### Features
- `GET /api/v1/memory-maps/features/` - List all accessible features
- `POST /api/v1/memory-maps/features/` - Create new feature
- `GET /api/v1/memory-maps/features/{id}/` - Get feature details
- `PATCH /api/v1/memory-maps/features/{id}/` - Update feature
- `DELETE /api/v1/memory-maps/features/{id}/` - Delete feature
- `GET /api/v1/memory-maps/features/{id}/content/` - Get all content (stories + photos)

### Stories
- `GET /api/v1/memory-maps/stories/` - List all accessible stories
- `POST /api/v1/memory-maps/stories/` - Create new story
- `GET /api/v1/memory-maps/stories/{id}/` - Get story details
- `PATCH /api/v1/memory-maps/stories/{id}/` - Update story
- `DELETE /api/v1/memory-maps/stories/{id}/` - Delete story

### Photos
- `GET /api/v1/memory-maps/photos/` - List all accessible photos
- `POST /api/v1/memory-maps/photos/` - Upload new photo
- `GET /api/v1/memory-maps/photos/{id}/` - Get photo details
- `PATCH /api/v1/memory-maps/photos/{id}/` - Update photo caption
- `DELETE /api/v1/memory-maps/photos/{id}/` - Delete photo

## Geometry Format

All geometries use GeoJSON format with **[longitude, latitude]** coordinate order:

```javascript
// Point
{
  type: "Point",
  coordinates: [lng, lat]
}

// LineString
{
  type: "LineString",
  coordinates: [[lng1, lat1], [lng2, lat2], ...]
}

// Polygon
{
  type: "Polygon",
  coordinates: [
    [[lng1, lat1], [lng2, lat2], [lng3, lat3], [lng1, lat1]]  // Outer ring
  ]
}
```

**Important:** Leaflet uses `[lat, lng]` order, but GeoJSON uses `[lng, lat]`. The application handles this conversion automatically.

## Permissions

- **Public Maps**: Visible to all users (read-only for non-owners)
- **Private Maps**: Only visible to owner
- **Features**: Only owner of parent map can create/edit/delete
- **Stories**: Only author can edit/delete
- **Photos**: Only uploader can edit/delete

## Next Steps

The following tasks remain to complete the full application:

1. **Task 6.1-6.2**: File Import UI (GeoJSON, KML, CSV)
2. **Task 7**: AWS Integration and Deployment
3. **Task 8**: External mapping services and performance optimization

## Troubleshooting

### Features not appearing on map
- Check browser console for errors
- Verify feature geometry is valid GeoJSON
- Ensure coordinates are in correct order [lng, lat]
- Check that map ID matches current map

### Authentication errors
- Verify JWT token is stored in localStorage
- Check token hasn't expired (refresh if needed)
- Ensure Authorization header format: `Bearer {token}`

### Photo upload fails
- Check file size (max 10MB)
- Verify file extension (.jpg, .jpeg, .png, .gif, .webp)
- Ensure feature exists and user owns parent map

### Geometry validation errors
- Verify GeoJSON format is correct
- Check coordinate values are within valid ranges
  - Latitude: -90 to 90
  - Longitude: -180 to 180
- Ensure polygons are closed (first point = last point)

## Summary

The feature creation and attribute reading functionality is **fully operational**. Users can:

✅ Create maps with custom center and zoom
✅ Draw points, lines, and polygons on maps
✅ Add titles, descriptions, and categories to features
✅ Attach stories with rich text content
✅ Upload photos with captions
✅ View all feature attributes in popups
✅ Edit and update feature information
✅ Delete features and their content
✅ Filter and search features by attributes

The system provides a complete, functional UI/UX for spatial data management with full backend integration.
