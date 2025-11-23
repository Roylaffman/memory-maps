# Personal Memory Maps - Design Document

## Overview

Personal Memory Maps is a Django-based web application that enables users to create interactive maps with attached stories and photos. The system leverages PostGIS for spatial data management, AWS services for hosting and storage, and Leaflet for interactive mapping. The architecture prioritizes cost-effectiveness while providing rich geospatial functionality.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django API    │    │   AWS RDS       │
│   (React/Vue)   │◄──►│   Backend       │◄──►│   PostgreSQL    │
│   + Leaflet     │    │   + PostGIS     │    │   + PostGIS     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AWS S3        │    │   External APIs │    │   Tile Services │
│   Media Storage │    │   (Optional)    │    │   (OSM, etc.)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

**Backend:**
- Django 4.x with Django REST Framework
- PostGIS extension for PostgreSQL
- GeoDjango for spatial operations
- AWS RDS PostgreSQL with PostGIS

**Frontend:**
- Modern JavaScript framework (React recommended)
- Leaflet.js for interactive mapping
- Leaflet.draw for polygon/point creation
- File upload components for GIS data

**Infrastructure:**
- AWS EC2 or Elastic Beanstalk for application hosting
- AWS RDS for database (PostgreSQL with PostGIS)
- AWS S3 for media file storage
- CloudFront CDN for static assets (optional)

**External Services:**
- OpenStreetMap tiles (free)
- Alternative tile providers (Mapbox, CartoDB) as options

## Components and Interfaces

### Core Models

#### Map Model
```python
class Map(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    center_lat = models.FloatField()
    center_lng = models.FloatField()
    zoom_level = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### MapFeature Model (Points and Polygons)
```python
class MapFeature(models.Model):
    FEATURE_TYPES = [
        ('point', 'Point'),
        ('polygon', 'Polygon'),
    ]
    
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    feature_type = models.CharField(max_length=10, choices=FEATURE_TYPES)
    geometry = models.GeometryField()  # PostGIS geometry field
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### Story Model
```python
class Story(models.Model):
    feature = models.ForeignKey(MapFeature, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### Photo Model
```python
class Photo(models.Model):
    feature = models.ForeignKey(MapFeature, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=500, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

### API Endpoints

#### Map Management
- `GET /api/maps/` - List user's maps
- `POST /api/maps/` - Create new map
- `GET /api/maps/{id}/` - Get map details
- `PUT /api/maps/{id}/` - Update map
- `DELETE /api/maps/{id}/` - Delete map

#### Feature Management
- `GET /api/maps/{map_id}/features/` - Get map features
- `POST /api/maps/{map_id}/features/` - Add feature to map
- `PUT /api/features/{id}/` - Update feature
- `DELETE /api/features/{id}/` - Delete feature

#### Content Management
- `POST /api/features/{feature_id}/stories/` - Add story
- `POST /api/features/{feature_id}/photos/` - Upload photo
- `GET /api/features/{feature_id}/content/` - Get all content

#### Data Import
- `POST /api/maps/{map_id}/import/geojson/` - Import GeoJSON
- `POST /api/maps/{map_id}/import/kml/` - Import KML/KMZ

### Frontend Components

#### MapView Component
- Leaflet map integration
- Feature rendering and interaction
- Drawing tools for points/polygons
- Popup displays for feature content

#### FeatureEditor Component
- Form for adding/editing features
- Story and photo upload interface
- Category selection and metadata

#### ImportWizard Component
- File upload interface for GIS data
- Preview and validation of imported features
- Batch processing feedback

#### MapGallery Component
- Grid view of user's maps
- Public map browsing
- Search and filtering capabilities

## Data Models

### Spatial Data Handling

**Coordinate System:**
- Default: WGS84 (EPSG:4326) for web compatibility
- Support for coordinate transformation via PostGIS
- Automatic reprojection for imported data

**Geometry Storage:**
- Points stored as PostGIS POINT geometry
- Polygons stored as PostGIS POLYGON geometry
- Spatial indexing for efficient queries
- Support for complex polygons with holes

**File Format Support:**
- GeoJSON: Native Django/PostGIS support
- KML/KMZ: Parse using fastkml library
- Coordinate lists: CSV import with lat/lng columns

### Media Management

**Photo Storage:**
- AWS S3 bucket for scalable storage
- Automatic thumbnail generation
- Image optimization for web display
- CDN integration for fast delivery

**File Organization:**
```
s3://memory-maps-media/
├── photos/
│   ├── {user_id}/
│   │   ├── {map_id}/
│   │   │   ├── original/
│   │   │   └── thumbnails/
└── imports/
    └── {user_id}/
        └── temp/
```

## Error Handling

### Import Error Management
- Validation of GIS file formats before processing
- Detailed error messages for malformed data
- Partial import support with error reporting
- Rollback capability for failed imports

### Spatial Query Errors
- Graceful handling of invalid geometries
- Coordinate system transformation errors
- Database connection resilience
- Fallback to simplified queries when needed

### User Experience Errors
- Network connectivity handling
- Progressive loading for large datasets
- Offline capability for cached maps
- Clear error messages with recovery suggestions

## Testing Strategy

### Unit Testing
- Model validation and spatial operations
- API endpoint functionality
- File import processing
- Geometry calculations and transformations

### Integration Testing
- End-to-end map creation workflow
- GIS data import and validation
- Photo upload and association
- Multi-user access and permissions

### Performance Testing
- Large dataset handling (1000+ features)
- Concurrent user access
- File upload performance
- Map rendering optimization

### Spatial Testing
- Coordinate system accuracy
- Geometry validation
- Spatial query performance
- Cross-browser mapping compatibility

## Security Considerations

### Authentication & Authorization
- Django's built-in authentication system
- JWT tokens for API access
- Role-based permissions for map access
- Owner-only editing capabilities

### Data Protection
- Input validation for all GIS data
- File type verification for uploads
- SQL injection prevention via ORM
- XSS protection for user content

### Privacy Controls
- Public/private map settings
- User consent for data sharing
- GDPR compliance for EU users
- Data export capabilities

## Performance Optimization

### Database Optimization
- Spatial indexing on geometry fields
- Query optimization for large datasets
- Connection pooling for concurrent access
- Read replicas for public map viewing

### Frontend Optimization
- Lazy loading of map features
- Clustering for dense point data
- Progressive image loading
- Caching of frequently accessed maps

### AWS Cost Optimization
- RDS instance sizing based on usage
- S3 lifecycle policies for old media
- CloudFront caching for static assets
- Reserved instances for predictable workloads

## Deployment Architecture

### Development Environment
- Local PostgreSQL with PostGIS
- Django development server
- Local file storage for media
- Docker containers for consistency

### Production Environment
- AWS Elastic Beanstalk for application hosting
- AWS RDS PostgreSQL with PostGIS extension
- AWS S3 for media storage
- CloudFront CDN for global distribution
- Route 53 for DNS management

### Monitoring and Maintenance
- CloudWatch for application monitoring
- Database performance tracking
- Error logging and alerting
- Automated backups and recovery procedures