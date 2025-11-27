"""
DRF serializers for memory_maps app.
Handles serialization of spatial data and file uploads.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Map, MapFeature, Story, Photo

try:
    from rest_framework_gis.serializers import GeoFeatureModelSerializer
    POSTGIS_ENABLED = True
except (ImportError, Exception):
    # Handle both ImportError and GDAL configuration errors
    POSTGIS_ENABLED = False


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model (read-only for display purposes)."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'username', 'email']


class MapSerializer(serializers.ModelSerializer):
    """Serializer for Map model with owner information."""
    
    owner = UserSerializer(read_only=True)
    feature_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Map
        fields = [
            'id', 'title', 'description', 'owner', 'is_public',
            'center_lat', 'center_lng', 'zoom_level',
            'feature_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'feature_count', 'created_at', 'updated_at']
    
    def validate_center_lat(self, value):
        """Validate latitude is within valid range."""
        if not -90.0 <= value <= 90.0:
            raise serializers.ValidationError("Latitude must be between -90 and 90 degrees.")
        return value
    
    def validate_center_lng(self, value):
        """Validate longitude is within valid range."""
        if not -180.0 <= value <= 180.0:
            raise serializers.ValidationError("Longitude must be between -180 and 180 degrees.")
        return value
    
    def validate_zoom_level(self, value):
        """Validate zoom level is within valid range."""
        if not 1 <= value <= 20:
            raise serializers.ValidationError("Zoom level must be between 1 and 20.")
        return value


class MapListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for map listings."""
    
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    feature_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Map
        fields = [
            'id', 'title', 'description', 'owner_username', 'is_public',
            'center_lat', 'center_lng', 'zoom_level',
            'feature_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner_username', 'feature_count', 'created_at', 'updated_at']


class PhotoSerializer(serializers.ModelSerializer):
    """Serializer for Photo model."""
    
    uploaded_by = UserSerializer(read_only=True)
    file_size_mb = serializers.FloatField(read_only=True)
    filename = serializers.CharField(read_only=True)
    
    class Meta:
        model = Photo
        fields = [
            'id', 'feature', 'image', 'caption',
            'uploaded_by', 'uploaded_at',
            'file_size_mb', 'filename'
        ]
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'file_size_mb', 'filename']
    
    def validate_image(self, value):
        """Validate image file size and type."""
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Image file size cannot exceed 10MB.")
        
        # Check file extension
        import os
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(
                f'Invalid file extension "{ext}". Allowed: {", ".join(valid_extensions)}'
            )
        
        return value


class StorySerializer(serializers.ModelSerializer):
    """Serializer for Story model."""
    
    author = UserSerializer(read_only=True)
    word_count = serializers.IntegerField(read_only=True)
    preview = serializers.CharField(read_only=True)
    
    class Meta:
        model = Story
        fields = [
            'id', 'feature', 'title', 'content',
            'author', 'created_at', 'updated_at',
            'word_count', 'preview'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'word_count', 'preview']
    
    def validate_title(self, value):
        """Validate title is not empty or just whitespace."""
        if not value or not value.strip():
            raise serializers.ValidationError("Story title cannot be empty or just whitespace.")
        return value.strip()
    
    def validate_content(self, value):
        """Validate content is not empty or just whitespace."""
        if not value or not value.strip():
            raise serializers.ValidationError("Story content cannot be empty or just whitespace.")
        return value.strip()


class MapFeatureSerializer(serializers.ModelSerializer):
    """Serializer for MapFeature model with spatial data."""
    
    story_count = serializers.IntegerField(read_only=True)
    photo_count = serializers.IntegerField(read_only=True)
    stories = StorySerializer(many=True, read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    
    class Meta:
        model = MapFeature
        fields = [
            'id', 'map', 'feature_type', 'geometry',
            'title', 'description', 'category',
            'story_count', 'photo_count',
            'stories', 'photos',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'story_count', 'photo_count', 'created_at', 'updated_at']
    
    def validate_geometry(self, value):
        """Validate geometry data."""
        if POSTGIS_ENABLED:
            # PostGIS handles validation
            return value
        else:
            # For non-PostGIS, validate GeoJSON format
            import json
            if isinstance(value, str):
                try:
                    geojson = json.loads(value)
                except json.JSONDecodeError as e:
                    raise serializers.ValidationError(f'Invalid GeoJSON format: {str(e)}')
            else:
                geojson = value
            
            if 'type' not in geojson or 'coordinates' not in geojson:
                raise serializers.ValidationError(
                    'Invalid GeoJSON format: must have "type" and "coordinates"'
                )
            
            return value


class MapFeatureListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for feature listings without nested content."""
    
    story_count = serializers.IntegerField(read_only=True)
    photo_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = MapFeature
        fields = [
            'id', 'map', 'feature_type', 'geometry',
            'title', 'description', 'category',
            'story_count', 'photo_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'story_count', 'photo_count', 'created_at', 'updated_at']
