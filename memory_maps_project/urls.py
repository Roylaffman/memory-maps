"""
URL configuration for memory_maps_project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API root endpoint."""
    return Response({
        'message': 'Memory Maps API',
        'version': 'v1',
        'endpoints': {
            'admin': request.build_absolute_uri('/admin/'),
            'memory_maps': request.build_absolute_uri('/api/v1/memory-maps/'),
            'auth': {
                'login': request.build_absolute_uri('/api/auth/login/'),
                'refresh': request.build_absolute_uri('/api/auth/refresh/'),
                'user': request.build_absolute_uri('/api/auth/user/'),
            }
        }
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    path('api/v1/memory-maps/', include('memory_maps.urls')),
    path('api/auth/', include('memory_maps.auth_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
