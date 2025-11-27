"""
Django models for memory_maps app.
Defines Map, MapFeature, Story, and Photo models with PostGIS support.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.conf import settings

# Import GIS models if PostGIS is enabled
try:
    from django.contrib.gis.db import models as gis_models
    from django.contrib.gis.geos import Point, Polygon, GEOSGeometry
    POSTGIS_ENABLED = True
except (ImportError, ImproperlyConfigured):
    POSTGIS_ENABLED = False
    # Fallback for development without PostGIS
    gis_models = None


class Map(models.Model):
    """
    Represents a personal memory map with geographic features.
    Each map has an owner, visibility settings, and default view parameters.
    """
    title = models.CharField(
        max_length=200,
        help_text="Title of the memory map"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the map and its purpose"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='memory_maps',
        help_text="User who created and owns this map"
    )
    is_public = models.BooleanField(
        default=False,
        help_text="Whether this map is publicly visible"
    )
    
    # Default map view settings
    center_lat = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        help_text="Latitude of the map center (-90 to 90)"
    )
    center_lng = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        help_text="Longitude of the map center (-180 to 180)"
    )
    zoom_level = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Default zoom level (1-20, where 1 is world view)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this map was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this map was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Memory Map'
        verbose_name_plural = 'Memory Maps'
        indexes = [
            models.Index(fields=['owner', '-created_at']),
            models.Index(fields=['is_public', '-created_at']),
        ]
    
    def __str__(self):
        """String representation of the map."""
        return f"{self.title} (by {self.owner.username})"
    
    def clean(self):
        """Validate model fields."""
        super().clean()
        
        # Validate latitude range
        if not -90.0 <= self.center_lat <= 90.0:
            raise ValidationError({
                'center_lat': 'Latitude must be between -90 and 90 degrees.'
            })
        
        # Validate longitude range
        if not -180.0 <= self.center_lng <= 180.0:
            raise ValidationError({
                'center_lng': 'Longitude must be between -180 and 180 degrees.'
            })
        
        # Validate zoom level
        if not 1 <= self.zoom_level <= 20:
            raise ValidationError({
                'zoom_level': 'Zoom level must be between 1 and 20.'
            })
    
    def save(self, *args, **kwargs):
        """Override save to run full_clean validation."""
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def feature_count(self):
        """Return the number of features in this map."""
        return self.features.count()
    
    @property
    def is_owned_by(self):
        """Return the owner's username for easy access."""
        return self.owner.username


class MapFeature(models.Model):
    """
    Represents a geographic feature (point or polygon) on a memory map.
    Features can contain stories, photos, and other content.
    Uses PostGIS geometry fields when available.
    """
    
    FEATURE_TYPES = [
        ('point', 'Point'),
        ('polygon', 'Polygon'),
    ]
    
    map = models.ForeignKey(
        Map,
        on_delete=models.CASCADE,
        related_name='features',
        help_text="The map this feature belongs to"
    )
    
    feature_type = models.CharField(
        max_length=10,
        choices=FEATURE_TYPES,
        help_text="Type of geographic feature (point or polygon)"
    )
    
    # PostGIS geometry field (when PostGIS is enabled)
    # For development without PostGIS, we store GeoJSON as text
    if POSTGIS_ENABLED:
        geometry = gis_models.GeometryField(
            help_text="PostGIS geometry (Point or Polygon)",
            spatial_index=True,
            srid=4326  # WGS84 coordinate system
        )
    else:
        # Fallback: store GeoJSON as text for SQLite development
        geometry = models.TextField(
            help_text="GeoJSON geometry representation (fallback for non-PostGIS)"
        )
    
    title = models.CharField(
        max_length=200,
        help_text="Title or name of this feature"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Description of this feature"
    )
    
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Category or type classification (e.g., 'permaculture', 'amenity')"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this feature was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this feature was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Map Feature'
        verbose_name_plural = 'Map Features'
        indexes = [
            models.Index(fields=['map', '-created_at']),
            models.Index(fields=['feature_type']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        """String representation of the feature."""
        return f"{self.title} ({self.feature_type}) on {self.map.title}"
    
    def clean(self):
        """Validate model fields."""
        super().clean()
        
        # Validate feature type matches geometry
        if POSTGIS_ENABLED and self.geometry:
            geom_type = self.geometry.geom_type.lower()
            
            if self.feature_type == 'point' and geom_type != 'point':
                raise ValidationError({
                    'geometry': f'Feature type is "point" but geometry is "{geom_type}"'
                })
            elif self.feature_type == 'polygon' and geom_type not in ['polygon', 'multipolygon']:
                raise ValidationError({
                    'geometry': f'Feature type is "polygon" but geometry is "{geom_type}"'
                })
        
        # For non-PostGIS, validate GeoJSON format
        if not POSTGIS_ENABLED and self.geometry:
            import json
            try:
                geojson = json.loads(self.geometry)
                if 'type' not in geojson or 'coordinates' not in geojson:
                    raise ValidationError({
                        'geometry': 'Invalid GeoJSON format: must have "type" and "coordinates"'
                    })
                
                # Validate type matches feature_type
                geom_type = geojson['type'].lower()
                if self.feature_type == 'point' and geom_type != 'point':
                    raise ValidationError({
                        'geometry': f'Feature type is "point" but GeoJSON type is "{geom_type}"'
                    })
                elif self.feature_type == 'polygon' and geom_type not in ['polygon', 'multipolygon']:
                    raise ValidationError({
                        'geometry': f'Feature type is "polygon" but GeoJSON type is "{geom_type}"'
                    })
            except json.JSONDecodeError as e:
                raise ValidationError({
                    'geometry': f'Invalid GeoJSON format: {str(e)}'
                })
    
    def save(self, *args, **kwargs):
        """Override save to run full_clean validation."""
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def story_count(self):
        """Return the number of stories attached to this feature."""
        return self.stories.count()
    
    @property
    def photo_count(self):
        """Return the number of photos attached to this feature."""
        return self.photos.count()
    
    def get_coordinates(self):
        """
        Get coordinates in a standardized format.
        Returns dict with 'type' and 'coordinates' keys.
        """
        if POSTGIS_ENABLED:
            return {
                'type': self.geometry.geom_type,
                'coordinates': list(self.geometry.coords) if hasattr(self.geometry, 'coords') else None
            }
        else:
            import json
            return json.loads(self.geometry)
    
    def set_point(self, latitude, longitude):
        """
        Set geometry as a point with given coordinates.
        
        Args:
            latitude: Latitude in decimal degrees (-90 to 90)
            longitude: Longitude in decimal degrees (-180 to 180)
        """
        if not -90.0 <= latitude <= 90.0:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not -180.0 <= longitude <= 180.0:
            raise ValueError("Longitude must be between -180 and 180 degrees")
        
        self.feature_type = 'point'
        
        if POSTGIS_ENABLED:
            self.geometry = Point(longitude, latitude, srid=4326)
        else:
            import json
            self.geometry = json.dumps({
                'type': 'Point',
                'coordinates': [longitude, latitude]
            })
    
    def set_polygon(self, coordinates):
        """
        Set geometry as a polygon with given coordinates.
        
        Args:
            coordinates: List of [longitude, latitude] pairs forming the polygon ring.
                        First and last coordinate should be the same (closed ring).
        """
        if not coordinates or len(coordinates) < 4:
            raise ValueError("Polygon must have at least 4 coordinates (closed ring)")
        
        # Ensure polygon is closed
        if coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])
        
        self.feature_type = 'polygon'
        
        if POSTGIS_ENABLED:
            self.geometry = Polygon(coordinates, srid=4326)
        else:
            import json
            self.geometry = json.dumps({
                'type': 'Polygon',
                'coordinates': [coordinates]
            })


class Story(models.Model):
    """
    Represents a text narrative or story attached to a map feature.
    Stories provide context, memories, and descriptions for geographic locations.
    """
    feature = models.ForeignKey(
        MapFeature,
        on_delete=models.CASCADE,
        related_name='stories',
        help_text="The map feature this story is attached to"
    )
    
    title = models.CharField(
        max_length=200,
        help_text="Title of the story"
    )
    
    content = models.TextField(
        help_text="The story content/narrative"
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='stories',
        help_text="User who wrote this story"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this story was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this story was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
        indexes = [
            models.Index(fields=['feature', '-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]
    
    def __str__(self):
        """String representation of the story."""
        return f"{self.title} by {self.author.username}"
    
    def clean(self):
        """Validate model fields."""
        super().clean()
        
        # Validate title is not empty or just whitespace
        if not self.title or not self.title.strip():
            raise ValidationError({
                'title': 'Story title cannot be empty or just whitespace.'
            })
        
        # Validate content is not empty or just whitespace
        if not self.content or not self.content.strip():
            raise ValidationError({
                'content': 'Story content cannot be empty or just whitespace.'
            })
        
        # Validate title length
        if len(self.title) > 200:
            raise ValidationError({
                'title': 'Story title cannot exceed 200 characters.'
            })
    
    def save(self, *args, **kwargs):
        """Override save to run full_clean validation."""
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def preview(self):
        """Return a preview of the story content (first 100 characters)."""
        if len(self.content) <= 100:
            return self.content
        return self.content[:97] + '...'
    
    @property
    def word_count(self):
        """Return the word count of the story content."""
        return len(self.content.split())


def photo_upload_path(instance, filename):
    """
    Generate upload path for photos.
    Path format: photos/{user_id}/{map_id}/{filename}
    """
    import os
    from django.utils.text import get_valid_filename
    
    # Get the map ID from the feature
    map_id = instance.feature.map.id
    user_id = instance.uploaded_by.id
    
    # Sanitize filename
    safe_filename = get_valid_filename(filename)
    
    # Return path
    return f'photos/{user_id}/{map_id}/{safe_filename}'


class Photo(models.Model):
    """
    Represents a photo attached to a map feature.
    Photos are stored in AWS S3 (or local storage in development).
    """
    feature = models.ForeignKey(
        MapFeature,
        on_delete=models.CASCADE,
        related_name='photos',
        help_text="The map feature this photo is attached to"
    )
    
    image = models.ImageField(
        upload_to=photo_upload_path,
        help_text="The photo image file"
    )
    
    caption = models.CharField(
        max_length=500,
        blank=True,
        help_text="Optional caption for the photo"
    )
    
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='photos',
        help_text="User who uploaded this photo"
    )
    
    # Timestamps
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this photo was uploaded"
    )
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
        indexes = [
            models.Index(fields=['feature', '-uploaded_at']),
            models.Index(fields=['uploaded_by', '-uploaded_at']),
        ]
    
    def __str__(self):
        """String representation of the photo."""
        return f"Photo for {self.feature.title} by {self.uploaded_by.username}"
    
    def clean(self):
        """Validate model fields."""
        super().clean()
        
        # Validate image file exists
        if not self.image:
            raise ValidationError({
                'image': 'Photo must have an image file.'
            })
        
        # Validate file size (max 10MB)
        if self.image.size > 10 * 1024 * 1024:
            raise ValidationError({
                'image': 'Image file size cannot exceed 10MB.'
            })
        
        # Validate file extension
        import os
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        ext = os.path.splitext(self.image.name)[1].lower()
        if ext not in valid_extensions:
            raise ValidationError({
                'image': f'Invalid file extension "{ext}". Allowed: {", ".join(valid_extensions)}'
            })
        
        # Validate caption length if provided
        if self.caption and len(self.caption) > 500:
            raise ValidationError({
                'caption': 'Caption cannot exceed 500 characters.'
            })
    
    def save(self, *args, **kwargs):
        """Override save to run full_clean validation."""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Override delete to remove the image file from storage."""
        # Delete the file from storage
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)
    
    @property
    def file_size_mb(self):
        """Return the file size in megabytes."""
        if self.image:
            return round(self.image.size / (1024 * 1024), 2)
        return 0
    
    @property
    def filename(self):
        """Return just the filename without the path."""
        import os
        if self.image:
            return os.path.basename(self.image.name)
        return None
