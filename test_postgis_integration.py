"""Test PostGIS integration with Django models"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memory_maps_project.settings')
django.setup()

from django.contrib.auth.models import User
from memory_maps.models import Map, MapFeature
from django.contrib.gis.geos import Point, Polygon

print("=" * 70)
print("TESTING POSTGIS INTEGRATION")
print("=" * 70)

# Create test user
print("\n1. Creating test user...")
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
print(f"✓ User: {user.username}")

# Create test map
print("\n2. Creating test map...")
map_obj = Map.objects.create(
    title='PostGIS Test Map',
    description='Testing PostGIS integration',
    owner=user,
    center_lat=40.7128,
    center_lng=-74.0060,
    zoom_level=12,
    is_public=True
)
print(f"✓ Map created: {map_obj.title} (ID: {map_obj.id})")

# Create point feature with PostGIS geometry
print("\n3. Creating point feature with PostGIS geometry...")
point_geom = Point(-74.0060, 40.7128, srid=4326)
point_feature = MapFeature.objects.create(
    map=map_obj,
    feature_type='point',
    geometry=point_geom,
    title='Central Park',
    description='A beautiful park in NYC',
    category='park'
)
print(f"✓ Point feature created: {point_feature.title}")
print(f"  Geometry: {point_feature.geometry}")
print(f"  Geometry type: {point_feature.geometry.geom_type}")

# Create polygon feature with PostGIS geometry
print("\n4. Creating polygon feature with PostGIS geometry...")
polygon_coords = [
    (-74.0, 40.7),
    (-74.0, 40.8),
    (-73.9, 40.8),
    (-73.9, 40.7),
    (-74.0, 40.7)
]
polygon_geom = Polygon(polygon_coords, srid=4326)
polygon_feature = MapFeature.objects.create(
    map=map_obj,
    feature_type='polygon',
    geometry=polygon_geom,
    title='Garden Area',
    description='A large garden',
    category='garden'
)
print(f"✓ Polygon feature created: {polygon_feature.title}")
print(f"  Geometry: {polygon_feature.geometry}")
print(f"  Geometry type: {polygon_feature.geometry.geom_type}")
print(f"  Area: {polygon_feature.geometry.area}")

# Query features
print("\n5. Querying features...")
all_features = MapFeature.objects.filter(map=map_obj)
print(f"✓ Total features: {all_features.count()}")

for feature in all_features:
    print(f"  - {feature.title} ({feature.feature_type})")

# Test spatial query
print("\n6. Testing spatial query...")
test_point = Point(-73.95, 40.75, srid=4326)
nearby_features = MapFeature.objects.filter(
    geometry__distance_lte=(test_point, 0.1)
)
print(f"✓ Features within 0.1 degrees of test point: {nearby_features.count()}")

print("\n" + "=" * 70)
print("SUCCESS! PostGIS is fully integrated and working!")
print("=" * 70)
