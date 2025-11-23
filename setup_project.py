"""
Setup script for the new memory_maps standalone project.
This will be copied to the new project directory and run there.
"""

from pathlib import Path
import re

PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = "memory_maps_project"

print("🔧 Setting up Memory Maps Django project...\n")

# Create __init__.py files
print("📝 Creating __init__.py files...")
(PROJECT_DIR / PROJECT_NAME / "settings" / "__init__.py").write_text("""\"\"\"
Settings package for memory_maps_project.
Automatically loads the appropriate settings module based on DJANGO_ENV.
\"\"\"

import os
from decouple import config

# Determine which settings to use
env = config('DJANGO_ENV', default='development')

if env == 'production':
    from .production import *
elif env == 'development':
    from .development import *
else:
    from .base import *
""")

(PROJECT_DIR / PROJECT_NAME / "__init__.py").write_text("")

print("   ✓ __init__.py files created")

# Update settings files to remove collab references
print("📝 Updating settings files...")

# Update base.py
base_settings = PROJECT_DIR / PROJECT_NAME / "settings" / "base.py"
if base_settings.exists():
    content = base_settings.read_text()
    
    # Remove collab from INSTALLED_APPS
    content = re.sub(r"    'collab',\n", "", content)
    
    # Update ROOT_URLCONF
    content = content.replace(
        "ROOT_URLCONF = 'worldbuilding.urls'",
        f"ROOT_URLCONF = '{PROJECT_NAME}.urls'"
    )
    
    # Update WSGI_APPLICATION
    content = content.replace(
        "WSGI_APPLICATION = 'worldbuilding.wsgi.application'",
        f"WSGI_APPLICATION = '{PROJECT_NAME}.wsgi.application'"
    )
    
    base_settings.write_text(content)
    print("   ✓ base.py updated")

# Create urls.py
print("📝 Creating urls.py...")
(PROJECT_DIR / PROJECT_NAME / "urls.py").write_text("""\"\"\"
URL configuration for memory_maps_project.
\"\"\"

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    \"\"\"API root endpoint.\"\"\"
    return Response({
        'message': 'Memory Maps API',
        'version': 'v1',
        'endpoints': {
            'admin': request.build_absolute_uri('/admin/'),
            'memory_maps': request.build_absolute_uri('/api/v1/memory-maps/'),
        }
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    path('api/v1/memory-maps/', include('memory_maps.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
""")
print("   ✓ urls.py created")

# Create wsgi.py
print("📝 Creating wsgi.py...")
(PROJECT_DIR / PROJECT_NAME / "wsgi.py").write_text(f"""\"\"\"
WSGI config for {PROJECT_NAME}.
\"\"\"

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{PROJECT_NAME}.settings')

application = get_wsgi_application()
""")
print("   ✓ wsgi.py created")

# Create asgi.py
print("📝 Creating asgi.py...")
(PROJECT_DIR / PROJECT_NAME / "asgi.py").write_text(f"""\"\"\"
ASGI config for {PROJECT_NAME}.
\"\"\"

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{PROJECT_NAME}.settings')

application = get_asgi_application()
""")
print("   ✓ asgi.py created")

# Create manage.py
print("📝 Creating manage.py...")
(PROJECT_DIR / "manage.py").write_text(f"""#!/usr/bin/env python
\"\"\"Django's command-line utility for administrative tasks.\"\"\"
import os
import sys


def main():
    \"\"\"Run administrative tasks.\"\"\"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{PROJECT_NAME}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
""")
print("   ✓ manage.py created")

# Create .gitignore
print("📝 Creating .gitignore...")
(PROJECT_DIR / ".gitignore").write_text("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
*.egg-info/
dist/
build/

# Django
*.log
db.sqlite3
db.sqlite3-journal
/media
/staticfiles
/static

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/
""")
print("   ✓ .gitignore created")

# Create README.md
print("📝 Creating README.md...")
(PROJECT_DIR / "README.md").write_text("""# Memory Maps

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
   venv\\Scripts\\activate  # Windows
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
""")
print("   ✓ README.md created")

print("\n✅ Setup complete!")
print("\n📝 Next steps:")
print("1. Create .env file: cp .env.example .env")
print("2. Edit .env with your database settings")
print("3. Run migrations: python manage.py migrate")
print("4. Create superuser: python manage.py createsuperuser")
print("5. Run server: python manage.py runserver")
print("6. Initialize git: git init && git add . && git commit -m 'Initial commit'")
