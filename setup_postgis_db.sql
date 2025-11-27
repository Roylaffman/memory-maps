-- Setup script for Memory Maps PostgreSQL database with PostGIS

-- Create database
CREATE DATABASE memory_maps;

-- Create user
CREATE USER memory_maps_user WITH PASSWORD 'memory_maps_dev_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE memory_maps TO memory_maps_user;

-- Connect to the new database (you'll need to run this separately)
-- \c memory_maps

-- Enable PostGIS extension (run after connecting to memory_maps database)
-- CREATE EXTENSION IF NOT EXISTS postgis;
-- CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Grant schema permissions
-- GRANT ALL ON SCHEMA public TO memory_maps_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO memory_maps_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO memory_maps_user;
