"""
Test file import functionality (GeoJSON, KML, CSV).
Tests the complete import workflow via the backend API.
"""

import requests
import json
import os

# Configuration
BASE_URL = "http://localhost:8000/api/v1/memory-maps"
AUTH_URL = "http://localhost:8000/api/auth"
USERNAME = "testuser"
PASSWORD = "testpass123"

def test_file_import():
    """Test the complete file import workflow."""
    
    print("=" * 60)
    print("FILE IMPORT FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1. Authenticating...")
    try:
        response = requests.post(
            f"{AUTH_URL}/login/",
            json={"username": USERNAME, "password": PASSWORD}
        )
        if response.status_code == 200:
            token = response.json().get('access')
            print(f"   ✓ Logged in successfully")
        else:
            print(f"   ✗ Login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Create a test map
    print("\n2. Creating a test map...")
    map_data = {
        "title": "Import Test Map",
        "description": "Testing file import functionality",
        "center_lat": 37.7749,
        "center_lng": -122.4194,
        "zoom_level": 12,
        "is_public": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/maps/",
            json=map_data,
            headers=headers
        )
        if response.status_code == 201:
            map_obj = response.json()
            map_id = map_obj['id']
            print(f"   ✓ Map created with ID: {map_id}")
        else:
            print(f"   ✗ Map creation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 3: Test GeoJSON import
    print("\n3. Testing GeoJSON import...")
    geojson_path = "test_data/sample.geojson"
    
    if not os.path.exists(geojson_path):
        print(f"   ⚠ Test file not found: {geojson_path}")
    else:
        try:
            with open(geojson_path, 'rb') as f:
                files = {'file': ('sample.geojson', f, 'application/json')}
                response = requests.post(
                    f"{BASE_URL}/maps/{map_id}/import_geojson/",
                    files=files,
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code == 201:
                    result = response.json()
                    print(f"   ✓ GeoJSON imported successfully")
                    print(f"   Imported: {result.get('imported', 0)} features")
                    if result.get('warnings'):
                        print(f"   Warnings: {len(result['warnings'])}")
                else:
                    print(f"   ✗ GeoJSON import failed: {response.status_code}")
                    print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    # Step 4: Test KML import
    print("\n4. Testing KML import...")
    kml_path = "test_data/sample.kml"
    
    if not os.path.exists(kml_path):
        print(f"   ⚠ Test file not found: {kml_path}")
    else:
        try:
            with open(kml_path, 'rb') as f:
                files = {'file': ('sample.kml', f, 'application/vnd.google-earth.kml+xml')}
                response = requests.post(
                    f"{BASE_URL}/maps/{map_id}/import_kml/",
                    files=files,
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code == 201:
                    result = response.json()
                    print(f"   ✓ KML imported successfully")
                    print(f"   Imported: {result.get('imported', 0)} features")
                    if result.get('warnings'):
                        print(f"   Warnings: {len(result['warnings'])}")
                else:
                    print(f"   ✗ KML import failed: {response.status_code}")
                    print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    # Step 5: Test CSV import
    print("\n5. Testing CSV coordinate import...")
    csv_path = "test_data/sample.csv"
    
    if not os.path.exists(csv_path):
        print(f"   ⚠ Test file not found: {csv_path}")
    else:
        try:
            with open(csv_path, 'rb') as f:
                files = {'file': ('sample.csv', f, 'text/csv')}
                data = {
                    'lat_col': 'lat',
                    'lng_col': 'lng',
                    'name_col': 'name'
                }
                response = requests.post(
                    f"{BASE_URL}/maps/{map_id}/import_coordinates/",
                    files=files,
                    data=data,
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code == 201:
                    result = response.json()
                    print(f"   ✓ CSV imported successfully")
                    print(f"   Imported: {result.get('imported', 0)} features")
                    if result.get('warnings'):
                        print(f"   Warnings: {len(result['warnings'])}")
                else:
                    print(f"   ✗ CSV import failed: {response.status_code}")
                    print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    # Step 6: Verify all imported features
    print("\n6. Verifying imported features...")
    try:
        response = requests.get(
            f"{BASE_URL}/maps/{map_id}/features/",
            headers=headers
        )
        if response.status_code == 200:
            features_list = response.json()
            features = features_list.get('results', features_list)
            print(f"   ✓ Retrieved {len(features)} total features")
            
            # Count by type
            points = sum(1 for f in features if f['feature_type'] == 'point')
            lines = sum(1 for f in features if f['feature_type'] == 'line')
            polygons = sum(1 for f in features if f['feature_type'] == 'polygon')
            
            print(f"   Points: {points}")
            print(f"   Lines: {lines}")
            print(f"   Polygons: {polygons}")
            
            # Show sample features
            print(f"\n   Sample features:")
            for feat in features[:5]:
                print(f"     - {feat['title']} ({feat['feature_type']})")
        else:
            print(f"   ✗ Feature retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Cleanup
    print("\n7. Cleaning up test data...")
    try:
        response = requests.delete(
            f"{BASE_URL}/maps/{map_id}/",
            headers=headers
        )
        if response.status_code == 204:
            print(f"   ✓ Test map deleted")
        else:
            print(f"   ⚠ Map deletion returned: {response.status_code}")
    except Exception as e:
        print(f"   ⚠ Cleanup error: {e}")
    
    print("\n" + "=" * 60)
    print("✓ FILE IMPORT TESTS COMPLETED!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_file_import()
    exit(0 if success else 1)
