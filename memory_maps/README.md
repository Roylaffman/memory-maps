# Memory Maps Django App

This Django app provides functionality for creating interactive maps with stories and photos attached to geographic locations.

## Features

- Create and manage personal memory maps
- Add points and polygons to maps using PostGIS
- Attach stories and photos to map features
- Import GIS data (GeoJSON, KML/KMZ)
- Public/private map sharing
- AWS S3 integration for media storage

## Requirements

- Django 4.2+
- PostgreSQL with PostGIS extension
- GDAL/GEOS libraries
- AWS S3 (for production media storage)

## Setup

1. Ensure PostgreSQL with PostGIS is installed and configured
2. Install required Python packages: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`

## Configuration

See `.env.example` for required environment variables.

### Development
- Set `DJANGO_ENV=development`
- Use local PostgreSQL with PostGIS

### Production
- Set `DJANGO_ENV=production`
- Configure AWS RDS PostgreSQL with PostGIS
- Configure AWS S3 for media storage

## API Endpoints

API endpoints will be available at `/api/v1/memory-maps/` once models and views are implemented.

## Models

- **Map**: Container for geographic features with metadata
- **MapFeature**: Points or polygons with associated content
- **Story**: Text narratives attached to features
- **Photo**: Images attached to features

## Development Status

This app is currently in initial setup phase. Core models and API endpoints will be implemented in subsequent tasks.
