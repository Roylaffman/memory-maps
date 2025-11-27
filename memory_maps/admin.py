"""
Django admin configuration for memory_maps app.
"""

from django.contrib import admin
from .models import Map, MapFeature, Story, Photo, POSTGIS_ENABLED

# Import GIS admin if PostGIS is enabled
if POSTGIS_ENABLED:
    try:
        from django.contrib.gis.admin import GISModelAdmin as GeoModelAdmin
    except ImportError:
        GeoModelAdmin = admin.ModelAdmin
else:
    GeoModelAdmin = admin.ModelAdmin


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


@admin.register(MapFeature)
class MapFeatureAdmin(GeoModelAdmin):
    """Admin interface for MapFeature model."""
    
    list_display = ['title', 'feature_type', 'map', 'category', 'created_at']
    list_filter = ['feature_type', 'category', 'created_at']
    search_fields = ['title', 'description', 'map__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('map', 'title', 'description', 'category')
        }),
        ('Geographic Data', {
            'fields': ('feature_type', 'geometry')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Enable map widget for PostGIS geometry fields
    if POSTGIS_ENABLED:
        map_template = 'gis/admin/openlayers.html'
        default_lon = -74.0060
        default_lat = 40.7128
        default_zoom = 12


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    """Admin interface for Story model."""
    
    list_display = ['title', 'feature', 'author', 'word_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'author']
    search_fields = ['title', 'content', 'feature__title', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'word_count', 'preview']
    
    fieldsets = (
        ('Story Information', {
            'fields': ('feature', 'title', 'content', 'author')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'word_count', 'preview'),
            'classes': ('collapse',)
        }),
    )
    
    def word_count(self, obj):
        """Display the word count of the story."""
        return obj.word_count
    word_count.short_description = 'Words'
    
    def preview(self, obj):
        """Display a preview of the story content."""
        return obj.preview
    preview.short_description = 'Preview'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Admin interface for Photo model."""
    
    list_display = ['filename', 'feature', 'uploaded_by', 'file_size_mb', 'uploaded_at']
    list_filter = ['uploaded_at', 'uploaded_by']
    search_fields = ['caption', 'feature__title', 'uploaded_by__username']
    readonly_fields = ['uploaded_at', 'file_size_mb', 'filename', 'image_preview']
    
    fieldsets = (
        ('Photo Information', {
            'fields': ('feature', 'image', 'caption', 'uploaded_by')
        }),
        ('Metadata', {
            'fields': ('uploaded_at', 'file_size_mb', 'filename', 'image_preview'),
            'classes': ('collapse',)
        }),
    )
    
    def file_size_mb(self, obj):
        """Display the file size in MB."""
        return f"{obj.file_size_mb} MB"
    file_size_mb.short_description = 'File Size'
    
    def filename(self, obj):
        """Display just the filename."""
        return obj.filename
    filename.short_description = 'Filename'
    
    def image_preview(self, obj):
        """Display a thumbnail preview of the image."""
        if obj.image:
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'
