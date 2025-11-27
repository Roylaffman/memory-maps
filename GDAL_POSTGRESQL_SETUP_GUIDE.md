# Complete GDAL and PostgreSQL Setup Guide for Windows

This guide documents the complete process of setting up GDAL Python bindings and PostgreSQL with PostGIS for Django GIS applications on Windows.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [GDAL Installation](#gdal-installation)
3. [PostgreSQL Installation](#postgresql-installation)
4. [Python Environment Setup](#python-environment-setup)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Scripts Reference](#scripts-reference)

---

## Prerequisites

### System Requirements
- Windows 10/11
- Python 3.11+ installed
- Administrator access for installations
- Internet connection for downloading packages

### Check Existing Installations

```powershell
# Check if GDAL is installed
gdalinfo --version

# Check if PostgreSQL is installed
psql --version

# Check Python version
python --version
```

---

## GDAL Installation

### Step 1: Install OSGeo4W (GDAL Command-Line Tools)

OSGeo4W provides GDAL command-line utilities that are useful for GIS operations.

1. **Download OSGeo4W Installer**
   - Visit: https://trac.osgeo.org/osgeo4w/
   - Download the installer (OSGeo4W-v2-setup.exe)

2. **Run Installer**
   - Choose "Express Install"
   - Select "GDAL" from the package list
   - Complete the installation (default location: `C:\OSGeo4W`)

3. **Verify Installation**
   ```powershell
   # Check GDAL version
   gdalinfo --version
   # Output: GDAL 3.12.0 "Chicoutimi", released 2025/11/03
   
   # Find GDAL location
   where.exe gdalinfo
   # Output: C:\OSGeo4W\bin\gdalinfo.exe
   ```

4. **Locate GDAL DLLs**
   ```powershell
   # List GDAL DLLs
   dir C:\OSGeo4W\bin\gdal*.dll
   # You should see files like: gdal311.dll, gdal312.dll
   ```

### Step 2: Install GDAL Python Bindings

The GDAL Python bindings allow Python code to use GDAL functionality.

#### Why Pre-built Wheels?

Building GDAL from source requires:
- Microsoft Visual C++ 14.0 or greater
- Complex build configuration
- Matching library versions

**Solution**: Use pre-built wheels that include all necessary DLLs.

#### Installation Steps

1. **Install pipwin (Optional - for package discovery)**
   ```powershell
   pip install pipwin
   ```
   
   Note: pipwin may have issues with newer package repositories. If it fails, proceed to step 2.

2. **Install GDAL from Pre-built Wheel**
   
   Find the appropriate wheel for your Python version from:
   - https://github.com/cgohlke/geospatial-wheels/releases
   
   For Python 3.11 on Windows (64-bit):
   ```powershell
   pip install https://github.com/cgohlke/geospatial-wheels/releases/download/v2024.2.18/GDAL-3.8.4-cp311-cp311-win_amd64.whl
   ```
   
   **Wheel Naming Convention**:
   - `GDAL-3.8.4` - GDAL version
   - `cp311` - Python 3.11
   - `win_amd64` - Windows 64-bit
   
   For other Python versions, replace `cp311` with:
   - Python 3.10: `cp310`
   - Python 3.12: `cp312`

3. **Verify Python Bindings**
   ```powershell
   python -c "from osgeo import gdal; print(f'GDAL Python version: {gdal.__version__}')"
   # Output: GDAL Python version: 3.8.4
   ```

4. **Check Included DLLs**
   ```powershell
   python -c "import os; from osgeo import gdal; import osgeo; print(os.path.dirname(osgeo.__file__))"
   # Output: C:\Users\...\venv\Lib\site-packages\osgeo
   
   # List DLLs in the osgeo package
   dir "C:\Users\...\venv\Lib\site-packages\osgeo\*.dll"
   # You should see: gdal.dll, geos.dll, geos_c.dll, proj_9_3.dll
   ```

**Important**: The pre-built wheel includes its own GDAL, GEOS, and PROJ libraries. These are self-contained and don't require OSGeo4W for Python operations.

---

## PostgreSQL Installation

### Step 1: Install PostgreSQL

1. **Download PostgreSQL**
   - Visit: https://www.postgresql.org/download/windows/
   - Download the installer (version 17.5 or later recommended)

2. **Run Installer**
   - Follow the installation wizard
   - Remember the password you set for the `postgres` user
   - Default port: 5432
   - Install Stack Builder when prompted (for PostGIS)

3. **Verify Installation**
   ```powershell
   psql --version
   # Output: psql (PostgreSQL) 17.5
   ```

### Step 2: Install PostGIS Extension

PostGIS adds spatial database capabilities to PostgreSQL.

1. **Using Stack Builder** (Recommended)
   - Launch Stack Builder from Start Menu
   - Select your PostgreSQL installation
   - Navigate to "Spatial Extensions"
   - Select "PostGIS" and install

2. **Manual Installation**
   - Download from: https://postgis.net/windows_downloads/
   - Run the installer
   - Select your PostgreSQL installation directory

3. **Verify PostGIS**
   ```powershell
   # Connect to PostgreSQL
   psql -U postgres
   
   # Check PostGIS availability
   SELECT name, default_version FROM pg_available_extensions WHERE name LIKE 'postgis%';
   ```

### Step 3: Create Database with PostGIS

```powershell
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE memory_maps;

# Create user
CREATE USER memory_maps_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE memory_maps TO memory_maps_user;

# Connect to the new database
\c memory_maps

# Enable PostGIS extension
CREATE EXTENSION postgis;

# Verify PostGIS installation
SELECT PostGIS_Version();

# Exit
\q
```

---

## Python Environment Setup

### Step 1: Configure Django Settings

Add GDAL configuration to your Django settings file (`settings/base.py`):

```python
# GDAL Configuration
import os
import sys

# Use GDAL from the Python wheel (osgeo package)
# The wheel includes its own GDAL, GEOS, and PROJ libraries
try:
    import osgeo
    osgeo_path = os.path.dirname(osgeo.__file__)
    
    # Set GDAL library path to the wheel's DLL
    gdal_dll = os.path.join(osgeo_path, 'gdal.dll')
    if os.path.exists(gdal_dll):
        GDAL_LIBRARY_PATH = gdal_dll
        os.environ['GDAL_LIBRARY_PATH'] = gdal_dll
    
    # Set GEOS library path to the wheel's DLL
    geos_dll = os.path.join(osgeo_path, 'geos_c.dll')
    if os.path.exists(geos_dll):
        GEOS_LIBRARY_PATH = geos_dll
        os.environ['GEOS_LIBRARY_PATH'] = geos_dll
    
    # Add osgeo directory to PATH so DLLs can find their dependencies
    if sys.platform == 'win32':
        os.environ['PATH'] = osgeo_path + ';' + os.environ.get('PATH', '')
        
except ImportError:
    # GDAL Python bindings not installed
    # Fall back to OSGeo4W if available
    if sys.platform == 'win32':
        osgeo4w_path = config('OSGEO4W_ROOT', default=r'C:\OSGeo4W')
        if os.path.exists(osgeo4w_path):
            os.environ['PATH'] = os.path.join(osgeo4w_path, 'bin') + ';' + os.environ.get('PATH', '')
```

**How This Works**:
1. Tries to import `osgeo` package
2. Finds the location of the osgeo package
3. Sets `GDAL_LIBRARY_PATH` to point to the wheel's `gdal.dll`
4. Sets `GEOS_LIBRARY_PATH` to point to the wheel's `geos_c.dll`
5. Adds the osgeo directory to PATH so DLLs can find dependencies
6. Falls back to OSGeo4W if Python bindings aren't installed

### Step 2: Configure Database Connection

Create or update your `.env` file:

```env
# Database Configuration
POSTGRES_DB=memory_maps
POSTGRES_USER=memory_maps_user
POSTGRES_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Optional: OSGeo4W path (if using command-line tools)
OSGEO4W_ROOT=C:\OSGeo4W
```

Update `settings/base.py` or `settings/development.py`:

```python
# For development with SQLite (no PostGIS)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For production with PostgreSQL + PostGIS (uncomment when ready)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': config('POSTGRES_DB'),
#         'USER': config('POSTGRES_USER'),
#         'PASSWORD': config('POSTGRES_PASSWORD'),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }
```

### Step 3: Enable Django GIS (When Ready)

In `settings/base.py`, uncomment GIS apps:

```python
INSTALLED_APPS = [
    # ...
    'django.contrib.gis',  # GeoDjango for spatial data
    # ...
    'rest_framework_gis',  # DRF GIS support
    # ...
]
```

---

## Verification

### Test Script 1: Basic GDAL Test

Create `test_gdal_basic.py`:

```python
"""Test GDAL Python bindings"""
from osgeo import gdal, ogr, osr

print("=" * 60)
print("Testing GDAL Python Bindings")
print("=" * 60)

# Test GDAL
print(f"✓ GDAL version: {gdal.__version__}")
print(f"✓ GDAL VersionInfo: {gdal.VersionInfo()}")

# Test OGR (vector data)
print(f"✓ OGR drivers available: {ogr.GetDriverCount()}")

# Test OSR (spatial reference)
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)  # WGS84
print(f"✓ OSR working: Created WGS84 spatial reference")

print("\nSUCCESS! GDAL is working correctly.")
```

Run it:
```powershell
python test_gdal_basic.py
```

### Test Script 2: Django GIS Test

Create `test_django_gis.py`:

```python
"""Test Django GIS integration"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

print("=" * 60)
print("Testing Django GIS")
print("=" * 60)

try:
    from django.contrib.gis.geos import Point, Polygon
    
    # Test Point creation
    p = Point(0, 0)
    print(f"✓ Created GEOS Point: {p}")
    
    # Test Polygon creation
    poly = Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)))
    print(f"✓ Created GEOS Polygon: {poly}")
    
    print("\nSUCCESS! Django GIS is working correctly.")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
```

Run it:
```powershell
python test_django_gis.py
```

### Test Script 3: PostgreSQL Connection

```powershell
# Test PostgreSQL connection
psql -U memory_maps_user -d memory_maps -c "SELECT version();"

# Test PostGIS
psql -U memory_maps_user -d memory_maps -c "SELECT PostGIS_Version();"
```

### Run Django Tests

```powershell
# Run all tests
python manage.py test

# Run specific test class
python manage.py test memory_maps.tests.MapAPITest
```

---

## Troubleshooting

### Issue 1: "Could not find the GDAL library"

**Symptoms**:
```
django.core.exceptions.ImproperlyConfigured: Could not find the GDAL library
```

**Solutions**:

1. **Check if GDAL Python bindings are installed**:
   ```powershell
   pip list | Select-String -Pattern "GDAL"
   ```
   
   If not installed, install the wheel:
   ```powershell
   pip install https://github.com/cgohlke/geospatial-wheels/releases/download/v2024.2.18/GDAL-3.8.4-cp311-cp311-win_amd64.whl
   ```

2. **Verify GDAL_LIBRARY_PATH is set correctly**:
   ```python
   import os
   print(os.environ.get('GDAL_LIBRARY_PATH'))
   ```

3. **Check if the DLL exists**:
   ```powershell
   python -c "import os; import osgeo; print(os.path.join(os.path.dirname(osgeo.__file__), 'gdal.dll'))"
   ```

### Issue 2: "The specified procedure could not be found" (WinError 127)

**Symptoms**:
```
OSError: [WinError 127] The specified procedure could not be found
```

**Cause**: GDAL DLL is found but missing dependencies.

**Solutions**:

1. **Ensure osgeo directory is in PATH** (should be automatic with our settings):
   ```python
   import os
   import osgeo
   osgeo_path = os.path.dirname(osgeo.__file__)
   os.environ['PATH'] = osgeo_path + ';' + os.environ.get('PATH', '')
   ```

2. **Use the wheel's bundled DLLs** (not OSGeo4W's):
   - The wheel includes all necessary DLLs
   - Don't mix OSGeo4W DLLs with wheel DLLs

### Issue 3: Version Mismatch

**Symptoms**:
```
GDAL version mismatch: Python bindings 3.8.4 vs system GDAL 3.12.0
```

**Solution**: This is normal and expected. The Python bindings (3.8.4) include their own GDAL library and don't need to match the system GDAL version (3.12.0). They work independently.

### Issue 4: PostgreSQL Connection Refused

**Symptoms**:
```
psql: error: connection to server at "localhost" (::1), port 5432 failed
```

**Solutions**:

1. **Check if PostgreSQL is running**:
   ```powershell
   # Check service status
   Get-Service -Name postgresql*
   
   # Start service if stopped
   Start-Service -Name "postgresql-x64-17"
   ```

2. **Verify connection parameters**:
   ```powershell
   psql -U postgres -h localhost -p 5432
   ```

3. **Check pg_hba.conf** (if authentication fails):
   - Location: `C:\Program Files\PostgreSQL\17\data\pg_hba.conf`
   - Ensure local connections are allowed

### Issue 5: PostGIS Extension Not Found

**Symptoms**:
```
ERROR: could not open extension control file "postgis.control"
```

**Solutions**:

1. **Reinstall PostGIS** using Stack Builder

2. **Verify PostGIS files exist**:
   ```
   C:\Program Files\PostgreSQL\17\share\extension\postgis.control
   ```

3. **Check available extensions**:
   ```sql
   SELECT * FROM pg_available_extensions WHERE name LIKE 'postgis%';
   ```

---

## Scripts Reference

### Quick Diagnostic Script

Save as `diagnose_gis_setup.py`:

```python
"""Comprehensive GIS setup diagnostic script"""
import os
import sys

print("=" * 70)
print("GIS SETUP DIAGNOSTIC REPORT")
print("=" * 70)

# 1. Python Version
print(f"\n1. Python Version: {sys.version}")

# 2. Check GDAL Python Bindings
print("\n2. GDAL Python Bindings:")
try:
    from osgeo import gdal, ogr, osr
    print(f"   ✓ GDAL installed: {gdal.__version__}")
    print(f"   ✓ OGR drivers: {ogr.GetDriverCount()}")
    
    import osgeo
    osgeo_path = os.path.dirname(osgeo.__file__)
    print(f"   ✓ Location: {osgeo_path}")
    
    # Check for DLLs
    gdal_dll = os.path.join(osgeo_path, 'gdal.dll')
    geos_dll = os.path.join(osgeo_path, 'geos_c.dll')
    print(f"   ✓ GDAL DLL exists: {os.path.exists(gdal_dll)}")
    print(f"   ✓ GEOS DLL exists: {os.path.exists(geos_dll)}")
    
except ImportError as e:
    print(f"   ✗ GDAL not installed: {e}")

# 3. Check OSGeo4W
print("\n3. OSGeo4W Installation:")
osgeo4w_path = r'C:\OSGeo4W'
if os.path.exists(osgeo4w_path):
    print(f"   ✓ OSGeo4W found at: {osgeo4w_path}")
    gdal_bin = os.path.join(osgeo4w_path, 'bin', 'gdalinfo.exe')
    print(f"   ✓ gdalinfo.exe exists: {os.path.exists(gdal_bin)}")
else:
    print(f"   ✗ OSGeo4W not found at: {osgeo4w_path}")

# 4. Check Django
print("\n4. Django:")
try:
    import django
    print(f"   ✓ Django installed: {django.get_version()}")
except ImportError:
    print("   ✗ Django not installed")

# 5. Check Django GIS
print("\n5. Django GIS:")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memory_maps_project.settings')
    import django
    django.setup()
    
    from django.contrib.gis.geos import Point
    p = Point(0, 0)
    print(f"   ✓ Django GIS working: {p}")
except Exception as e:
    print(f"   ✗ Django GIS error: {e}")

# 6. Environment Variables
print("\n6. Environment Variables:")
print(f"   GDAL_LIBRARY_PATH: {os.environ.get('GDAL_LIBRARY_PATH', 'Not set')}")
print(f"   GEOS_LIBRARY_PATH: {os.environ.get('GEOS_LIBRARY_PATH', 'Not set')}")

# 7. PostgreSQL
print("\n7. PostgreSQL:")
try:
    import subprocess
    result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"   ✓ PostgreSQL: {result.stdout.strip()}")
    else:
        print("   ✗ PostgreSQL not found in PATH")
except FileNotFoundError:
    print("   ✗ PostgreSQL not found")

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
```

Run it:
```powershell
python diagnose_gis_setup.py
```

---

## Summary

### What We Installed

1. **OSGeo4W** (C:\OSGeo4W)
   - Provides GDAL command-line tools
   - Version: 3.12.0
   - Used for: GIS file operations, data conversion

2. **GDAL Python Bindings** (via wheel)
   - Version: 3.8.4
   - Includes: gdal.dll, geos.dll, geos_c.dll, proj_9_3.dll
   - Used for: Python GIS operations in Django

3. **PostgreSQL** 
   - Version: 17.5
   - Used for: Database storage

4. **PostGIS**
   - Extension for PostgreSQL
   - Used for: Spatial database operations

### Key Concepts

- **OSGeo4W vs Python Wheel**: OSGeo4W provides command-line tools, while the Python wheel provides libraries for Python code. They can coexist and serve different purposes.

- **DLL Locations**: The Python wheel includes its own DLLs in the `site-packages/osgeo` directory. These are separate from OSGeo4W's DLLs.

- **Django Configuration**: Django needs to know where to find the GDAL and GEOS DLLs. Our settings file automatically detects and configures these paths.

### Next Steps

1. Enable Django GIS apps in settings when ready for full PostGIS integration
2. Switch from SQLite to PostgreSQL database
3. Run migrations to create spatial database tables
4. Implement GIS data import features (Task 4)

---

## Additional Resources

- **GDAL Documentation**: https://gdal.org/
- **Django GIS Documentation**: https://docs.djangoproject.com/en/stable/ref/contrib/gis/
- **PostGIS Documentation**: https://postgis.net/documentation/
- **Christoph Gohlke's Wheels**: https://github.com/cgohlke/geospatial-wheels
- **OSGeo4W**: https://trac.osgeo.org/osgeo4w/

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-27  
**Tested On**: Windows 11, Python 3.11, Django 4.2
