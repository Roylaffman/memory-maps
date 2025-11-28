import { MapContainer, TileLayer, useMap, ZoomControl } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { useEffect } from 'react';

// Component to handle map initialization and updates
function MapController({ center, zoom }) {
  const map = useMap();
  
  useEffect(() => {
    if (center && zoom) {
      map.setView(center, zoom);
    }
  }, [center, zoom, map]);
  
  return null;
}

/**
 * MapView Component
 * Displays an interactive Leaflet map with OpenStreetMap tiles
 * 
 * @param {Object} props
 * @param {[number, number]} props.center - Map center coordinates [lat, lng]
 * @param {number} props.zoom - Initial zoom level
 * @param {number} props.minZoom - Minimum zoom level (default: 3)
 * @param {number} props.maxZoom - Maximum zoom level (default: 18)
 * @param {React.ReactNode} props.children - Child components (markers, polygons, etc.)
 */
function MapView({ 
  center = [37.7749, -122.4194], 
  zoom = 10, 
  minZoom = 3,
  maxZoom = 18,
  children 
}) {
  return (
    <MapContainer
      center={center}
      zoom={zoom}
      minZoom={minZoom}
      maxZoom={maxZoom}
      style={{ height: '100%', width: '100%' }}
      scrollWheelZoom={true}
      zoomControl={false} // We'll add it manually with better positioning
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        maxZoom={maxZoom}
      />
      <ZoomControl position="bottomright" />
      <MapController center={center} zoom={zoom} />
      {children}
    </MapContainer>
  );
}

export default MapView;
