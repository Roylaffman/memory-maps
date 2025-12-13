# Memory Maps

A Django application for creating interactive maps with stories and photos attached to geographic locations.

## 🗺️ Features

- **Interactive Maps**: Create and manage personal memory maps with geographic features
- **Rich Content**: Attach stories and photos to map locations
- **GIS Support**: Full PostGIS integration for spatial data
- **File Import**: Import GeoJSON, KML/KMZ, and CSV coordinate files
- **Authentication**: Secure user authentication with JWT tokens
- **Sharing**: Public/private map visibility controls
- **Media Storage**: AWS S3 integration for photo storage

## 🚀 Quick Start

1. **Clone and Setup**:
   ```bash
   git clone https://github.com/Roylaffman/memory-maps.git
   cd memory-maps
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your database and settings
   ```

3. **Database Setup**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

5. **Frontend Development**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📚 Documentation

### Setup & Configuration
- [📋 Quick Start Guide](./QUICKSTART.md)
- [🗄️ PostGIS Setup](./memory_maps/SETUP.md)
- [🔧 GDAL/PostgreSQL Setup](./GDAL_POSTGRESQL_SETUP_GUIDE.md)

### User Guides
- [🎯 Feature Creation Guide](./FEATURE_CREATION_GUIDE.md)
- [📁 File Import Guide](./FILE_IMPORT_COMPLETE.md)
- [🔐 Authentication & Login](./LOGIN_CREDENTIALS.md)

### Development
- [🧪 Testing Guide](./TESTING_GUIDE.md)
- [🔗 Backend Integration](./frontend/BACKEND_INTEGRATION.md)
- [📋 Project Summary](./PROJECT_SUMMARY.md)

### Troubleshooting
- [🔍 Integration Verification](./INTEGRATION_VERIFICATION.md)
- [🚨 Issue Resolution](./ISSUE_RESOLVED.md)
- [🔐 Login Troubleshooting](./TROUBLESHOOT_LOGIN.md)

### Testing Documentation
- [🧪 Photo Upload Permission Testing](./docs/test/PHOTO_UPLOAD_PERMISSION_ISSUE.md)
- [🔑 Private Credentials](./docs/test/PRIVATE_CREDENTIALS.md)

## 🏗️ Architecture

### Backend (Django)
- **Django REST Framework**: API endpoints
- **PostGIS**: Spatial database support
- **JWT Authentication**: Secure token-based auth
- **File Upload**: Image handling with validation

### Frontend (React + Vite)
- **Leaflet Maps**: Interactive mapping
- **React Components**: Modular UI
- **API Integration**: RESTful backend communication
- **File Import**: Drag-and-drop GIS file support

## 🔧 API Endpoints

Base URL: `/api/v1/memory-maps/`

### Maps
- `GET /maps/` - List all accessible maps
- `POST /maps/` - Create new map
- `GET /maps/{id}/` - Get map details
- `PATCH /maps/{id}/` - Update map
- `DELETE /maps/{id}/` - Delete map

### Features
- `GET /features/` - List features
- `POST /features/` - Create feature
- `GET /features/{id}/` - Get feature details
- `PATCH /features/{id}/` - Update feature
- `DELETE /features/{id}/` - Delete feature

### Photos & Stories
- `POST /photos/` - Upload photo
- `POST /stories/` - Create story
- `GET /photos/` - List photos
- `GET /stories/` - List stories

### Import
- `POST /maps/{id}/import_geojson/` - Import GeoJSON
- `POST /maps/{id}/import_kml/` - Import KML/KMZ
- `POST /maps/{id}/import_coordinates/` - Import CSV coordinates

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
cd frontend && npm test
```

For detailed testing information, see [Testing Guide](./TESTING_GUIDE.md).

## 🔐 Security

- JWT token authentication
- Owner-only access to private maps
- File upload validation
- CORS configuration for frontend
- Permission checks on all operations

## 🚀 Deployment

### Production Settings
- Configure PostgreSQL with PostGIS
- Set up AWS S3 for media storage
- Configure environment variables
- Use production WSGI server

### Environment Variables
See `.env.example` for required configuration.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- [📋 Troubleshooting Guide](./TROUBLESHOOT_LOGIN.md)
- [🔍 Integration Testing](./INTEGRATION_VERIFICATION.md)
- [📧 Issues](https://github.com/Roylaffman/memory-maps/issues)
