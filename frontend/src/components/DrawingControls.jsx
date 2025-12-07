import { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet-draw';
import 'leaflet-draw/dist/leaflet.draw.css';

/**
 * DrawingControls Component
 * Adds Leaflet.draw controls for creating points and polygons
 * 
 * @param {Object} props
 * @param {Function} props.onFeatureCreated - Callback when a feature is drawn (receives layer and type)
 * @param {Function} props.onFeatureEdited - Callback when features are edited (receives layers)
 * @param {Function} props.onFeatureDeleted - Callback when features are deleted (receives layers)
 * @param {L.FeatureGroup} props.editableLayer - Optional feature group containing editable features
 */
function DrawingControls({ onFeatureCreated, onFeatureEdited, onFeatureDeleted, editableLayer }) {
  const map = useMap();

  useEffect(() => {
    // Use provided editable layer or create a new one
    const drawnItems = editableLayer || new L.FeatureGroup();
    if (!editableLayer) {
      map.addLayer(drawnItems);
    }

    // Configure drawing controls
    const drawControl = new L.Control.Draw({
      position: 'topright',
      draw: {
        polygon: {
          allowIntersection: false,
          showArea: true,
          drawError: {
            color: '#e74c3c',
            message: '<strong>Error:</strong> Shape edges cannot cross!'
          },
          shapeOptions: {
            color: '#3388ff',
            weight: 3,
            opacity: 0.8,
            fillOpacity: 0.3
          }
        },
        polyline: {
          shapeOptions: {
            color: '#3388ff',
            weight: 3,
            opacity: 0.8
          }
        },
        circle: false, // Disable circle drawing
        rectangle: {
          shapeOptions: {
            color: '#3388ff',
            weight: 3,
            opacity: 0.8,
            fillOpacity: 0.3
          }
        },
        marker: {
          icon: L.icon({
            iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
            iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
            shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
          })
        },
        circlemarker: false // Disable circle marker
      },
      edit: {
        featureGroup: drawnItems,
        remove: true
      }
    });

    map.addControl(drawControl);

    // Event handlers
    const handleCreated = (e) => {
      const { layer, layerType } = e;
      drawnItems.addLayer(layer);
      
      if (onFeatureCreated) {
        // Extract geometry data
        let geometry;
        if (layerType === 'marker') {
          const latlng = layer.getLatLng();
          geometry = {
            type: 'Point',
            coordinates: [latlng.lng, latlng.lat]
          };
        } else if (layerType === 'polyline') {
          const latlngs = layer.getLatLngs();
          geometry = {
            type: 'LineString',
            coordinates: latlngs.map(ll => [ll.lng, ll.lat])
          };
        } else if (layerType === 'polygon' || layerType === 'rectangle') {
          const latlngs = layer.getLatLngs()[0];
          geometry = {
            type: 'Polygon',
            coordinates: [latlngs.map(ll => [ll.lng, ll.lat])]
          };
        }
        
        onFeatureCreated({
          layer,
          type: layerType,
          geometry
        });
      }
    };

    const handleEdited = (e) => {
      const { layers } = e;
      if (onFeatureEdited) {
        const editedFeatures = [];
        layers.eachLayer((layer) => {
          let geometry;
          if (layer instanceof L.Marker) {
            const latlng = layer.getLatLng();
            geometry = {
              type: 'Point',
              coordinates: [latlng.lng, latlng.lat]
            };
          } else if (layer instanceof L.Polyline && !(layer instanceof L.Polygon)) {
            const latlngs = layer.getLatLngs();
            geometry = {
              type: 'LineString',
              coordinates: latlngs.map(ll => [ll.lng, ll.lat])
            };
          } else if (layer instanceof L.Polygon) {
            const latlngs = layer.getLatLngs()[0];
            geometry = {
              type: 'Polygon',
              coordinates: [latlngs.map(ll => [ll.lng, ll.lat])]
            };
          }
          editedFeatures.push({ layer, geometry });
        });
        onFeatureEdited(editedFeatures);
      }
    };

    const handleDeleted = (e) => {
      const { layers } = e;
      if (onFeatureDeleted) {
        const deletedFeatures = [];
        layers.eachLayer((layer) => {
          deletedFeatures.push(layer);
        });
        onFeatureDeleted(deletedFeatures);
      }
    };

    // Attach event listeners
    map.on(L.Draw.Event.CREATED, handleCreated);
    map.on(L.Draw.Event.EDITED, handleEdited);
    map.on(L.Draw.Event.DELETED, handleDeleted);

    // Cleanup
    return () => {
      map.off(L.Draw.Event.CREATED, handleCreated);
      map.off(L.Draw.Event.EDITED, handleEdited);
      map.off(L.Draw.Event.DELETED, handleDeleted);
      map.removeControl(drawControl);
      if (!editableLayer) {
        map.removeLayer(drawnItems);
      }
    };
  }, [map, onFeatureCreated, onFeatureEdited, onFeatureDeleted, editableLayer]);

  return null;
}

export default DrawingControls;
