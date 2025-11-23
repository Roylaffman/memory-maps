"""
Django models for memory_maps app.
Defines Map, MapFeature, Story, and Photo models with PostGIS support.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Note: GIS models will be implemented when PostGIS is configured
# from django.contrib.gis.db import models as gis_models


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
