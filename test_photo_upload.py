"""
Test photo upload functionality
"""
import requests
import io
from PIL import Image

# Login first
login_response = requests.post(
    'http://localhost:8000/api/auth/login/',
    json={'username': 'roylaffman', 'password': 'Laceyjones29'}
)
print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json()['access']
    print(f"Got token: {token[:20]}...")
    
    # Create a small test image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    # Try to upload to feature 5 (the one you created)
    files = {'image': ('test.jpg', img_bytes, 'image/jpeg')}
    data = {'feature': '85', 'caption': 'Test photo from script'}
    
    response = requests.post(
        'http://localhost:8000/api/v1/memory-maps/photos/',
        files=files,
        data=data,
        headers={'Authorization': f'Bearer {token}'}
    )
    
    print(f"\nPhoto upload status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        print("\n✅ Photo upload successful!")
        photo_data = response.json()
        print(f"Photo ID: {photo_data.get('id')}")
        print(f"Image URL: {photo_data.get('image')}")
    else:
        print("\n❌ Photo upload failed!")
else:
    print("Login failed!")
