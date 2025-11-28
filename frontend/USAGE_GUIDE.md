# Personal Memory Maps - Usage Guide

## Getting Started

1. **Start the development server:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Open your browser:**
   Navigate to `http://localhost:5174`

## Using the Map

### Drawing Features

#### Create a Point (Marker)
1. Click the **marker icon** (📍) in the top-right toolbar
2. Click anywhere on the map to place the marker
3. A popup will appear showing the new feature
4. The feature count in the header will update

#### Create a Polygon
1. Click the **polygon icon** (▭) in the top-right toolbar
2. Click multiple points on the map to define the polygon
3. Double-click to finish the polygon
4. The area will be calculated and displayed
5. Feature appears with a blue fill and border

#### Create a Rectangle
1. Click the **rectangle icon** (▢) in the top-right toolbar
2. Click and drag to create the rectangle
3. Release to finish

### Editing Features

1. Click the **edit icon** (✏️) in the toolbar
2. Click "Edit layers" button
3. Drag vertices to modify shapes
4. Drag markers to move them
5. Click "Save" to confirm changes

### Deleting Features

#### Method 1: Via Drawing Controls
1. Click the **trash icon** (🗑️) in the toolbar
2. Click "Remove layers" button
3. Click on features to select them
4. Click "Delete" to confirm

#### Method 2: Via Popup
1. Click on any feature to open its popup
2. Click the red "Delete" button
3. Confirm the deletion

### Viewing Feature Information

1. Click on any marker or polygon
2. A popup appears showing:
   - Feature title
   - Description
   - Category badge
   - Photos (if any)
   - Stories (if any)
   - Edit and Delete buttons

## Map Navigation

### Zoom
- **Scroll wheel**: Zoom in/out
- **Zoom buttons**: Bottom-right corner (+/-)
- **Double-click**: Zoom in
- **Shift + drag**: Zoom to area

### Pan
- **Click and drag**: Move the map
- **Arrow keys**: Pan in directions (if focused)

### Zoom Levels
- **Minimum**: 3 (world view)
- **Maximum**: 18 (street level)
- **Default**: 10 (city view)

## Feature Counter

The header displays the current number of features on the map:
- Updates automatically when features are added/removed
- Shows "0 features" when map is empty

## Keyboard Shortcuts

- **Escape**: Cancel current drawing operation
- **Delete**: Remove selected features (in edit mode)
- **Ctrl/Cmd + Z**: Undo last point (while drawing)

## Tips & Tricks

### Drawing Polygons
- Click carefully to place each vertex
- Double-click to finish (don't click the first point again)
- The polygon will show its area in square meters
- Polygons cannot self-intersect (will show error)

### Organizing Features
- Use categories to group related features
- Add descriptive titles for easy identification
- Use the popup to quickly view feature details

### Performance
- The map handles hundreds of features efficiently
- Large polygons may take a moment to render
- Zoom in for better precision when drawing

## Troubleshooting

### Marker icons not showing
- Check your internet connection (icons load from CDN)
- Refresh the page

### Can't draw
- Make sure no other drawing tool is active
- Click "Cancel" if a drawing is in progress
- Refresh the page if controls are unresponsive

### Popup not appearing
- Make sure you're clicking directly on the feature
- Try zooming in for better precision
- Check browser console for errors

## Editing Feature Content (NEW!)

### Opening the Editor
- **Automatic**: Editor opens automatically when you create a new feature
- **Manual**: Click any feature, then click the "Edit" button in the popup

### Adding Details
1. **Title**: Enter a descriptive name (required)
2. **Description**: Add detailed information about the feature
3. **Category**: Classify the feature (e.g., Garden, Building, Trail)

### Uploading Photos
1. Click the "📷 Add Photos" button
2. Select one or more images from your device
3. Photos appear instantly with preview thumbnails
4. Add captions by typing in the field below each photo
5. Remove photos by clicking the × button

### Adding Stories
1. Click the "+ Add Story" button
2. Enter a story title
3. Write your story content
4. Click "Save Story" to add it
5. Add multiple stories to tell the complete narrative
6. Remove stories by clicking the × button on each card

### Saving Changes
- Click "Save Changes" to update the feature
- Click "Cancel" or the × button to discard changes
- Click outside the modal to close without saving

## What's Next

Coming in Task 5.4:
- 🗺️ Map gallery and management
- 🔍 Search and filter features
- 🔗 Share maps with others
- 👁️ Public/private visibility controls
