"""
Tests for memory_maps app.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from memory_maps.models import Map, MapFeature, Story, Photo, POSTGIS_ENABLED
import json
import os
from io import BytesIO
from PIL import Image

# Import PostGIS components if available
if POSTGIS_ENABLED:
    from django.contrib.gis.geos import Point, Polygon


class MapModelTest(TestCase):
    """Test cases for Map model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_map_creation(self):
        """Test creating a valid map."""
        map_obj = Map.objects.create(
            title='My Memory Map',
            description='A map of my favorite places',
            owner=self.user,
            center_lat=40.7128,
            center_lng=-74.0060,
            zoom_level=12
        )
        
        self.assertEqual(map_obj.title, 'My Memory Map')
        self.assertEqual(map_obj.description, 'A map of my favorite places')
        self.assertEqual(map_obj.owner, self.user)
        self.assertEqual(map_obj.center_lat, 40.7128)
        self.assertEqual(map_obj.center_lng, -74.0060)
        self.assertEqual(map_obj.zoom_level, 12)
        self.assertFalse(map_obj.is_public)
        self.assertIsNotNone(map_obj.created_at)
        self.assertIsNotNone(map_obj.updated_at)
    
    def test_map_string_representation(self):
        """Test map __str__ method."""
        map_obj = Map.objects.create(
            title='Test Map',
            owner=self.user,
            center_lat=0.0,
            center_lng=0.0
        )
        
        self.assertEqual(str(map_obj), 'Test Map (by testuser)')
    
    def test_map_default_values(self):
        """Test map default values."""
        map_obj = Map.objects.create(
            title='Test Map',
            owner=self.user,
            center_lat=0.0,
            center_lng=0.0
        )
        
        self.assertFalse(map_obj.is_public)
        self.assertEqual(map_obj.zoom_level, 10)
        self.assertEqual(map_obj.description, '')
    
    def test_map_latitude_validation_min(self):
        """Test that latitude below -90 raises validation error."""
        map_obj = Map(
            title='Test Map',
            owner=self.user,
            center_lat=-91.0,
            center_lng=0.0,
            zoom_level=10
        )
        
        with self.assertRaises(ValidationError) as context:
            map_obj.save()
        
        self.assertIn('center_lat', context.exception.message_dict)
    
    def test_map_latitude_validation_max(self):
        """Test that latitude above 90 raises validation error."""
        map_obj = Map(
            title='Test Map',
            owner=self.user,
            center_lat=91.0,
            center_lng=0.0,
            zoom_level=10
        )
        
        with self.assertRaises(ValidationError) as context:
            map_obj.save()
        
        self.assertIn('center_lat', context.exception.message_dict)
    
    def test_map_longitude_validation_min(self):
        """Test that longitude below -180 raises validation error."""
        map_obj = Map(
            title='Test Map',
            owner=self.user,
            center_lat=0.0,
            center_lng=-181.0,
            zoom_level=10
        )
        
        with self.assertRaises(ValidationError) as context:
            map_obj.save()
        
        self.assertIn('center_lng', context.exception.message_dict)
    
    def test_map_longitude_validation_max(self):
        """Test that longitude above 180 raises validation error."""
        map_obj = Map(
            title='Test Map',
            owner=self.user,
            center_lat=0.0,
            center_lng=181.0,
            zoom_level=10
        )
        
        with self.assertRaises(ValidationError) as context:
            map_obj.save()
        
        self.assertIn('center_lng', context.exception.message_dict)
    
    def test_map_zoom_level_validation_min(self):
        """Test that zoom level below 1 raises validation error."""
        map_obj = Map(
            title='Test Map',
            owner=self.user,
            center_lat=0.0,
            center_lng=0.0,
            zoom_level=0
        )
        
        with self.assertRaises(ValidationError) as context:
            map_obj.save()
        
        self.assertIn('zoom_level', context.exception.message_dict)
    
    def test_map_zoom_level_validation_max(self):
        """Test that zoom level above 20 raises validation error."""
        map_obj = Map(
            title='Test Map',
            owner=self.user,
            center_lat=0.0,
            center_lng=0.0,
            zoom_level=21
        )
        
        with self.assertRaises(ValidationError) as context:
            map_obj.save()
        
        self.assertIn('zoom_level', context.exception.message_dict)
    
    def test_map_valid_boundary_coordinates(self):
        """Test that boundary coordinate values are accepted."""
        # Test minimum valid values
        map_obj1 = Map.objects.create(
            title='Min Coords Map',
            owner=self.user,
            center_lat=-90.0,
            center_lng=-180.0,
            zoom_level=1
        )
        self.assertEqual(map_obj1.center_lat, -90.0)
        self.assertEqual(map_obj1.center_lng, -180.0)
        
        # Test maximum valid values
        map_obj2 = Map.objects.create(
            title='Max Coords Map',
            owner=self.user,
            center_lat=90.0,
            center_lng=180.0,
            zoom_level=20
        )
        self.assertEqual(map_obj2.center_lat, 90.0)
        self.assertEqual(map_obj2.center_lng, 180.0)
    
    def test_map_feature_count_property(self):
        """Test map feature_count property."""
        map_obj = Map.objects.create(
            title='Test Map',
            owner=self.user,
            center_lat=0.0,
            center_lng=0.0
        )
        
        self.assertEqual(map_obj.feature_count, 0)
        
        # Add features
        MapFeature.objects.create(
            map=map_obj,
            feature_type='point',
            geometry=json.dumps({'type': 'Point', 'coordinates': [0.0, 0.0]}),
            title='Feature 1'
        )
        
        MapFeature.objects.create(
            map=map_obj,
            feature_type='point',
            geometry=json.dumps({'type': 'Point', 'coordinates': [1.0, 1.0]}),
            title='Feature 2'
        )
        
        self.assertEqual(map_obj.feature_count, 2)
    
    def test_map_is_owned_by_property(self):
        """Test map is_owned_by property."""
        map_obj = Map.objects.create(
            title='Test Map',
            owner=self.user,
            center_lat=0.0,
            center_lng=0.0
        )
        
        self.assertEqual(map_obj.is_owned_by, 'testuser')
    
    def test_map_cascade_delete_with_owner(self):
        """Test that map is deleted when owner is deleted."""
        map_obj = Map.objects.create(
            title='Test Map',
            owner=self.user,
            center_lat=0.0,
            center_lng=0.0
        )
        
        map_id = map_obj.id
        self.user.delete()
        
        with self.assertRaises(Map.DoesNotExist):
            Map.objects.get(id=map_id)
    
    def test_map_public_visibility(self):
        """Test map public visibility setting."""
        map_obj = Map.objects.create(
            title='Public Map',
            owner=self.user,
            center_lat=0.0,
            center_lng=0.0,
            is_public=True
        )
        
        self.assertTrue(map_obj.is_public)


class MapFeatureModelTest(TestCase):
    """Test cases for MapFeature model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.map = Map.objects.create(
            title='Test Map',
            description='A test map',
            owner=self.user,
            center_lat=40.7128,
            center_lng=-74.0060,
            zoom_level=10
        )
    
    def test_feature_creation_point_geojson(self):
        """Test creating a point feature with GeoJSON."""
        feature = MapFeature.objects.create(
            map=self.map,
            feature_type='point',
            geometry=json.dumps({
                'type': 'Point',
                'coordinates': [-74.0060, 40.7128]
            }),
            title='Central Park',
            description='A beautiful park',
            category='park'
        )
        
        self.assertEqual(feature.feature_type, 'point')
        self.assertEqual(feature.title, 'Central Park')
        self.assertEqual(feature.description, 'A beautiful park')
        self.assertEqual(feature.category, 'park')
        self.assertEqual(feature.map, self.map)
    
    def test_feature_creation_polygon_geojson(self):
        """Test creating a polygon feature with GeoJSON."""
        coordinates = [
            [-74.0, 40.7],
            [-74.0, 40.8],
            [-73.9, 40.8],
            [-73.9, 40.7],
            [-74.0, 40.7]
        ]
        
        feature = MapFeature.objects.create(
            map=self.map,
            feature_type='polygon',
            geometry=json.dumps({
                'type': 'Polygon',
                'coordinates': [coordinates]
            }),
            title='Garden Area'
        )
        
        self.assertEqual(feature.feature_type, 'polygon')
        self.assertEqual(feature.title, 'Garden Area')
    
    def test_feature_string_representation(self):
        """Test feature __str__ method."""
        feature = MapFeature.objects.create(
            map=self.map,
            feature_type='point',
            geometry=json.dumps({'type': 'Point', 'coordinates': [0.0, 0.0]}),
            title='Test Feature'
        )
        
        self.assertEqual(str(feature), 'Test Feature (point) on Test Map')
    
    def test_feature_set_point_method(self):
        """Test set_point method for creating point geometry."""
        feature = MapFeature(
            map=self.map,
            title='Test Point'
        )
        
        feature.set_point(40.7128, -74.0060)
        feature.save()
        
        self.assertEqual(feature.feature_type, 'point')
        coords = feature.get_coordinates()
        self.assertEqual(coords['type'], 'Point')
    
    def test_feature_set_point_invalid_latitude(self):
        """Test set_point with invalid latitude."""
        feature = MapFeature(
            map=self.map,
            title='Test Point'
        )
        
        with self.assertRaises(ValueError):
            feature.set_point(91.0, 0.0)
        
        with self.assertRaises(ValueError):
            feature.set_point(-91.0, 0.0)
    
    def test_feature_set_point_invalid_longitude(self):
        """Test set_point with invalid longitude."""
        feature = MapFeature(
            map=self.map,
            title='Test Point'
        )
        
        with self.assertRaises(ValueError):
            feature.set_point(0.0, 181.0)
        
        with self.assertRaises(ValueError):
            feature.set_point(0.0, -181.0)
    
    def test_feature_set_polygon_method(self):
        """Test set_polygon method for creating polygon geometry."""
        feature = MapFeature(
            map=self.map,
            title='Test Polygon'
        )
        
        coordinates = [
            [-74.0, 40.7],
            [-74.0, 40.8],
            [-73.9, 40.8],
            [-73.9, 40.7],
            [-74.0, 40.7]
        ]
        
        feature.set_polygon(coordinates)
        feature.save()
        
        self.assertEqual(feature.feature_type, 'polygon')
        coords = feature.get_coordinates()
        self.assertEqual(coords['type'], 'Polygon')
    
    def test_feature_set_polygon_auto_close(self):
        """Test that set_polygon automatically closes the ring."""
        feature = MapFeature(
            map=self.map,
            title='Test Polygon'
        )
        
        # Provide unclosed ring
        coordinates = [
            [-74.0, 40.7],
            [-74.0, 40.8],
            [-73.9, 40.8],
            [-73.9, 40.7]
        ]
        
        feature.set_polygon(coordinates)
        feature.save()
        
        # Should be closed now
        coords = feature.get_coordinates()
        if POSTGIS_ENABLED:
            # PostGIS automatically handles ring closure
            self.assertEqual(feature.feature_type, 'polygon')
        else:
            # Check GeoJSON has closed ring
            geojson = json.loads(feature.geometry)
            ring = geojson['coordinates'][0]
            self.assertEqual(ring[0], ring[-1])
    
    def test_feature_set_polygon_insufficient_coordinates(self):
        """Test set_polygon with insufficient coordinates."""
        feature = MapFeature(
            map=self.map,
            title='Test Polygon'
        )
        
        with self.assertRaises(ValueError):
            feature.set_polygon([[0, 0], [1, 1]])
    
    def test_feature_type_mismatch_validation(self):
        """Test that feature type must match geometry type."""
        # Try to create point feature with polygon geometry
        feature = MapFeature(
            map=self.map,
            feature_type='point',
            geometry=json.dumps({
                'type': 'Polygon',
                'coordinates': [[[-74.0, 40.7], [-74.0, 40.8], [-73.9, 40.8], [-74.0, 40.7]]]
            }),
            title='Mismatched Feature'
        )
        
        with self.assertRaises(ValidationError) as context:
            feature.save()
        
        self.assertIn('geometry', context.exception.message_dict)
    
    def test_feature_invalid_geojson_format(self):
        """Test that invalid GeoJSON raises validation error."""
        feature = MapFeature(
            map=self.map,
            feature_type='point',
            geometry='{"invalid": "json"}',
            title='Invalid Feature'
        )
        
        with self.assertRaises(ValidationError) as context:
            feature.save()
        
        self.assertIn('geometry', context.exception.message_dict)
    
    def test_feature_malformed_json(self):
        """Test that malformed JSON raises validation error."""
        feature = MapFeature(
            map=self.map,
            feature_type='point',
            geometry='not valid json at all',
            title='Malformed Feature'
        )
        
        with self.assertRaises(ValidationError) as context:
            feature.save()
        
        self.assertIn('geometry', context.exception.message_dict)
    
    def test_feature_get_coordinates_method(self):
        """Test get_coordinates method."""
        feature = MapFeature.objects.create(
            map=self.map,
            feature_type='point',
            geometry=json.dumps({
                'type': 'Point',
                'coordinates': [-74.0060, 40.7128]
            }),
            title='Test Point'
        )
        
        coords = feature.get_coordinates()
        self.assertIn('type', coords)
        self.assertIn('coordinates', coords)
        self.assertEqual(coords['type'], 'Point')
    
    def test_feature_story_count_property(self):
        """Test feature story_count property."""
        feature = MapFeature.objects.create(
            map=self.map,
            feature_type='point',
            geometry=json.dumps({'type': 'Point', 'coordinates': [0.0, 0.0]}),
            title='Test Feature'
        )
        
        self.assertEqual(feature.story_count, 0)
        
        # Add stories
        Story.objects.create(
            feature=feature,
            title='Story 1',
            content='Content 1',
            author=self.user
        )
        
        Story.objects.create(
            feature=feature,
            title='Story 2',
            content='Content 2',
            author=self.user
        )
        
        self.assertEqual(feature.story_count, 2)
    
    def test_feature_photo_count_property(self):
        """Test feature photo_count property."""
        feature = MapFeature.objects.create(
            map=self.map,
            feature_type='point',
            geometry=json.dumps({'type': 'Point', 'coordinates': [0.0, 0.0]}),
            title='Test Feature'
        )
        
        self.assertEqual(feature.photo_count, 0)
    
    def test_feature_cascade_delete_with_map(self):
        """Test that feature is deleted when map is deleted."""
        feature = MapFeature.objects.create(
            map=self.map,
            feature_type='point',
            geometry=json.dumps({'type': 'Point', 'coordinates': [0.0, 0.0]}),
            title='Test Feature'
        )
        
        feature_id = feature.id
        self.map.delete()
        
        with self.assertRaises(MapFeature.DoesNotExist):
            MapFeature.objects.get(id=feature_id)
    
    def test_feature_optional_fields(self):
        """Test that description and category are optional."""
        feature = MapFeature.objects.create(
            map=self.map,
            feature_type='point',
            geometry=json.dumps({'type': 'Point', 'coordinates': [0.0, 0.0]}),
            title='Minimal Feature'
        )
        
        self.assertEqual(feature.description, '')
        self.assertEqual(feature.category, '')


class StoryModelTest(TestCase):
    """Test cases for Story model."""
    
    def setUp(self):
        """Set up test data."""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test map
        self.map = Map.objects.create(
            title='Test Map',
            description='A test map',
            owner=self.user,
            center_lat=40.7128,
            center_lng=-74.0060,
            zoom_level=10
        )
        
        # Create test feature
        self.feature = MapFeature.objects.create(
            map=self.map,
            feature_type='point',
            geometry=json.dumps({
                'type': 'Point',
                'coordinates': [-74.0060, 40.7128]
            }),
            title='Test Feature',
            description='A test feature'
        )
    
    def test_story_creation(self):
        """Test creating a valid story."""
        story = Story.objects.create(
            feature=self.feature,
            title='My Memory',
            content='This is a wonderful memory from this location.',
            author=self.user
        )
        
        self.assertEqual(story.title, 'My Memory')
        self.assertEqual(story.content, 'This is a wonderful memory from this location.')
        self.assertEqual(story.author, self.user)
        self.assertEqual(story.feature, self.feature)
        self.assertIsNotNone(story.created_at)
        self.assertIsNotNone(story.updated_at)
    
    def test_story_string_representation(self):
        """Test story __str__ method."""
        story = Story.objects.create(
            feature=self.feature,
            title='My Memory',
            content='Test content',
            author=self.user
        )
        
        self.assertEqual(str(story), 'My Memory by testuser')
    
    def test_story_empty_title_validation(self):
        """Test that empty title raises validation error."""
        story = Story(
            feature=self.feature,
            title='',
            content='Test content',
            author=self.user
        )
        
        with self.assertRaises(ValidationError) as context:
            story.save()
        
        self.assertIn('title', context.exception.message_dict)
    
    def test_story_whitespace_title_validation(self):
        """Test that whitespace-only title raises validation error."""
        story = Story(
            feature=self.feature,
            title='   ',
            content='Test content',
            author=self.user
        )
        
        with self.assertRaises(ValidationError) as context:
            story.save()
        
        self.assertIn('title', context.exception.message_dict)
    
    def test_story_empty_content_validation(self):
        """Test that empty content raises validation error."""
        story = Story(
            feature=self.feature,
            title='Test Title',
            content='',
            author=self.user
        )
        
        with self.assertRaises(ValidationError) as context:
            story.save()
        
        self.assertIn('content', context.exception.message_dict)
    
    def test_story_whitespace_content_validation(self):
        """Test that whitespace-only content raises validation error."""
        story = Story(
            feature=self.feature,
            title='Test Title',
            content='   ',
            author=self.user
        )
        
        with self.assertRaises(ValidationError) as context:
            story.save()
        
        self.assertIn('content', context.exception.message_dict)
    
    def test_story_title_max_length(self):
        """Test that title exceeding max length raises validation error."""
        story = Story(
            feature=self.feature,
            title='x' * 201,  # Exceeds 200 character limit
            content='Test content',
            author=self.user
        )
        
        with self.assertRaises(ValidationError) as context:
            story.save()
        
        self.assertIn('title', context.exception.message_dict)
    
    def test_story_preview_property(self):
        """Test story preview property."""
        # Short content
        story = Story.objects.create(
            feature=self.feature,
            title='Short Story',
            content='Short content',
            author=self.user
        )
        self.assertEqual(story.preview, 'Short content')
        
        # Long content
        long_content = 'x' * 150
        story2 = Story.objects.create(
            feature=self.feature,
            title='Long Story',
            content=long_content,
            author=self.user
        )
        self.assertEqual(len(story2.preview), 100)
        self.assertTrue(story2.preview.endswith('...'))
    
    def test_story_word_count_property(self):
        """Test story word count property."""
        story = Story.objects.create(
            feature=self.feature,
            title='Test Story',
            content='This is a test story with eight words.',
            author=self.user
        )
        
        self.assertEqual(story.word_count, 8)
    
    def test_story_cascade_delete_with_feature(self):
        """Test that story is deleted when feature is deleted."""
        story = Story.objects.create(
            feature=self.feature,
            title='Test Story',
            content='Test content',
            author=self.user
        )
        
        story_id = story.id
        self.feature.delete()
        
        with self.assertRaises(Story.DoesNotExist):
            Story.objects.get(id=story_id)
    
    def test_multiple_stories_per_feature(self):
        """Test that multiple stories can be attached to one feature."""
        story1 = Story.objects.create(
            feature=self.feature,
            title='Story 1',
            content='Content 1',
            author=self.user
        )
        
        story2 = Story.objects.create(
            feature=self.feature,
            title='Story 2',
            content='Content 2',
            author=self.user
        )
        
        self.assertEqual(self.feature.stories.count(), 2)
        self.assertIn(story1, self.feature.stories.all())
        self.assertIn(story2, self.feature.stories.all())


class PhotoModelTest(TestCase):
    """Test cases for Photo model."""
    
    def setUp(self):
        """Set up test data."""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test map
        self.map = Map.objects.create(
            title='Test Map',
            description='A test map',
            owner=self.user,
            center_lat=40.7128,
            center_lng=-74.0060,
            zoom_level=10
        )
        
        # Create test feature
        self.feature = MapFeature.objects.create(
            map=self.map,
            feature_type='point',
            geometry=json.dumps({
                'type': 'Point',
                'coordinates': [-74.0060, 40.7128]
            }),
            title='Test Feature',
            description='A test feature'
        )
    
    def create_test_image(self, filename='test.jpg', size=(100, 100), color='red'):
        """Helper method to create a test image file."""
        file = BytesIO()
        image = Image.new('RGB', size, color)
        image.save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile(
            filename,
            file.read(),
            content_type='image/jpeg'
        )
    
    def test_photo_creation(self):
        """Test creating a valid photo."""
        image = self.create_test_image()
        
        photo = Photo.objects.create(
            feature=self.feature,
            image=image,
            caption='A beautiful view',
            uploaded_by=self.user
        )
        
        self.assertEqual(photo.caption, 'A beautiful view')
        self.assertEqual(photo.uploaded_by, self.user)
        self.assertEqual(photo.feature, self.feature)
        self.assertIsNotNone(photo.uploaded_at)
        self.assertTrue(photo.image.name)
    
    def test_photo_string_representation(self):
        """Test photo __str__ method."""
        image = self.create_test_image()
        
        photo = Photo.objects.create(
            feature=self.feature,
            image=image,
            caption='Test caption',
            uploaded_by=self.user
        )
        
        self.assertEqual(str(photo), 'Photo for Test Feature by testuser')
    
    def test_photo_without_caption(self):
        """Test creating photo without caption (optional field)."""
        image = self.create_test_image()
        
        photo = Photo.objects.create(
            feature=self.feature,
            image=image,
            uploaded_by=self.user
        )
        
        self.assertEqual(photo.caption, '')
    
    def test_photo_caption_max_length(self):
        """Test that caption exceeding max length raises validation error."""
        image = self.create_test_image()
        
        photo = Photo(
            feature=self.feature,
            image=image,
            caption='x' * 501,  # Exceeds 500 character limit
            uploaded_by=self.user
        )
        
        with self.assertRaises(ValidationError) as context:
            photo.save()
        
        self.assertIn('caption', context.exception.message_dict)
    
    def test_photo_file_size_property(self):
        """Test photo file_size_mb property."""
        image = self.create_test_image()
        
        photo = Photo.objects.create(
            feature=self.feature,
            image=image,
            uploaded_by=self.user
        )
        
        self.assertIsInstance(photo.file_size_mb, float)
        self.assertGreaterEqual(photo.file_size_mb, 0)
    
    def test_photo_filename_property(self):
        """Test photo filename property."""
        image = self.create_test_image('mytest.jpg')
        
        photo = Photo.objects.create(
            feature=self.feature,
            image=image,
            uploaded_by=self.user
        )
        
        self.assertIsNotNone(photo.filename)
        self.assertTrue(photo.filename.endswith('.jpg'))
    
    def test_photo_cascade_delete_with_feature(self):
        """Test that photo is deleted when feature is deleted."""
        image = self.create_test_image()
        
        photo = Photo.objects.create(
            feature=self.feature,
            image=image,
            uploaded_by=self.user
        )
        
        photo_id = photo.id
        self.feature.delete()
        
        with self.assertRaises(Photo.DoesNotExist):
            Photo.objects.get(id=photo_id)
    
    def test_multiple_photos_per_feature(self):
        """Test that multiple photos can be attached to one feature."""
        image1 = self.create_test_image('photo1.jpg')
        image2 = self.create_test_image('photo2.jpg')
        
        photo1 = Photo.objects.create(
            feature=self.feature,
            image=image1,
            caption='Photo 1',
            uploaded_by=self.user
        )
        
        photo2 = Photo.objects.create(
            feature=self.feature,
            image=image2,
            caption='Photo 2',
            uploaded_by=self.user
        )
        
        self.assertEqual(self.feature.photos.count(), 2)
        self.assertIn(photo1, self.feature.photos.all())
        self.assertIn(photo2, self.feature.photos.all())
    
    def test_photo_upload_path(self):
        """Test that photo upload path follows expected format."""
        image = self.create_test_image('test.jpg')
        
        photo = Photo.objects.create(
            feature=self.feature,
            image=image,
            uploaded_by=self.user
        )
        
        # Path should be: photos/{user_id}/{map_id}/{filename}
        expected_path_parts = ['photos', str(self.user.id), str(self.map.id)]
        
        for part in expected_path_parts:
            self.assertIn(part, photo.image.name)



# API Integration Tests

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse


class MapAPITest(APITestCase):
    """Test cases for Map API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )
        
        # Create test maps
        self.map1 = Map.objects.create(
            title='User1 Private Map',
            description='Private map',
            owner=self.user1,
            center_lat=40.7128,
            center_lng=-74.0060,
            zoom_level=12,
            is_public=False
        )
        
        self.map2 = Map.objects.create(
            title='User1 Public Map',
            description='Public map',
            owner=self.user1,
            center_lat=40.7128,
            center_lng=-74.0060,
            zoom_level=12,
            is_public=True
        )
        
        self.map3 = Map.objects.create(
            title='User2 Public Map',
            description='Another public map',
            owner=self.user2,
            center_lat=51.5074,
            center_lng=-0.1278,
            zoom_level=10,
            is_public=True
        )
    
    def test_list_maps_authenticated(self):
        """Test listing maps as authenticated user."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:map-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User1 should see their own maps (2) + user2's public map (1) = 3
        self.assertEqual(len(response.data['results']), 3)
    
    def test_list_maps_unauthenticated(self):
        """Test listing maps as unauthenticated user."""
        url = reverse('memory_maps:map-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Anonymous users should only see public maps (2)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_create_map_authenticated(self):
        """Test creating a map as authenticated user."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:map-list')
        data = {
            'title': 'New Map',
            'description': 'A new test map',
            'center_lat': 34.0522,
            'center_lng': -118.2437,
            'zoom_level': 11,
            'is_public': False
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Map')
        self.assertEqual(response.data['owner']['username'], 'user1')
    
    def test_create_map_unauthenticated(self):
        """Test creating a map as unauthenticated user fails."""
        url = reverse('memory_maps:map-list')
        data = {
            'title': 'New Map',
            'center_lat': 34.0522,
            'center_lng': -118.2437,
            'zoom_level': 11
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_retrieve_own_map(self):
        """Test retrieving own map."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:map-detail', kwargs={'pk': self.map1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'User1 Private Map')
    
    def test_retrieve_public_map(self):
        """Test retrieving public map."""
        self.client.force_authenticate(user=self.user2)
        
        url = reverse('memory_maps:map-detail', kwargs={'pk': self.map2.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'User1 Public Map')
    
    def test_retrieve_other_private_map_fails(self):
        """Test retrieving another user's private map fails."""
        self.client.force_authenticate(user=self.user2)
        
        url = reverse('memory_maps:map-detail', kwargs={'pk': self.map1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_own_map(self):
        """Test updating own map."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:map-detail', kwargs={'pk': self.map1.id})
        data = {
            'title': 'Updated Map Title',
            'description': 'Updated description',
            'center_lat': 40.7128,
            'center_lng': -74.0060,
            'zoom_level': 15,
            'is_public': True
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Map Title')
        self.assertTrue(response.data['is_public'])
    
    def test_update_other_map_fails(self):
        """Test updating another user's map fails."""
        self.client.force_authenticate(user=self.user2)
        
        url = reverse('memory_maps:map-detail', kwargs={'pk': self.map1.id})
        data = {
            'title': 'Hacked Title',
            'center_lat': 40.7128,
            'center_lng': -74.0060,
            'zoom_level': 15
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_own_map(self):
        """Test deleting own map."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:map-detail', kwargs={'pk': self.map1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Map.objects.filter(id=self.map1.id).exists())
    
    def test_delete_other_map_fails(self):
        """Test deleting another user's map fails."""
        self.client.force_authenticate(user=self.user2)
        
        url = reverse('memory_maps:map-detail', kwargs={'pk': self.map1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Map.objects.filter(id=self.map1.id).exists())
    
    def test_my_maps_endpoint(self):
        """Test custom my_maps endpoint."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:map-my-maps')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User1 should only see their own maps (2)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_public_maps_endpoint(self):
        """Test custom public_maps endpoint."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:map-public-maps')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should see all public maps (2)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_search_maps(self):
        """Test searching maps by title."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:map-list')
        response = self.client.get(url, {'search': 'Public'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should find maps with "Public" in title
        self.assertGreater(len(response.data['results']), 0)


class MapFeatureAPITest(APITestCase):
    """Test cases for MapFeature API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )
        
        # Create test maps
        self.map1 = Map.objects.create(
            title='User1 Map',
            owner=self.user1,
            center_lat=40.7128,
            center_lng=-74.0060,
            zoom_level=12,
            is_public=False
        )
        
        self.map2 = Map.objects.create(
            title='User2 Public Map',
            owner=self.user2,
            center_lat=51.5074,
            center_lng=-0.1278,
            zoom_level=10,
            is_public=True
        )
        
        # Create test features
        self.feature1 = MapFeature.objects.create(
            map=self.map1,
            feature_type='point',
            geometry=json.dumps({'type': 'Point', 'coordinates': [-74.0060, 40.7128]}),
            title='Feature 1',
            category='park'
        )
        
        self.feature2 = MapFeature.objects.create(
            map=self.map2,
            feature_type='polygon',
            geometry=json.dumps({
                'type': 'Polygon',
                'coordinates': [[[-0.1, 51.5], [-0.1, 51.6], [-0.0, 51.6], [-0.0, 51.5], [-0.1, 51.5]]]
            }),
            title='Feature 2',
            category='garden'
        )
    
    def test_list_features_authenticated(self):
        """Test listing features as authenticated user."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:feature-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User1 should see their own features + public map features
        self.assertEqual(len(response.data['results']), 2)
    
    def test_list_features_unauthenticated(self):
        """Test listing features as unauthenticated user."""
        url = reverse('memory_maps:feature-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Anonymous users should only see features from public maps
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_feature_on_own_map(self):
        """Test creating a feature on own map."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:feature-list')
        data = {
            'map': self.map1.id,
            'feature_type': 'point',
            'geometry': json.dumps({'type': 'Point', 'coordinates': [-73.9, 40.8]}),
            'title': 'New Feature',
            'description': 'A new test feature',
            'category': 'landmark'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Feature')
    
    def test_create_feature_on_other_map_fails(self):
        """Test creating a feature on another user's map fails."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:feature-list')
        data = {
            'map': self.map2.id,
            'feature_type': 'point',
            'geometry': json.dumps({'type': 'Point', 'coordinates': [-0.1, 51.5]}),
            'title': 'Unauthorized Feature'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_feature_on_own_map(self):
        """Test updating a feature on own map."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:feature-detail', kwargs={'pk': self.feature1.id})
        data = {
            'map': self.map1.id,
            'feature_type': 'point',
            'geometry': json.dumps({'type': 'Point', 'coordinates': [-74.0060, 40.7128]}),
            'title': 'Updated Feature',
            'category': 'updated'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Feature')
    
    def test_update_feature_on_other_map_fails(self):
        """Test updating a feature on another user's map fails."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:feature-detail', kwargs={'pk': self.feature2.id})
        data = {
            'map': self.map2.id,
            'feature_type': 'polygon',
            'geometry': json.dumps({
                'type': 'Polygon',
                'coordinates': [[[-0.1, 51.5], [-0.1, 51.6], [-0.0, 51.6], [-0.0, 51.5], [-0.1, 51.5]]]
            }),
            'title': 'Hacked Feature'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_feature_on_own_map(self):
        """Test deleting a feature on own map."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:feature-detail', kwargs={'pk': self.feature1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MapFeature.objects.filter(id=self.feature1.id).exists())
    
    def test_delete_feature_on_other_map_fails(self):
        """Test deleting a feature on another user's map fails."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:feature-detail', kwargs={'pk': self.feature2.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(MapFeature.objects.filter(id=self.feature2.id).exists())
    
    def test_filter_features_by_map(self):
        """Test filtering features by map_id."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:feature-list')
        response = self.client.get(url, {'map_id': self.map1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Feature 1')
    
    def test_filter_features_by_type(self):
        """Test filtering features by feature_type."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:feature-list')
        response = self.client.get(url, {'feature_type': 'point'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_filter_features_by_category(self):
        """Test filtering features by category."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:feature-list')
        response = self.client.get(url, {'category': 'park'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class StoryAPITest(APITestCase):
    """Test cases for Story API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )
        
        # Create test map and feature
        self.map1 = Map.objects.create(
            title='User1 Map',
            owner=self.user1,
            center_lat=40.7128,
            center_lng=-74.0060,
            is_public=False
        )
        
        self.feature1 = MapFeature.objects.create(
            map=self.map1,
            feature_type='point',
            geometry=json.dumps({'type': 'Point', 'coordinates': [-74.0060, 40.7128]}),
            title='Feature 1'
        )
        
        # Create test story
        self.story1 = Story.objects.create(
            feature=self.feature1,
            title='My Story',
            content='This is my story content.',
            author=self.user1
        )
    
    def test_create_story_on_own_feature(self):
        """Test creating a story on own feature."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:story-list')
        data = {
            'feature': self.feature1.id,
            'title': 'New Story',
            'content': 'This is a new story about this place.'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Story')
        self.assertEqual(response.data['author']['username'], 'user1')
    
    def test_create_story_on_other_feature_fails(self):
        """Test creating a story on another user's feature fails."""
        # Create another user's map and feature
        map2 = Map.objects.create(
            title='User2 Map',
            owner=self.user2,
            center_lat=51.5074,
            center_lng=-0.1278
        )
        
        feature2 = MapFeature.objects.create(
            map=map2,
            feature_type='point',
            geometry=json.dumps({'type': 'Point', 'coordinates': [-0.1278, 51.5074]}),
            title='Feature 2'
        )
        
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:story-list')
        data = {
            'feature': feature2.id,
            'title': 'Unauthorized Story',
            'content': 'This should fail.'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_own_story(self):
        """Test updating own story."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:story-detail', kwargs={'pk': self.story1.id})
        data = {
            'feature': self.feature1.id,
            'title': 'Updated Story',
            'content': 'Updated content.'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Story')
    
    def test_update_other_story_fails(self):
        """Test updating another user's story fails."""
        self.client.force_authenticate(user=self.user2)
        
        url = reverse('memory_maps:story-detail', kwargs={'pk': self.story1.id})
        data = {
            'feature': self.feature1.id,
            'title': 'Hacked Story',
            'content': 'Hacked content.'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_own_story(self):
        """Test deleting own story."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:story-detail', kwargs={'pk': self.story1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Story.objects.filter(id=self.story1.id).exists())
    
    def test_delete_other_story_fails(self):
        """Test deleting another user's story fails."""
        self.client.force_authenticate(user=self.user2)
        
        url = reverse('memory_maps:story-detail', kwargs={'pk': self.story1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Story.objects.filter(id=self.story1.id).exists())
    
    def test_filter_stories_by_feature(self):
        """Test filtering stories by feature_id."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:story-list')
        response = self.client.get(url, {'feature_id': self.feature1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class PhotoAPITest(APITestCase):
    """Test cases for Photo API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )
        
        # Create test map and feature
        self.map1 = Map.objects.create(
            title='User1 Map',
            owner=self.user1,
            center_lat=40.7128,
            center_lng=-74.0060,
            is_public=False
        )
        
        self.feature1 = MapFeature.objects.create(
            map=self.map1,
            feature_type='point',
            geometry=json.dumps({'type': 'Point', 'coordinates': [-74.0060, 40.7128]}),
            title='Feature 1'
        )
    
    def create_test_image(self, filename='test.jpg', size=(100, 100), color='red'):
        """Helper method to create a test image file."""
        file = BytesIO()
        image = Image.new('RGB', size, color)
        image.save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile(
            filename,
            file.read(),
            content_type='image/jpeg'
        )
    
    def test_upload_photo_to_own_feature(self):
        """Test uploading a photo to own feature."""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:photo-list')
        image = self.create_test_image()
        
        data = {
            'feature': self.feature1.id,
            'image': image,
            'caption': 'A beautiful view'
        }
        
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['caption'], 'A beautiful view')
        self.assertEqual(response.data['uploaded_by']['username'], 'user1')
    
    def test_upload_photo_to_other_feature_fails(self):
        """Test uploading a photo to another user's feature fails."""
        # Create another user's map and feature
        map2 = Map.objects.create(
            title='User2 Map',
            owner=self.user2,
            center_lat=51.5074,
            center_lng=-0.1278
        )
        
        feature2 = MapFeature.objects.create(
            map=map2,
            feature_type='point',
            geometry=json.dumps({'type': 'Point', 'coordinates': [-0.1278, 51.5074]}),
            title='Feature 2'
        )
        
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:photo-list')
        image = self.create_test_image()
        
        data = {
            'feature': feature2.id,
            'image': image,
            'caption': 'Unauthorized photo'
        }
        
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_own_photo(self):
        """Test deleting own photo."""
        # Create a photo first
        image = self.create_test_image()
        photo = Photo.objects.create(
            feature=self.feature1,
            image=image,
            caption='Test photo',
            uploaded_by=self.user1
        )
        
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:photo-detail', kwargs={'pk': photo.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Photo.objects.filter(id=photo.id).exists())
    
    def test_delete_other_photo_fails(self):
        """Test deleting another user's photo fails."""
        # Create a photo
        image = self.create_test_image()
        photo = Photo.objects.create(
            feature=self.feature1,
            image=image,
            caption='Test photo',
            uploaded_by=self.user1
        )
        
        self.client.force_authenticate(user=self.user2)
        
        url = reverse('memory_maps:photo-detail', kwargs={'pk': photo.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Photo.objects.filter(id=photo.id).exists())
    
    def test_filter_photos_by_feature(self):
        """Test filtering photos by feature_id."""
        # Create a photo
        image = self.create_test_image()
        Photo.objects.create(
            feature=self.feature1,
            image=image,
            uploaded_by=self.user1
        )
        
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('memory_maps:photo-list')
        response = self.client.get(url, {'feature_id': self.feature1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)



# GIS Import Tests

class GeoJSONImportTest(APITestCase):
    """Test cases for GeoJSON import functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.map = Map.objects.create(
            title='Test Map',
            owner=self.user,
            center_lat=40.7128,
            center_lng=-74.0060
        )
    
    def test_import_geojson_feature_collection(self):
        """Test importing a GeoJSON FeatureCollection."""
        self.client.force_authenticate(user=self.user)
        
        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-74.0060, 40.7128]
                    },
                    "properties": {
                        "name": "Test Point",
                        "description": "A test point"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-74.0, 40.7],
                            [-74.0, 40.8],
                            [-73.9, 40.8],
                            [-73.9, 40.7],
                            [-74.0, 40.7]
                        ]]
                    },
                    "properties": {
                        "name": "Test Polygon"
                    }
                }
            ]
        }
        
        url = reverse('memory_maps:map-import-geojson', kwargs={'pk': self.map.id})
        response = self.client.post(url, {'data': json.dumps(geojson_data)}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['imported'], 2)
        self.assertEqual(MapFeature.objects.filter(map=self.map).count(), 2)
    
    def test_import_geojson_single_feature(self):
        """Test importing a single GeoJSON Feature."""
        self.client.force_authenticate(user=self.user)
        
        geojson_data = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-74.0060, 40.7128]
            },
            "properties": {
                "name": "Single Point"
            }
        }
        
        url = reverse('memory_maps:map-import-geojson', kwargs={'pk': self.map.id})
        response = self.client.post(url, {'data': json.dumps(geojson_data)}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['imported'], 1)
    
    def test_import_geojson_invalid_json(self):
        """Test importing invalid JSON."""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('memory_maps:map-import-geojson', kwargs={'pk': self.map.id})
        response = self.client.post(url, {'data': 'not valid json'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('errors', response.data)
    
    def test_import_geojson_unauthorized(self):
        """Test importing to another user's map fails."""
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.force_authenticate(user=other_user)
        
        geojson_data = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-74.0060, 40.7128]
            },
            "properties": {"name": "Test"}
        }
        
        url = reverse('memory_maps:map-import-geojson', kwargs={'pk': self.map.id})
        response = self.client.post(url, {'data': json.dumps(geojson_data)}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CoordinateImportTest(APITestCase):
    """Test cases for CSV coordinate import functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.map = Map.objects.create(
            title='Test Map',
            owner=self.user,
            center_lat=40.7128,
            center_lng=-74.0060
        )
    
    def test_import_coordinates_csv(self):
        """Test importing coordinates from CSV."""
        self.client.force_authenticate(user=self.user)
        
        csv_content = """name,lat,lng
Point 1,40.7128,-74.0060
Point 2,40.7589,-73.9851
Point 3,40.7614,-73.9776
"""
        
        csv_file = BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'coordinates.csv'
        
        url = reverse('memory_maps:map-import-coordinates', kwargs={'pk': self.map.id})
        response = self.client.post(url, {'file': csv_file}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['imported'], 3)
        self.assertEqual(MapFeature.objects.filter(map=self.map, feature_type='point').count(), 3)
    
    def test_import_coordinates_custom_columns(self):
        """Test importing coordinates with custom column names."""
        self.client.force_authenticate(user=self.user)
        
        csv_content = """location,latitude,longitude
Place 1,40.7128,-74.0060
Place 2,40.7589,-73.9851
"""
        
        csv_file = BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'coordinates.csv'
        
        url = reverse('memory_maps:map-import-coordinates', kwargs={'pk': self.map.id})
        response = self.client.post(url, {
            'file': csv_file,
            'lat_col': 'latitude',
            'lng_col': 'longitude',
            'name_col': 'location'
        }, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['imported'], 2)
    
    def test_import_coordinates_invalid_data(self):
        """Test importing coordinates with invalid data."""
        self.client.force_authenticate(user=self.user)
        
        csv_content = """name,lat,lng
Point 1,invalid,-74.0060
Point 2,40.7589,invalid
"""
        
        csv_file = BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'coordinates.csv'
        
        url = reverse('memory_maps:map-import-coordinates', kwargs={'pk': self.map.id})
        response = self.client.post(url, {'file': csv_file}, format='multipart')
        
        # Should have errors
        self.assertIn('errors', response.data)
        self.assertGreater(len(response.data['errors']), 0)
    
    def test_import_coordinates_out_of_range(self):
        """Test importing coordinates with out-of-range values."""
        self.client.force_authenticate(user=self.user)
        
        csv_content = """name,lat,lng
Point 1,91.0,-74.0060
Point 2,40.7589,-181.0
"""
        
        csv_file = BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'coordinates.csv'
        
        url = reverse('memory_maps:map-import-coordinates', kwargs={'pk': self.map.id})
        response = self.client.post(url, {'file': csv_file}, format='multipart')
        
        # Should have errors for out-of-range coordinates
        self.assertIn('errors', response.data)
        self.assertGreater(len(response.data['errors']), 0)


# GIS Import Unit Tests

from memory_maps.gis_import import GeoJSONImporter, KMLImporter, CoordinateImporter


class GeoJSONImporterTest(TestCase):
    """Test cases for GeoJSON import functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.map = Map.objects.create(
            title='Test Map',
            owner=self.user,
            center_lat=40.7128,
            center_lng=-74.0060
        )
    
    def test_import_valid_feature_collection(self):
        """Test importing a valid GeoJSON FeatureCollection."""
        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-74.0060, 40.7128]
                    },
                    "properties": {
                        "name": "Test Point",
                        "description": "A test point"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-74.0, 40.7],
                            [-74.0, 40.8],
                            [-73.9, 40.8],
                            [-73.9, 40.7],
                            [-74.0, 40.7]
                        ]]
                    },
                    "properties": {
                        "name": "Test Polygon",
                        "category": "garden"
                    }
                }
            ]
        }
        
        importer = GeoJSONImporter(self.map)
        count, errors, warnings = importer.import_from_dict(geojson_data)
        
        self.assertEqual(count, 2)
        self.assertEqual(len(errors), 0)
        self.assertEqual(MapFeature.objects.filter(map=self.map).count(), 2)
        
        # Verify point feature
        point_feature = MapFeature.objects.get(map=self.map, feature_type='point')
        self.assertEqual(point_feature.title, 'Test Point')
        self.assertEqual(point_feature.description, 'A test point')
        
        # Verify polygon feature
        polygon_feature = MapFeature.objects.get(map=self.map, feature_type='polygon')
        self.assertEqual(polygon_feature.title, 'Test Polygon')
        self.assertEqual(polygon_feature.category, 'garden')
    
    def test_import_single_feature(self):
        """Test importing a single GeoJSON Feature."""
        geojson_data = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-74.0060, 40.7128]
            },
            "properties": {
                "name": "Single Point"
            }
        }
        
        importer = GeoJSONImporter(self.map)
        count, errors, warnings = importer.import_from_dict(geojson_data)
        
        self.assertEqual(count, 1)
        self.assertEqual(len(errors), 0)
        self.assertEqual(MapFeature.objects.filter(map=self.map).count(), 1)
    
    def test_import_from_string(self):
        """Test importing GeoJSON from a string."""
        geojson_string = json.dumps({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-74.0060, 40.7128]
            },
            "properties": {
                "name": "String Point"
            }
        })
        
        importer = GeoJSONImporter(self.map)
        count, errors, warnings = importer.import_from_string(geojson_string)
        
        self.assertEqual(count, 1)
        self.assertEqual(len(errors), 0)
    
    def test_import_invalid_json(self):
        """Test that invalid JSON returns error."""
        importer = GeoJSONImporter(self.map)
        count, errors, warnings = importer.import_from_string("not valid json")
        
        self.assertEqual(count, 0)
        self.assertGreater(len(errors), 0)
        self.assertIn('Invalid JSON', errors[0])
    
    def test_import_invalid_geojson_type(self):
        """Test that invalid GeoJSON type returns error."""
        geojson_data = {
            "type": "InvalidType",
            "features": []
        }
        
        importer = GeoJSONImporter(self.map)
        count, errors, warnings = importer.import_from_dict(geojson_data)
        
        self.assertEqual(count, 0)
        self.assertGreater(len(errors), 0)
        self.assertIn('Unsupported GeoJSON type', errors[0])
    
    def test_import_feature_collection_without_features(self):
        """Test that FeatureCollection without features array returns error."""
        geojson_data = {
            "type": "FeatureCollection"
        }
        
        importer = GeoJSONImporter(self.map)
        count, errors, warnings = importer.import_from_dict(geojson_data)
        
        self.assertEqual(count, 0)
        self.assertGreater(len(errors), 0)
    
    def test_import_feature_without_geometry(self):
        """Test that feature without geometry returns error."""
        geojson_data = {
            "type": "Feature",
            "properties": {
                "name": "No Geometry"
            }
        }
        
        importer = GeoJSONImporter(self.map)
        count, errors, warnings = importer.import_from_dict(geojson_data)
        
        self.assertEqual(count, 0)
        self.assertGreater(len(errors), 0)
    
    def test_import_unsupported_geometry_type(self):
        """Test that unsupported geometry types generate warnings."""
        geojson_data = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[-74.0, 40.7], [-74.0, 40.8]]
            },
            "properties": {
                "name": "Line"
            }
        }
        
        importer = GeoJSONImporter(self.map)
        count, errors, warnings = importer.import_from_dict(geojson_data)
        
        self.assertEqual(count, 0)
        self.assertGreater(len(warnings), 0)
    
    def test_import_empty_feature_collection(self):
        """Test importing empty FeatureCollection."""
        geojson_data = {
            "type": "FeatureCollection",
            "features": []
        }
        
        importer = GeoJSONImporter(self.map)
        count, errors, warnings = importer.import_from_dict(geojson_data)
        
        self.assertEqual(count, 0)
        self.assertGreater(len(warnings), 0)
        self.assertIn('No features found', warnings[0])
    
    def test_import_feature_with_default_title(self):
        """Test that features without name get default title."""
        geojson_data = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-74.0060, 40.7128]
            },
            "properties": {}
        }
        
        importer = GeoJSONImporter(self.map)
        count, errors, warnings = importer.import_from_dict(geojson_data)
        
        self.assertEqual(count, 1)
        feature = MapFeature.objects.get(map=self.map)
        self.assertEqual(feature.title, 'Feature 1')
    
    def test_import_multipolygon(self):
        """Test importing MultiPolygon geometry."""
        geojson_data = {
            "type": "Feature",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[-74.0, 40.7], [-74.0, 40.8], [-73.9, 40.8], [-73.9, 40.7], [-74.0, 40.7]]]
                ]
            },
            "properties": {
                "name": "Multi Polygon"
            }
        }
        
        importer = GeoJSONImporter(self.map)
        count, errors, warnings = importer.import_from_dict(geojson_data)
        
        self.assertEqual(count, 1)
        feature = MapFeature.objects.get(map=self.map)
        self.assertEqual(feature.feature_type, 'polygon')
    
    def test_import_partial_success(self):
        """Test that valid features are imported even if some fail."""
        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-74.0060, 40.7128]
                    },
                    "properties": {"name": "Valid Point"}
                },
                {
                    "type": "Feature",
                    "properties": {"name": "No Geometry"}
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-73.9, 40.8]
                    },
                    "properties": {"name": "Another Valid Point"}
                }
            ]
        }
        
        importer = GeoJSONImporter(self.map)
        count, errors, warnings = importer.import_from_dict(geojson_data)
        
        self.assertEqual(count, 2)
        self.assertGreater(len(errors), 0)
        self.assertEqual(MapFeature.objects.filter(map=self.map).count(), 2)


class KMLImporterTest(TestCase):
    """Test cases for KML/KMZ import functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.map = Map.objects.create(
            title='Test Map',
            owner=self.user,
            center_lat=40.7128,
            center_lng=-74.0060
        )
    
    def create_kml_file(self, kml_content):
        """Helper to create a KML file object."""
        return BytesIO(kml_content.encode('utf-8'))
    
    def create_kmz_file(self, kml_content):
        """Helper to create a KMZ file object."""
        kmz_buffer = BytesIO()
        with zipfile.ZipFile(kmz_buffer, 'w', zipfile.ZIP_DEFLATED) as kmz:
            kmz.writestr('doc.kml', kml_content)
        kmz_buffer.seek(0)
        return kmz_buffer
    
    def test_import_valid_kml(self):
        """Test importing a valid KML file."""
        kml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Placemark>
      <name>Test Point</name>
      <description>A test point</description>
      <Point>
        <coordinates>-74.0060,40.7128,0</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>'''
        
        kml_file = self.create_kml_file(kml_content)
        
        importer = KMLImporter(self.map)
        count, errors, warnings = importer.import_from_file(kml_file)
        
        self.assertEqual(count, 1)
        self.assertEqual(len(errors), 0)
        self.assertEqual(MapFeature.objects.filter(map=self.map).count(), 1)
        
        feature = MapFeature.objects.get(map=self.map)
        self.assertEqual(feature.title, 'Test Point')
        self.assertEqual(feature.description, 'A test point')
        self.assertEqual(feature.feature_type, 'point')
    
    def test_import_valid_kmz(self):
        """Test importing a valid KMZ file."""
        kml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Placemark>
      <name>KMZ Point</name>
      <Point>
        <coordinates>-74.0060,40.7128,0</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>'''
        
        kmz_file = self.create_kmz_file(kml_content)
        
        importer = KMLImporter(self.map)
        count, errors, warnings = importer.import_from_file(kmz_file)
        
        self.assertEqual(count, 1)
        self.assertEqual(len(errors), 0)
        
        feature = MapFeature.objects.get(map=self.map)
        self.assertEqual(feature.title, 'KMZ Point')
    
    def test_import_kml_with_polygon(self):
        """Test importing KML with polygon geometry."""
        kml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Placemark>
      <name>Test Polygon</name>
      <Polygon>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>
              -74.0,40.7,0
              -74.0,40.8,0
              -73.9,40.8,0
              -73.9,40.7,0
              -74.0,40.7,0
            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>
  </Document>
</kml>'''
        
        kml_file = self.create_kml_file(kml_content)
        
        importer = KMLImporter(self.map)
        count, errors, warnings = importer.import_from_file(kml_file)
        
        self.assertEqual(count, 1)
        feature = MapFeature.objects.get(map=self.map)
        self.assertEqual(feature.feature_type, 'polygon')
    
    def test_import_kml_with_folders(self):
        """Test importing KML with nested folders."""
        kml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Folder>
      <name>Folder 1</name>
      <Placemark>
        <name>Point 1</name>
        <Point>
          <coordinates>-74.0,40.7,0</coordinates>
        </Point>
      </Placemark>
    </Folder>
    <Folder>
      <name>Folder 2</name>
      <Placemark>
        <name>Point 2</name>
        <Point>
          <coordinates>-73.9,40.8,0</coordinates>
        </Point>
      </Placemark>
    </Folder>
  </Document>
</kml>'''
        
        kml_file = self.create_kml_file(kml_content)
        
        importer = KMLImporter(self.map)
        count, errors, warnings = importer.import_from_file(kml_file)
        
        self.assertEqual(count, 2)
        self.assertEqual(MapFeature.objects.filter(map=self.map).count(), 2)
    
    def test_import_kmz_without_kml(self):
        """Test that KMZ without KML file returns error."""
        kmz_buffer = BytesIO()
        with zipfile.ZipFile(kmz_buffer, 'w', zipfile.ZIP_DEFLATED) as kmz:
            kmz.writestr('readme.txt', 'No KML here')
        kmz_buffer.seek(0)
        
        importer = KMLImporter(self.map)
        count, errors, warnings = importer.import_from_file(kmz_buffer)
        
        self.assertEqual(count, 0)
        self.assertGreater(len(errors), 0)
        self.assertIn('No KML file found', errors[0])
    
    def test_import_invalid_kml(self):
        """Test that invalid KML returns error."""
        kml_file = self.create_kml_file('not valid kml')
        
        importer = KMLImporter(self.map)
        count, errors, warnings = importer.import_from_file(kml_file)
        
        self.assertEqual(count, 0)
        self.assertGreater(len(errors), 0)
    
    def test_import_kml_placemark_without_geometry(self):
        """Test that placemarks without geometry generate warnings."""
        kml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Placemark>
      <name>No Geometry</name>
      <description>This has no geometry</description>
    </Placemark>
  </Document>
</kml>'''
        
        kml_file = self.create_kml_file(kml_content)
        
        importer = KMLImporter(self.map)
        count, errors, warnings = importer.import_from_file(kml_file)
        
        self.assertEqual(count, 0)
        self.assertGreater(len(warnings), 0)
    
    def test_import_kml_unnamed_placemark(self):
        """Test that unnamed placemarks get default name."""
        kml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Placemark>
      <Point>
        <coordinates>-74.0060,40.7128,0</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>'''
        
        kml_file = self.create_kml_file(kml_content)
        
        importer = KMLImporter(self.map)
        count, errors, warnings = importer.import_from_file(kml_file)
        
        self.assertEqual(count, 1)
        feature = MapFeature.objects.get(map=self.map)
        self.assertEqual(feature.title, 'Unnamed')


class CoordinateImporterTest(TestCase):
    """Test cases for CSV coordinate import functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.map = Map.objects.create(
            title='Test Map',
            owner=self.user,
            center_lat=40.7128,
            center_lng=-74.0060
        )
    
    def test_import_valid_csv(self):
        """Test importing valid CSV coordinates."""
        csv_content = '''lat,lng,name
40.7128,-74.0060,New York
34.0522,-118.2437,Los Angeles
41.8781,-87.6298,Chicago'''
        
        importer = CoordinateImporter(self.map)
        count, errors, warnings = importer.import_from_csv(csv_content)
        
        self.assertEqual(count, 3)
        self.assertEqual(len(errors), 0)
        self.assertEqual(MapFeature.objects.filter(map=self.map).count(), 3)
        
        # Verify features
        ny_feature = MapFeature.objects.get(map=self.map, title='New York')
        self.assertEqual(ny_feature.feature_type, 'point')
    
    def test_import_csv_custom_columns(self):
        """Test importing CSV with custom column names."""
        csv_content = '''latitude,longitude,city
40.7128,-74.0060,New York'''
        
        importer = CoordinateImporter(self.map)
        count, errors, warnings = importer.import_from_csv(
            csv_content,
            lat_col='latitude',
            lng_col='longitude',
            name_col='city'
        )
        
        self.assertEqual(count, 1)
        feature = MapFeature.objects.get(map=self.map)
        self.assertEqual(feature.title, 'New York')
    
    def test_import_csv_without_name_column(self):
        """Test importing CSV without name column uses default names."""
        csv_content = '''lat,lng
40.7128,-74.0060
34.0522,-118.2437'''
        
        importer = CoordinateImporter(self.map)
        count, errors, warnings = importer.import_from_csv(csv_content)
        
        self.assertEqual(count, 2)
        features = MapFeature.objects.filter(map=self.map).order_by('id')
        self.assertEqual(features[0].title, 'Point 1')
        self.assertEqual(features[1].title, 'Point 2')
    
    def test_import_csv_missing_lat_column(self):
        """Test that CSV without latitude column returns error."""
        csv_content = '''lng,name
-74.0060,New York'''
        
        importer = CoordinateImporter(self.map)
        count, errors, warnings = importer.import_from_csv(csv_content)
        
        self.assertEqual(count, 0)
        self.assertGreater(len(errors), 0)
        self.assertIn('Latitude column', errors[0])
    
    def test_import_csv_missing_lng_column(self):
        """Test that CSV without longitude column returns error."""
        csv_content = '''lat,name
40.7128,New York'''
        
        importer = CoordinateImporter(self.map)
        count, errors, warnings = importer.import_from_csv(csv_content)
        
        self.assertEqual(count, 0)
        self.assertGreater(len(errors), 0)
        self.assertIn('Longitude column', errors[0])
    
    def test_import_csv_invalid_coordinates(self):
        """Test that invalid coordinates generate errors."""
        csv_content = '''lat,lng,name
not_a_number,-74.0060,Invalid
40.7128,not_a_number,Also Invalid'''
        
        importer = CoordinateImporter(self.map)
        count, errors, warnings = importer.import_from_csv(csv_content)
        
        self.assertEqual(count, 0)
        self.assertEqual(len(errors), 2)
    
    def test_import_csv_out_of_range_latitude(self):
        """Test that out-of-range latitude generates error."""
        csv_content = '''lat,lng,name
91.0,-74.0060,Invalid Lat
-91.0,-74.0060,Also Invalid'''
        
        importer = CoordinateImporter(self.map)
        count, errors, warnings = importer.import_from_csv(csv_content)
        
        self.assertEqual(count, 0)
        self.assertEqual(len(errors), 2)
    
    def test_import_csv_out_of_range_longitude(self):
        """Test that out-of-range longitude generates error."""
        csv_content = '''lat,lng,name
40.7128,181.0,Invalid Lng
40.7128,-181.0,Also Invalid'''
        
        importer = CoordinateImporter(self.map)
        count, errors, warnings = importer.import_from_csv(csv_content)
        
        self.assertEqual(count, 0)
        self.assertEqual(len(errors), 2)
    
    def test_import_csv_partial_success(self):
        """Test that valid rows are imported even if some fail."""
        csv_content = '''lat,lng,name
40.7128,-74.0060,Valid Point
invalid,-74.0060,Invalid Point
34.0522,-118.2437,Another Valid Point'''
        
        importer = CoordinateImporter(self.map)
        count, errors, warnings = importer.import_from_csv(csv_content)
        
        self.assertEqual(count, 2)
        self.assertEqual(len(errors), 1)
        self.assertEqual(MapFeature.objects.filter(map=self.map).count(), 2)
    
    def test_import_empty_csv(self):
        """Test that empty CSV returns error."""
        csv_content = ''
        
        importer = CoordinateImporter(self.map)
        count, errors, warnings = importer.import_from_csv(csv_content)
        
        self.assertEqual(count, 0)
        self.assertGreater(len(errors), 0)
    
    def test_import_csv_boundary_coordinates(self):
        """Test importing coordinates at valid boundaries."""
        csv_content = '''lat,lng,name
90.0,180.0,North East
-90.0,-180.0,South West
0.0,0.0,Origin'''
        
        importer = CoordinateImporter(self.map)
        count, errors, warnings = importer.import_from_csv(csv_content)
        
        self.assertEqual(count, 3)
        self.assertEqual(len(errors), 0)
