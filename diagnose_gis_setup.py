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
