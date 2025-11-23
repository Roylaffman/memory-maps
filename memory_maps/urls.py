"""
URL configuration for memory_maps app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'memory_maps'

router = DefaultRouter()

# ViewSets will be registered here as they are created
# Example: router.register(r'maps', MapViewSet, basename='map')

urlpatterns = [
    path('', include(router.urls)),
]
