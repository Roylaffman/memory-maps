import { useState } from 'react'
import MapView from './components/MapView'
import DrawingControls from './components/DrawingControls'
import MapFeatures from './components/MapFeatures'
import './App.css'

function App() {
  // Default center: San Francisco coordinates
  const [mapCenter] = useState([37.7749, -122.4194]);
  const [mapZoom] = useState(10);
  const [features, setFeatures] = useState([]);

  // Handle new feature creation
  const handleFeatureCreated = ({ layer, type, geometry }) => {
    const newFeature = {
      id: Date.now(), // Temporary ID
      feature_type: type === 'marker' ? 'point' : 'polygon',
      geometry,
      title: `New ${type === 'marker' ? 'Point' : 'Polygon'}`,
      description: 'Click edit to add details',
      category: '',
      stories: [],
      photos: []
    };
    
    setFeatures(prev => [...prev, newFeature]);
    console.log('Feature created:', newFeature);
  };

  // Handle feature editing
  const handleFeatureEdit = (feature) => {
    console.log('Edit feature:', feature);
    // TODO: Open edit modal/form in Task 5.3
    alert(`Edit feature: ${feature.title}\n(Feature editing UI will be implemented in Task 5.3)`);
  };

  // Handle feature deletion
  const handleFeatureDelete = (feature) => {
    if (confirm(`Delete "${feature.title}"?`)) {
      setFeatures(prev => prev.filter(f => f.id !== feature.id));
      console.log('Feature deleted:', feature);
    }
  };

  // Handle features edited via drawing controls
  const handleFeaturesEdited = (editedFeatures) => {
    console.log('Features edited:', editedFeatures);
    // Update geometries of edited features
    // This is a simplified version - full implementation would match by layer ID
  };

  // Handle features deleted via drawing controls
  const handleFeaturesDeleted = (deletedLayers) => {
    console.log('Features deleted via drawing controls:', deletedLayers);
    // In a full implementation, we'd match layers to features and remove them
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Personal Memory Maps</h1>
        <div className="header-info">
          <span className="feature-count">{features.length} features</span>
        </div>
      </header>
      <main className="map-container">
        <MapView center={mapCenter} zoom={mapZoom}>
          <DrawingControls 
            onFeatureCreated={handleFeatureCreated}
            onFeatureEdited={handleFeaturesEdited}
            onFeatureDeleted={handleFeaturesDeleted}
          />
          <MapFeatures 
            features={features}
            onFeatureEdit={handleFeatureEdit}
            onFeatureDelete={handleFeatureDelete}
          />
        </MapView>
      </main>
    </div>
  )
}

export default App
