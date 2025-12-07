# 🔒 Photo Upload Permission Issue - RESOLVED!

## 🎯 The Problem
Error: "Failed to save feature request failed" when trying to upload photos.

## 🔍 Root Cause
You are logged in as **`roylaffman`** (user ID 4), but the map "PuntaMona" belongs to **`rlafferty`** (user ID 5).

The backend correctly enforces permissions - users can only upload photos to features on maps they own.

## ✅ The Fix Applied
1. **Fixed API Content-Type handling** - The request function now properly handles FormData uploads by not setting `Content-Type: application/json` for FormData requests
2. **Permissions are working correctly** - The backend is properly checking ownership before allowing photo uploads

## 🚀 How to Upload Photos Successfully

### Option 1: Create Your Own Map (Recommended)
1. Go back to the gallery (click "← Back to Gallery")
2. Click "+ Create New Map"
3. Fill in the map details
4. Click "Create Map"
5. Add features (points, lines, polygons) to YOUR map
6. Upload photos to those features ✅

### Option 2: Log In as the Map Owner
1. Log out (click "Logout" in the top right)
2. Log in as `rlafferty` (the owner of PuntaMona map)
3. Now you can upload photos to features on that map ✅

### Option 3: Request Collaborative Access (Future Feature)
Currently, only map owners can add content. A future feature could allow map owners to grant edit permissions to other users.

## 📊 Current Database State

**Users:**
- `roylaffman` (ID: 4) - No maps owned
- `rlafferty` (ID: 5) - Owns "PuntaMona" map (ID: 12)

**Maps:**
- Map ID 12: "PuntaMona" - Owner: `rlafferty`
  - Feature ID 85: "Front House" (point)

## ✅ What's Working Now
- ✅ Login/authentication
- ✅ Map viewing (public and owned maps)
- ✅ Feature creation
- ✅ Permission checks (preventing unauthorized uploads)
- ✅ Photo upload API (when user owns the map)
- ✅ FormData handling in API requests

## 🔧 Technical Details

### Permission Check (in `memory_maps/views.py`)
```python
def perform_create(self, serializer):
    """Set the uploader and validate permissions when uploading a photo."""
    feature = serializer.validated_data['feature']
    if feature.map.owner != self.request.user:
        raise PermissionDenied("You can only add photos to features on your own maps.")
    serializer.save(uploaded_by=self.request.user)
```

This is **correct behavior** - it prevents users from uploading content to maps they don't own.

### API Fix (in `frontend/src/services/api.js`)
```javascript
// Before: Always set Content-Type
headers: {
  'Content-Type': 'application/json',
  ...options.headers,
}

// After: Only set Content-Type for non-FormData
headers: {
  ...options.headers,
}
// Add Content-Type for JSON requests (but not for FormData)
if (!(options.body instanceof FormData)) {
  config.headers['Content-Type'] = 'application/json';
}
```

## 🎯 Next Steps
1. Create a new map as `roylaffman`
2. Add features to your new map
3. Upload photos to those features
4. Everything should work perfectly! ✅

---
**Date:** December 7, 2025  
**Issue:** Permission denied when uploading photos to another user's map  
**Status:** Working as designed - permissions are correctly enforced  
**Solution:** Create your own map or log in as the map owner
