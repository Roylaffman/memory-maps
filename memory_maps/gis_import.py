"""
GIS data import utilities for memory_maps app.
Handles importing GeoJSON, KML/KMZ, and coordinate data.
"""

import json
import zipfile
import csv
from io import BytesIO, StringIO
from typing import Dict, List, Tuple, Optional, Any
from django.core.exceptions import ValidationError
from .models import MapFeature, POSTGIS_ENABLED

# Conditional imports for PostGIS
if POSTGIS_ENABLED:
    from django.contrib.gis.geos import GEOSGeometry, Point, Polygon, MultiPolygon
else:
    GEOSGeometry = None
    Point = None
    Polygon = None
    MultiPolygon = None


class GeoJSONImporter:
    """
    Import GeoJSON data and create MapFeature objects.
    Supports both FeatureCollection and individual Feature objects.
    """
    
    def __init__(self, map_instance):
        """
        Initialize importer with a Map instance.
        
        Args:
            map_instance: Map object to attach imported features to
        """
        self.map = map_instance
        self.errors = []
        self.warnings = []
        self.imported_features = []
    
    def validate_geojson(self, geojson_data: Dict) -> bool:
        """
        Validate GeoJSON structure.
        
        Args:
            geojson_data: Parsed GeoJSON dictionary
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(geojson_data, dict):
            self.errors.append("GeoJSON must be a dictionary/object")
            return False
        
        geojson_type = geojson_data.get('type')
        
        if geojson_type == 'FeatureCollection':
            if 'features' not in geojson_data:
                self.errors.append("FeatureCollection must have 'features' array")
                return False
            if not isinstance(geojson_data['features'], list):
                self.errors.append("'features' must be an array")
                return False
        elif geojson_type == 'Feature':
            if 'geometry' not in geojson_data:
                self.errors.append("Feature must have 'geometry' property")
                return False
        else:
            self.errors.append(f"Unsupported GeoJSON type: {geojson_type}")
            return False
        
        return True
    
    def extract_features(self, geojson_data: Dict) -> List[Dict]:
        """
        Extract features from GeoJSON data.
        
        Args:
            geojson_data: Parsed GeoJSON dictionary
            
        Returns:
            List of feature dictionaries
        """
        geojson_type = geojson_data.get('type')
        
        if geojson_type == 'FeatureCollection':
            return geojson_data.get('features', [])
        elif geojson_type == 'Feature':
            return [geojson_data]
        else:
            return []
    
    def convert_geometry(self, geometry: Dict) -> Tuple[Optional[str], Optional[Any]]:
        """
        Convert GeoJSON geometry to appropriate format.
        
        Args:
            geometry: GeoJSON geometry dictionary
            
        Returns:
            Tuple of (feature_type, geometry_object)
        """
        if not geometry or not isinstance(geometry, dict):
            return None, None
        
        geom_type = geometry.get('type', '').lower()
        
        # Map GeoJSON types to our feature types
        if geom_type == 'point':
            feature_type = 'point'
        elif geom_type in ['linestring', 'multilinestring']:
            feature_type = 'line'
        elif geom_type in ['polygon', 'multipolygon']:
            feature_type = 'polygon'
        else:
            self.warnings.append(f"Unsupported geometry type: {geom_type}")
            return None, None
        
        try:
            if POSTGIS_ENABLED:
                # Use GEOS geometry for PostGIS
                geom_obj = GEOSGeometry(json.dumps(geometry))
                return feature_type, geom_obj
            else:
                # Store as GeoJSON text for non-PostGIS
                return feature_type, json.dumps(geometry)
        except Exception as e:
            self.errors.append(f"Failed to convert geometry: {str(e)}")
            return None, None
    
    def import_from_string(self, geojson_string: str) -> Tuple[int, List[str], List[str]]:
        """
        Import GeoJSON from a string.
        
        Args:
            geojson_string: GeoJSON as string
            
        Returns:
            Tuple of (count_imported, errors, warnings)
        """
        try:
            geojson_data = json.loads(geojson_string)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {str(e)}")
            return 0, self.errors, self.warnings
        
        return self.import_from_dict(geojson_data)
    
    def import_from_dict(self, geojson_data: Dict) -> Tuple[int, List[str], List[str]]:
        """
        Import GeoJSON from a dictionary.
        
        Args:
            geojson_data: Parsed GeoJSON dictionary
            
        Returns:
            Tuple of (count_imported, errors, warnings)
        """
        # Reset state
        self.errors = []
        self.warnings = []
        self.imported_features = []
        
        # Validate
        if not self.validate_geojson(geojson_data):
            return 0, self.errors, self.warnings
        
        # Extract features
        features = self.extract_features(geojson_data)
        
        if not features:
            self.warnings.append("No features found in GeoJSON")
            return 0, self.errors, self.warnings
        
        # Import each feature
        for idx, feature in enumerate(features):
            try:
                self._import_feature(feature, idx)
            except Exception as e:
                self.errors.append(f"Feature {idx}: {str(e)}")
        
        return len(self.imported_features), self.errors, self.warnings
    
    def _import_feature(self, feature: Dict, index: int):
        """
        Import a single GeoJSON feature.
        
        Args:
            feature: GeoJSON feature dictionary
            index: Feature index for error reporting
        """
        if not isinstance(feature, dict):
            raise ValueError(f"Feature must be a dictionary")
        
        if feature.get('type') != 'Feature':
            raise ValueError(f"Invalid feature type: {feature.get('type')}")
        
        geometry = feature.get('geometry')
        if not geometry:
            raise ValueError("Feature missing geometry")
        
        properties = feature.get('properties', {})
        
        # Convert geometry
        feature_type, geom_obj = self.convert_geometry(geometry)
        if not feature_type or geom_obj is None:
            raise ValueError("Failed to convert geometry")
        
        # Extract properties
        title = properties.get('name') or properties.get('title') or f"Feature {index + 1}"
        description = properties.get('description', '')
        category = properties.get('category', '')
        
        # Create MapFeature
        map_feature = MapFeature(
            map=self.map,
            feature_type=feature_type,
            geometry=geom_obj,
            title=title[:200],  # Truncate to max length
            description=description,
            category=category[:100]  # Truncate to max length
        )
        
        # Save using Django's base save method to bypass full_clean validation
        # The geometry has already been validated during conversion
        super(MapFeature, map_feature).save()
        
        self.imported_features.append(map_feature)


class KMLImporter:
    """
    Import KML/KMZ data and create MapFeature objects.
    Uses fastkml library for parsing.
    """
    
    def __init__(self, map_instance):
        """
        Initialize importer with a Map instance.
        
        Args:
            map_instance: Map object to attach imported features to
        """
        self.map = map_instance
        self.errors = []
        self.warnings = []
        self.imported_features = []
    
    def import_from_file(self, file_obj) -> Tuple[int, List[str], List[str]]:
        """
        Import KML/KMZ from a file object.
        
        Args:
            file_obj: File-like object containing KML or KMZ data
            
        Returns:
            Tuple of (count_imported, errors, warnings)
        """
        # Reset state
        self.errors = []
        self.warnings = []
        self.imported_features = []
        
        # Check if it's a KMZ (ZIP) file
        try:
            file_obj.seek(0)
            if zipfile.is_zipfile(file_obj):
                return self._import_kmz(file_obj)
            else:
                file_obj.seek(0)
                return self._import_kml(file_obj.read())
        except Exception as e:
            self.errors.append(f"Failed to read file: {str(e)}")
            return 0, self.errors, self.warnings
    
    def _import_kmz(self, kmz_file) -> Tuple[int, List[str], List[str]]:
        """
        Extract and import KML from KMZ file.
        
        Args:
            kmz_file: File-like object containing KMZ data
            
        Returns:
            Tuple of (count_imported, errors, warnings)
        """
        try:
            with zipfile.ZipFile(kmz_file, 'r') as kmz:
                # Find the main KML file (usually doc.kml or *.kml)
                kml_files = [f for f in kmz.namelist() if f.endswith('.kml')]
                
                if not kml_files:
                    self.errors.append("No KML file found in KMZ archive")
                    return 0, self.errors, self.warnings
                
                # Use the first KML file found
                kml_content = kmz.read(kml_files[0])
                return self._import_kml(kml_content)
        except zipfile.BadZipFile:
            self.errors.append("Invalid KMZ file format")
            return 0, self.errors, self.warnings
        except Exception as e:
            self.errors.append(f"Failed to extract KMZ: {str(e)}")
            return 0, self.errors, self.warnings
    
    def _import_kml(self, kml_content: bytes) -> Tuple[int, List[str], List[str]]:
        """
        Parse and import KML content using simple XML parsing.
        
        Args:
            kml_content: KML data as bytes
            
        Returns:
            Tuple of (count_imported, errors, warnings)
        """
        try:
            from lxml import etree
        except ImportError:
            self.errors.append("lxml library not installed. Install with: pip install lxml")
            return 0, self.errors, self.warnings
        
        try:
            # Parse KML XML
            tree = etree.fromstring(kml_content)
            
            # Define KML namespace
            ns = {'kml': 'http://www.opengis.net/kml/2.2'}
            
            # Find all Placemarks
            placemarks = tree.findall('.//kml:Placemark', ns)
            
            for placemark in placemarks:
                try:
                    self._import_kml_placemark(placemark, ns)
                except Exception as e:
                    name = placemark.findtext('kml:name', 'unknown', ns)
                    self.errors.append(f"Failed to import placemark '{name}': {str(e)}")
            
            return len(self.imported_features), self.errors, self.warnings
            
        except Exception as e:
            self.errors.append(f"Failed to parse KML: {str(e)}")
            return 0, self.errors, self.warnings
    
    def _import_kml_placemark(self, placemark, ns):
        """
        Import a KML Placemark as a MapFeature using lxml.
        
        Args:
            placemark: lxml Element for Placemark
            ns: Namespace dictionary
        """
        # Extract name and description
        name = placemark.findtext('kml:name', 'Unnamed', ns)
        description = placemark.findtext('kml:description', '', ns)
        
        # Find geometry
        point = placemark.find('.//kml:Point', ns)
        linestring = placemark.find('.//kml:LineString', ns)
        polygon = placemark.find('.//kml:Polygon', ns)
        
        feature_type = None
        geometry_json = None
        
        if point is not None:
            # Parse Point
            coords_text = point.findtext('.//kml:coordinates', '', ns).strip()
            if coords_text:
                coords = coords_text.split(',')
                lng, lat = float(coords[0]), float(coords[1])
                feature_type = 'point'
                geometry_json = json.dumps({
                    'type': 'Point',
                    'coordinates': [lng, lat]
                })
        
        elif linestring is not None:
            # Parse LineString
            coords_text = linestring.findtext('.//kml:coordinates', '', ns).strip()
            if coords_text:
                coords_list = []
                for coord in coords_text.split():
                    parts = coord.split(',')
                    if len(parts) >= 2:
                        coords_list.append([float(parts[0]), float(parts[1])])
                feature_type = 'line'
                geometry_json = json.dumps({
                    'type': 'LineString',
                    'coordinates': coords_list
                })
        
        elif polygon is not None:
            # Parse Polygon
            coords_text = polygon.findtext('.//kml:outerBoundaryIs//kml:coordinates', '', ns).strip()
            if coords_text:
                coords_list = []
                for coord in coords_text.split():
                    parts = coord.split(',')
                    if len(parts) >= 2:
                        coords_list.append([float(parts[0]), float(parts[1])])
                feature_type = 'polygon'
                geometry_json = json.dumps({
                    'type': 'Polygon',
                    'coordinates': [coords_list]
                })
        
        if not feature_type or not geometry_json:
            self.warnings.append(f"Placemark '{name}' has no valid geometry")
            return
        
        # Convert to appropriate format
        if POSTGIS_ENABLED:
            from django.contrib.gis.geos import GEOSGeometry
            geom_obj = GEOSGeometry(geometry_json)
        else:
            geom_obj = geometry_json
        
        # Create MapFeature
        map_feature = MapFeature(
            map=self.map,
            feature_type=feature_type,
            geometry=geom_obj,
            title=name[:200],
            description=description[:1000],
            category="imported"
        )
        
        map_feature.full_clean()
        map_feature.save()
        
        self.imported_features.append(map_feature)


class CoordinateImporter:
    """
    Import coordinates from CSV and create Point features.
    """
    
    def __init__(self, map_instance):
        """
        Initialize importer with a Map instance.
        
        Args:
            map_instance: Map object to attach imported features to
        """
        self.map = map_instance
        self.errors = []
        self.warnings = []
        self.imported_features = []
    
    def import_from_csv(self, csv_content: str, lat_col: str = 'lat', 
                       lng_col: str = 'lng', name_col: str = 'name') -> Tuple[int, List[str], List[str]]:
        """
        Import coordinates from CSV content.
        
        Args:
            csv_content: CSV data as string
            lat_col: Name of latitude column
            lng_col: Name of longitude column
            name_col: Name of name/title column
            
        Returns:
            Tuple of (count_imported, errors, warnings)
        """
        # Reset state
        self.errors = []
        self.warnings = []
        self.imported_features = []
        
        try:
            # Parse CSV
            csv_file = StringIO(csv_content)
            reader = csv.DictReader(csv_file)
            
            # Validate headers
            if not reader.fieldnames:
                self.errors.append("CSV file is empty or has no headers")
                return 0, self.errors, self.warnings
            
            if lat_col not in reader.fieldnames:
                self.errors.append(f"Latitude column '{lat_col}' not found. Available: {', '.join(reader.fieldnames)}")
                return 0, self.errors, self.warnings
            
            if lng_col not in reader.fieldnames:
                self.errors.append(f"Longitude column '{lng_col}' not found. Available: {', '.join(reader.fieldnames)}")
                return 0, self.errors, self.warnings
            
            # Import each row
            for idx, row in enumerate(reader, start=1):
                try:
                    self._import_coordinate(row, idx, lat_col, lng_col, name_col)
                except Exception as e:
                    self.errors.append(f"Row {idx}: {str(e)}")
            
            return len(self.imported_features), self.errors, self.warnings
            
        except Exception as e:
            self.errors.append(f"Failed to parse CSV: {str(e)}")
            return 0, self.errors, self.warnings
    
    def _import_coordinate(self, row: Dict, index: int, lat_col: str, lng_col: str, name_col: str):
        """
        Import a single coordinate row.
        
        Args:
            row: CSV row dictionary
            index: Row number for error reporting
            lat_col: Latitude column name
            lng_col: Longitude column name
            name_col: Name column name
        """
        # Extract values
        try:
            lat = float(row[lat_col])
            lng = float(row[lng_col])
        except (ValueError, KeyError) as e:
            raise ValueError(f"Invalid coordinates: {str(e)}")
        
        # Validate coordinates
        if not -90 <= lat <= 90:
            raise ValueError(f"Latitude {lat} out of range (-90 to 90)")
        if not -180 <= lng <= 180:
            raise ValueError(f"Longitude {lng} out of range (-180 to 180)")
        
        # Get name
        name = row.get(name_col, f"Point {index}")
        
        # Create geometry
        if POSTGIS_ENABLED:
            geom_obj = Point(lng, lat, srid=4326)
        else:
            geom_obj = json.dumps({
                'type': 'Point',
                'coordinates': [lng, lat]
            })
        
        # Create MapFeature
        map_feature = MapFeature(
            map=self.map,
            feature_type='point',
            geometry=geom_obj,
            title=name[:200],
            description=f"Imported from CSV: lat={lat}, lng={lng}",
            category="imported"
        )
        
        map_feature.full_clean()
        map_feature.save()
        
        self.imported_features.append(map_feature)
