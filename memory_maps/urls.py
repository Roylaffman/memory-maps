"""
URL configuration for memory_maps app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MapViewSet, MapFeatureViewSet, StoryViewSet, PhotoViewSet

app_name = 'memory_maps'

router = DefaultRouter()

# Register viewsets
router.register(r'maps', MapViewSet, basename='map')
router.register(r'features', MapFeatureViewSet, basename='feature')
router.register(r'stories', StoryViewSet, basename='story')
router.register(r'photos', PhotoViewSet, basename='photo')

urlpatterns = [
    path('', include(router.urls)),
]
