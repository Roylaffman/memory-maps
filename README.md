# Memory Maps

A Django application for creating interactive maps with stories and photos attached to geographic locations.

## Features

- Create and manage personal memory maps
- Add points and polygons to maps using PostGIS
- Attach stories and photos to map features
- Import GIS data (GeoJSON, KML/KMZ)
- Public/private map sharing
- AWS S3 integration for media storage

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run development server:
   ```bash
   python manage.py runserver
   ```

## PostGIS Setup

See `memory_maps/SETUP.md` for detailed PostGIS installation instructions.

## API Documentation

API endpoints are available at `/api/v1/memory-maps/`

## Development

See `.kiro/specs/personal-memory-maps/` for requirements, design, and implementation tasks.

## License

MIT License
