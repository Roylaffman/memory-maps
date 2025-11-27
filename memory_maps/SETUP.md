# Memory Maps Setup Guide

## Prerequisites

The Memory Maps app requires PostGIS for full functionality. This guide covers setup for both development and production environments.

## Development Setup

### Option 1: Without PostGIS (Limited Functionality)

For initial development and testing without spatial features:

1. Use the default SQLite database (already configured)
2. Set `USE_POSTGIS=False` in your `.env` file (or omit it)
3. Run migrations: `python manage.py migrate`

**Note:** Spatial features will not work without PostGIS.

### Option 2: With PostGIS (Full Functionality) For me Option 2 is the only option 

#### Windows Setup

1. **Install PostgreSQL with PostGIS:**
   - Download PostgreSQL from https://www.postgresql.org/download/windows/
   - During installation, include the PostGIS extension via Stack Builder
   - Or download PostGIS separately from https://postgis.net/windows_downloads/

2. **Install GDAL:**
   - Download OSGeo4W installer from https://trac.osgeo.org/osgeo4w/
   - Install GDAL and its dependencies
   - Verify installation: `gdalinfo --version`
   
   **Installing GDAL Python Bindings:**
   
   Since building GDAL from source requires Visual C++ build tools, use one of these approaches:
   
   **Option A: Use pre-built wheels (Recommended)**
   ```bash
   # For GDAL 3.12.x
   pip install GDAL==3.12.0.post1 --find-links https://github.com/cgohlke/geospatial-wheels/releases
   ```
   
   **Option B: Use OSGeo4W Python**
   - Use the Python installation that comes with OSGeo4W
   - Located at: `C:\OSGeo4W\bin\python3.exe`
   
   **Option C: Skip GDAL Python bindings for now, (no)**
   - The app will work without GDAL Python bindings for basic functionality
   - GIS file import features (Task 4) will require GDAL

3. **Configure Environment Variables:**
   
   For OSGeo4W installation, set these in your system or add to `.env`:
   ```
   GDAL_LIBRARY_PATH=C:\OSGeo4W\bin\gdal312.dll
   GEOS_LIBRARY_PATH=C:\OSGeo4W\bin\geos_c.dll
   OSGEO4W_ROOT=C:\OSGeo4W
   ```
   
   **Note:** The DLL version number (e.g., gdal312.dll) should match your installed GDAL version.
   Check with: `gdalinfo --version`
   
   **Alternative:** Add OSGeo4W to your system PATH:
   - Add `C:\OSGeo4W\bin` to your PATH environment variable
   - This allows Django to find GDAL automatically

4. **Create Database:**
   ```bash
   psql -U postgres
   CREATE DATABASE worldbuilding;
   CREATE USER worldbuilding_user WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE worldbuilding TO worldbuilding_user;
   \c worldbuilding
   CREATE EXTENSION postgis;
   ```

5. **Update .env file:**
   ```
   USE_POSTGIS=True
   POSTGRES_DB=worldbuilding
   POSTGRES_USER=worldbuilding_user
   POSTGRES_PASSWORD=password
   DB_HOST=localhost
   DB_PORT=5432
   ```

6. **Enable GIS apps in settings:**
   - Uncomment `django.contrib.gis` in `worldbuilding/settings/base.py`
   - Uncomment `rest_framework_gis` in `worldbuilding/settings/base.py`

7. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

#### macOS Setup

1. **Install PostgreSQL and PostGIS:**
   ```bash
   brew install postgresql postgis
   brew services start postgresql
   ```

2. **Install GDAL:**
   ```bash
   brew install gdal
   ```

3. **Create Database:**
   ```bash
   psql postgres
   CREATE DATABASE worldbuilding;
   CREATE USER worldbuilding_user WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE worldbuilding TO worldbuilding_user;
   \c worldbuilding
   CREATE EXTENSION postgis;
   ```

4. **Update .env file:** (same as Windows step 5)

5. **Enable GIS apps and run migrations:** (same as Windows steps 6-7)

#### Linux Setup

1. **Install PostgreSQL and PostGIS:**
   ```bash
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib postgis
   ```

2. **Install GDAL:**
   ```bash
   sudo apt-get install gdal-bin libgdal-dev
   sudo apt-get install python3-gdal
   ```

3. **Create Database:** (same as macOS step 3)

4. **Update .env file:** (same as Windows step 5)

5. **Enable GIS apps and run migrations:** (same as Windows steps 6-7)

## Production Setup (AWS)

### AWS RDS PostgreSQL with PostGIS

1. **Create RDS Instance:**
   - Go to AWS RDS Console
   - Create new PostgreSQL database
   - Choose version 13+ (PostGIS support)
   - Select appropriate instance size (db.t3.micro for testing)
   - Enable public accessibility if needed
   - Configure security groups

2. **Enable PostGIS Extension:**
   ```bash
   psql -h your-rds-endpoint.rds.amazonaws.com -U admin -d worldbuilding
   CREATE EXTENSION postgis;
   CREATE EXTENSION postgis_topology;
   ```

3. **Configure Environment Variables:**
   ```
   DJANGO_ENV=production
   USE_POSTGIS=True
   RDS_DB_NAME=worldbuilding
   RDS_USERNAME=admin
   RDS_PASSWORD=your-secure-password
   RDS_HOSTNAME=your-rds-endpoint.rds.amazonaws.com
   RDS_PORT=5432
   ```

4. **AWS S3 for Media Storage:**
   - Create S3 bucket: `memory-maps-media`
   - Configure IAM user with S3 access
   - Set environment variables:
     ```
     AWS_ACCESS_KEY_ID=your-key
     AWS_SECRET_ACCESS_KEY=your-secret
     AWS_STORAGE_BUCKET_NAME=memory-maps-media
     AWS_S3_REGION_NAME=us-east-1
     ```

5. **Deploy Application:**
   - Use Elastic Beanstalk or EC2
   - Ensure GDAL is installed on the server
   - Run migrations: `python manage.py migrate`

## Verification

Test your setup:

```bash
python manage.py check
python manage.py shell
```

In the shell:
```python
from django.contrib.gis.geos import Point
p = Point(0, 0)
print(p)  # Should print: POINT (0 0)
```

## Troubleshooting

### GDAL Not Found
- Ensure GDAL is installed and in your PATH
- Set `GDAL_LIBRARY_PATH` environment variable
- On Windows, use OSGeo4W installer

### PostGIS Extension Not Found
- Ensure PostGIS is installed with PostgreSQL
- Run `CREATE EXTENSION postgis;` in your database
- Check PostgreSQL version compatibility

### Connection Refused
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Verify firewall/security group settings

## Next Steps

Once setup is complete, proceed to implement the data models in task 2.
