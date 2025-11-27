"""
DRF views and viewsets for memory_maps app.
Handles API endpoints for maps, features, stories, and photos.
"""

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404

from .models import Map, MapFeature, Story, Photo
from .serializers import (
    MapSerializer, MapListSerializer,
    MapFeatureSerializer, MapFeatureListSerializer,
    StorySerializer, PhotoSerializer
)
from .permissions import IsOwnerOrReadOnly


class MapViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Map model.
    Provides CRUD operations with owner-only access control.
    Public maps are visible to all users.
    """
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return maps based on user permissions.
        - Authenticated users see their own maps + public maps
        - Anonymous users see only public maps
        """
        queryset = Map.objects.select_related('owner')
        
        if self.request.user.is_authenticated:
            # Show user's own maps and public maps
            queryset = queryset.filter(
                Q(owner=self.request.user) | Q(is_public=True)
            )
        else:
            # Show only public maps to anonymous users
            queryset = queryset.filter(is_public=True)
        
        return queryset
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view."""
        if self.action == 'list':
            return MapListSerializer
        return MapSerializer
    
    def perform_create(self, serializer):
        """Set the owner to the current user when creating a map."""
        serializer.save(owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_maps(self, request):
        """
        Custom endpoint to get only the current user's maps.
        GET /api/maps/my_maps/
        """
        queryset = Map.objects.filter(owner=request.user).order_by('-created_at')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MapListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MapListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def public_maps(self, request):
        """
        Custom endpoint to get only public maps.
        GET /api/maps/public_maps/
        """
        queryset = Map.objects.filter(is_public=True).select_related('owner').order_by('-created_at')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MapListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MapListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def features(self, request, pk=None):
        """
        Get all features for a specific map.
        GET /api/maps/{id}/features/
        """
        map_obj = self.get_object()
        features = map_obj.features.order_by('-created_at')
        
        page = self.paginate_queryset(features)
        if page is not None:
            serializer = MapFeatureListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MapFeatureListSerializer(features, many=True)
        return Response(serializer.data)


class MapFeatureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for MapFeature model.
    Provides CRUD operations for map features with spatial data.
    """
    
    serializer_class = MapFeatureSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return features based on map visibility.
        Users can only see features from maps they own or public maps.
        """
        queryset = MapFeature.objects.select_related('map', 'map__owner')
        
        if self.request.user.is_authenticated:
            # Show features from user's maps and public maps
            queryset = queryset.filter(
                Q(map__owner=self.request.user) | Q(map__is_public=True)
            )
        else:
            # Show only features from public maps
            queryset = queryset.filter(map__is_public=True)
        
        # Filter by map_id if provided in query params
        map_id = self.request.query_params.get('map_id', None)
        if map_id is not None:
            queryset = queryset.filter(map_id=map_id)
        
        # Filter by feature_type if provided
        feature_type = self.request.query_params.get('feature_type', None)
        if feature_type is not None:
            queryset = queryset.filter(feature_type=feature_type)
        
        # Filter by category if provided
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__icontains=category)
        
        return queryset
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view."""
        if self.action == 'list':
            return MapFeatureListSerializer
        return MapFeatureSerializer
    
    def perform_create(self, serializer):
        """Validate user has permission to add features to the map."""
        map_obj = serializer.validated_data['map']
        if map_obj.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only add features to your own maps.")
        serializer.save()
    
    def perform_update(self, serializer):
        """Validate user has permission to update the feature."""
        if serializer.instance.map.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only update features on your own maps.")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Validate user has permission to delete the feature."""
        if instance.map.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete features from your own maps.")
        instance.delete()
    
    @action(detail=True, methods=['get'])
    def content(self, request, pk=None):
        """
        Get all content (stories and photos) for a specific feature.
        GET /api/features/{id}/content/
        """
        feature = self.get_object()
        
        stories = feature.stories.select_related('author').order_by('-created_at')
        photos = feature.photos.select_related('uploaded_by').order_by('-uploaded_at')
        
        return Response({
            'stories': StorySerializer(stories, many=True).data,
            'photos': PhotoSerializer(photos, many=True).data
        })


class StoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Story model.
    Provides CRUD operations for stories attached to map features.
    """
    
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return stories based on feature/map visibility.
        Users can only see stories from maps they own or public maps.
        """
        queryset = Story.objects.select_related(
            'feature', 'feature__map', 'author'
        )
        
        if self.request.user.is_authenticated:
            # Show stories from user's maps and public maps
            queryset = queryset.filter(
                Q(feature__map__owner=self.request.user) | Q(feature__map__is_public=True)
            )
        else:
            # Show only stories from public maps
            queryset = queryset.filter(feature__map__is_public=True)
        
        # Filter by feature_id if provided in query params
        feature_id = self.request.query_params.get('feature_id', None)
        if feature_id is not None:
            queryset = queryset.filter(feature_id=feature_id)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the author and validate permissions when creating a story."""
        feature = serializer.validated_data['feature']
        if feature.map.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only add stories to features on your own maps.")
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        """Validate user has permission to update the story."""
        if serializer.instance.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only update your own stories.")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Validate user has permission to delete the story."""
        if instance.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own stories.")
        instance.delete()


class PhotoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Photo model.
    Provides CRUD operations for photos attached to map features.
    Handles file uploads.
    """
    
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['uploaded_at']
    ordering = ['-uploaded_at']
    
    def get_queryset(self):
        """
        Return photos based on feature/map visibility.
        Users can only see photos from maps they own or public maps.
        """
        queryset = Photo.objects.select_related(
            'feature', 'feature__map', 'uploaded_by'
        )
        
        if self.request.user.is_authenticated:
            # Show photos from user's maps and public maps
            queryset = queryset.filter(
                Q(feature__map__owner=self.request.user) | Q(feature__map__is_public=True)
            )
        else:
            # Show only photos from public maps
            queryset = queryset.filter(feature__map__is_public=True)
        
        # Filter by feature_id if provided in query params
        feature_id = self.request.query_params.get('feature_id', None)
        if feature_id is not None:
            queryset = queryset.filter(feature_id=feature_id)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the uploader and validate permissions when uploading a photo."""
        feature = serializer.validated_data['feature']
        if feature.map.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only add photos to features on your own maps.")
        serializer.save(uploaded_by=self.request.user)
    
    def perform_update(self, serializer):
        """Validate user has permission to update the photo."""
        if serializer.instance.uploaded_by != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only update your own photos.")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Validate user has permission to delete the photo."""
        if instance.uploaded_by != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own photos.")
        instance.delete()



# GIS Import Views

from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from .gis_import import GeoJSONImporter, KMLImporter, CoordinateImporter


class MapImportMixin:
    """Mixin to add import functionality to MapViewSet."""
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def import_geojson(self, request, pk=None):
        """
        Import GeoJSON data to a map.
        POST /api/maps/{id}/import_geojson/
        
        Accepts either:
        - file: GeoJSON file upload
        - data: GeoJSON as JSON string in request body
        """
        map_obj = self.get_object()
        
        # Check if user owns the map
        if map_obj.owner != request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only import data to your own maps.")
        
        # Get GeoJSON data
        if 'file' in request.FILES:
            geojson_file = request.FILES['file']
            try:
                geojson_string = geojson_file.read().decode('utf-8')
            except UnicodeDecodeError:
                return Response(
                    {'error': 'File must be UTF-8 encoded'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif 'data' in request.data:
            geojson_string = request.data['data']
        else:
            return Response(
                {'error': 'Either "file" or "data" parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Import
        importer = GeoJSONImporter(map_obj)
        count, errors, warnings = importer.import_from_string(geojson_string)
        
        if errors:
            return Response({
                'success': False,
                'imported': count,
                'errors': errors,
                'warnings': warnings
            }, status=status.HTTP_400_BAD_REQUEST if count == 0 else status.HTTP_207_MULTI_STATUS)
        
        return Response({
            'success': True,
            'imported': count,
            'warnings': warnings,
            'features': [{'id': f.id, 'title': f.title} for f in importer.imported_features]
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def import_kml(self, request, pk=None):
        """
        Import KML/KMZ data to a map.
        POST /api/maps/{id}/import_kml/
        
        Accepts:
        - file: KML or KMZ file upload
        """
        map_obj = self.get_object()
        
        # Check if user owns the map
        if map_obj.owner != request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only import data to your own maps.")
        
        # Get file
        if 'file' not in request.FILES:
            return Response(
                {'error': '"file" parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        kml_file = request.FILES['file']
        
        # Import
        importer = KMLImporter(map_obj)
        count, errors, warnings = importer.import_from_file(kml_file)
        
        if errors:
            return Response({
                'success': False,
                'imported': count,
                'errors': errors,
                'warnings': warnings
            }, status=status.HTTP_400_BAD_REQUEST if count == 0 else status.HTTP_207_MULTI_STATUS)
        
        return Response({
            'success': True,
            'imported': count,
            'warnings': warnings,
            'features': [{'id': f.id, 'title': f.title} for f in importer.imported_features]
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def import_coordinates(self, request, pk=None):
        """
        Import coordinates from CSV to a map.
        POST /api/maps/{id}/import_coordinates/
        
        Accepts:
        - file: CSV file upload
        - lat_col: Name of latitude column (default: 'lat')
        - lng_col: Name of longitude column (default: 'lng')
        - name_col: Name of name column (default: 'name')
        """
        map_obj = self.get_object()
        
        # Check if user owns the map
        if map_obj.owner != request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only import data to your own maps.")
        
        # Get file
        if 'file' not in request.FILES:
            return Response(
                {'error': '"file" parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = request.FILES['file']
        
        # Get column names
        lat_col = request.data.get('lat_col', 'lat')
        lng_col = request.data.get('lng_col', 'lng')
        name_col = request.data.get('name_col', 'name')
        
        # Read CSV
        try:
            csv_content = csv_file.read().decode('utf-8')
        except UnicodeDecodeError:
            return Response(
                {'error': 'File must be UTF-8 encoded'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Import
        importer = CoordinateImporter(map_obj)
        count, errors, warnings = importer.import_from_csv(csv_content, lat_col, lng_col, name_col)
        
        if errors:
            return Response({
                'success': False,
                'imported': count,
                'errors': errors,
                'warnings': warnings
            }, status=status.HTTP_400_BAD_REQUEST if count == 0 else status.HTTP_207_MULTI_STATUS)
        
        return Response({
            'success': True,
            'imported': count,
            'warnings': warnings,
            'features': [{'id': f.id, 'title': f.title} for f in importer.imported_features]
        }, status=status.HTTP_201_CREATED)


# Update MapViewSet to include import functionality
MapViewSet.__bases__ = (MapImportMixin,) + MapViewSet.__bases__
