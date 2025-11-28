import { Marker, Polygon } from 'react-leaflet';
import L from 'leaflet';
import FeaturePopup from './FeaturePopup';

// Fix for default marker icon in production builds
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

/**
 * MapFeatures Component
 * Renders map features (markers and polygons) with interactive popups
 * 
 * @param {Object} props
 * @param {Array} props.features - Array of feature objects to display
 * @param {Function} props.onFeatureEdit - Callback when a feature is edited
 * @param {Function} props.onFeatureDelete - Callback when a feature is deleted
 */
function MapFeatures({ features = [], onFeatureEdit, onFeatureDelete }) {
  const renderFeature = (feature) => {
    const { id, feature_type, geometry, title, description, category, stories, photos } = feature;

    // Handle Point features (markers)
    if (feature_type === 'point' && geometry?.type === 'Point') {
      const [lng, lat] = geometry.coordinates;
      return (
        <Marker key={id} position={[lat, lng]}>
          <FeaturePopup
            feature={{ id, title, description, category, stories, photos }}
            onEdit={onFeatureEdit}
            onDelete={onFeatureDelete}
          />
        </Marker>
      );
    }

    // Handle Polygon features
    if (feature_type === 'polygon' && geometry?.type === 'Polygon') {
      const positions = geometry.coordinates[0].map(([lng, lat]) => [lat, lng]);
      return (
        <Polygon
          key={id}
          positions={positions}
          pathOptions={{
            color: '#3388ff',
            weight: 3,
            opacity: 0.8,
            fillOpacity: 0.3
          }}
        >
          <FeaturePopup
            feature={{ id, title, description, category, stories, photos }}
            onEdit={onFeatureEdit}
            onDelete={onFeatureDelete}
          />
        </Polygon>
      );
    }

    return null;
  };

  return (
    <>
      {features.map(renderFeature)}
    </>
  );
}

export default MapFeatures;
