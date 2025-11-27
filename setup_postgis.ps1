# Setup script for Memory Maps PostgreSQL database with PostGIS
# Run this script to set up your database

Write-Host "Setting up Memory Maps PostgreSQL database..." -ForegroundColor Green

# Step 1: Create database and user
Write-Host "`nStep 1: Creating database and user..." -ForegroundColor Yellow
psql -U postgres -c "CREATE DATABASE memory_maps;"
psql -U postgres -c "CREATE USER memory_maps_user WITH PASSWORD 'memory_maps_dev_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE memory_maps TO memory_maps_user;"

# Step 2: Enable PostGIS extension
Write-Host "`nStep 2: Enabling PostGIS extension..." -ForegroundColor Yellow
psql -U postgres -d memory_maps -c "CREATE EXTENSION IF NOT EXISTS postgis;"
psql -U postgres -d memory_maps -c "CREATE EXTENSION IF NOT EXISTS postgis_topology;"

# Step 3: Grant schema permissions
Write-Host "`nStep 3: Granting permissions..." -ForegroundColor Yellow
psql -U postgres -d memory_maps -c "GRANT ALL ON SCHEMA public TO memory_maps_user;"
psql -U postgres -d memory_maps -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO memory_maps_user;"
psql -U postgres -d memory_maps -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO memory_maps_user;"
psql -U postgres -d memory_maps -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO memory_maps_user;"
psql -U postgres -d memory_maps -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO memory_maps_user;"

# Step 4: Verify PostGIS installation
Write-Host "`nStep 4: Verifying PostGIS installation..." -ForegroundColor Yellow
psql -U postgres -d memory_maps -c "SELECT PostGIS_Version();"

Write-Host "`nDatabase setup complete!" -ForegroundColor Green
Write-Host "Database: memory_maps" -ForegroundColor Cyan
Write-Host "User: memory_maps_user" -ForegroundColor Cyan
Write-Host "Password: memory_maps_dev_password" -ForegroundColor Cyan
