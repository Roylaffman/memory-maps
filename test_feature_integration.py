"""
Integration test to verify feature creation and attribute reading.
Tests the complete flow from creating a map to adding features with attributes.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api/v1/memory-maps"
AUTH_URL = "http://localhost:8000/api/auth"
USERNAME = "testuser"
PASSWORD = "testpass123"

def test_feature_workflow():
    """Test the complete feature creation and reading workflow."""
    
    print("=" * 60)
    print("FEATURE CREATION AND ATTRIBUTE READING TEST")
    print("=" * 60)
    
    # Step 1: Login (or create user if needed)
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
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        print("   Note: Make sure Django server is running on port 8000")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Create a test map
    print("\n2. Creating a test map...")
    map_data = {
        "title": "Test Map for Features",
        "description": "Testing feature creation and attributes",
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
            print(f"   Title: {map_obj['title']}")
        else:
            print(f"   ✗ Map creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 3: Create a point feature with attributes
    print("\n3. Creating a point feature with attributes...")
    feature_data = {
        "map": map_id,
        "feature_type": "point",
        "geometry": {
            "type": "Point",
            "coordinates": [-122.4194, 37.7749]
        },
        "title": "Golden Gate Park",
        "description": "A large urban park in San Francisco",
        "category": "Park"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/features/",
            json=feature_data,
            headers=headers
        )
        if response.status_code == 201:
            feature = response.json()
            feature_id = feature['id']
            print(f"   ✓ Feature created with ID: {feature_id}")
            print(f"   Title: {feature['title']}")
            print(f"   Type: {feature['feature_type']}")
            print(f"   Category: {feature['category']}")
        else:
            print(f"   ✗ Feature creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 4: Create a polygon feature
    print("\n4. Creating a polygon feature...")
    polygon_data = {
        "map": map_id,
        "feature_type": "polygon",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-122.42, 37.77],
                [-122.41, 37.77],
                [-122.41, 37.78],
                [-122.42, 37.78],
                [-122.42, 37.77]
            ]]
        },
        "title": "Neighborhood Area",
        "description": "A residential neighborhood",
        "category": "Residential"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/features/",
            json=polygon_data,
            headers=headers
        )
        if response.status_code == 201:
            polygon = response.json()
            polygon_id = polygon['id']
            print(f"   ✓ Polygon created with ID: {polygon_id}")
            print(f"   Title: {polygon['title']}")
        else:
            print(f"   ✗ Polygon creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 5: Add a story to the feature
    print("\n5. Adding a story to the feature...")
    story_data = {
        "feature": feature_id,
        "title": "My Visit to Golden Gate Park",
        "content": "I visited this beautiful park on a sunny day. The gardens were amazing!"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/stories/",
            json=story_data,
            headers=headers
        )
        if response.status_code == 201:
            story = response.json()
            print(f"   ✓ Story created with ID: {story['id']}")
            print(f"   Title: {story['title']}")
            print(f"   Word count: {story.get('word_count', 'N/A')}")
        else:
            print(f"   ✗ Story creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 6: Read feature with all attributes
    print("\n6. Reading feature with all attributes...")
    try:
        response = requests.get(
            f"{BASE_URL}/features/{feature_id}/",
            headers=headers
        )
        if response.status_code == 200:
            full_feature = response.json()
            print(f"   ✓ Feature retrieved successfully")
            print(f"   Title: {full_feature['title']}")
            print(f"   Description: {full_feature['description']}")
            print(f"   Category: {full_feature['category']}")
            print(f"   Geometry Type: {full_feature['geometry']['type']}")
            print(f"   Coordinates: {full_feature['geometry']['coordinates']}")
            print(f"   Stories: {full_feature.get('story_count', 0)}")
            print(f"   Photos: {full_feature.get('photo_count', 0)}")
            
            if full_feature.get('stories'):
                print(f"\n   Story Details:")
                for story in full_feature['stories']:
                    print(f"     - {story['title']}")
        else:
            print(f"   ✗ Feature retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 7: Get all features for the map
    print("\n7. Getting all features for the map...")
    try:
        response = requests.get(
            f"{BASE_URL}/maps/{map_id}/features/",
            headers=headers
        )
        if response.status_code == 200:
            features_list = response.json()
            features = features_list.get('results', features_list)
            print(f"   ✓ Retrieved {len(features)} features")
            for feat in features:
                print(f"     - {feat['title']} ({feat['feature_type']})")
        else:
            print(f"   ✗ Feature list retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 8: Update feature attributes
    print("\n8. Updating feature attributes...")
    update_data = {
        "description": "Updated: A large urban park with beautiful gardens and trails",
        "category": "Recreation"
    }
    
    try:
        response = requests.patch(
            f"{BASE_URL}/features/{feature_id}/",
            json=update_data,
            headers=headers
        )
        if response.status_code == 200:
            updated_feature = response.json()
            print(f"   ✓ Feature updated successfully")
            print(f"   New description: {updated_feature['description']}")
            print(f"   New category: {updated_feature['category']}")
        else:
            print(f"   ✗ Feature update failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Cleanup
    print("\n9. Cleaning up test data...")
    try:
        # Delete map (will cascade delete features and stories)
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
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_feature_workflow()
    exit(0 if success else 1)
