"""
Django admin configuration for memory_maps app.
"""

from django.contrib import admin
from .models import Map

# Note: GIS admin will be added when PostGIS is configured
# from django.contrib.gis.admin import GISModelAdmin


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    """Admin interface for Map model."""
    
    list_display = ['title', 'owner', 'is_public', 'feature_count', 'created_at', 'updated_at']
    list_filter = ['is_public', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'owner__username']
    readonly_fields = ['created_at', 'updated_at', 'feature_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'owner', 'is_public')
        }),
        ('Map View Settings', {
            'fields': ('center_lat', 'center_lng', 'zoom_level')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'feature_count'),
            'classes': ('collapse',)
        }),
    )
    
    def feature_count(self, obj):
        """Display the number of features in the map."""
        return obj.feature_count
    feature_count.short_description = 'Features'
