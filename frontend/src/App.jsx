import { useState } from 'react'
import MapView from './components/MapView'
import DrawingControls from './components/DrawingControls'
import MapFeatures from './components/MapFeatures'
import FeatureEditor from './components/FeatureEditor'
import MapGallery from './components/MapGallery'
import MapCreator from './components/MapCreator'
import ShareModal from './components/ShareModal'
import './App.css'

function App() {
  // View state: 'gallery' or 'map'
  const [currentView, setCurrentView] = useState('gallery');
  
  // Maps state
  const [maps, setMaps] = useState([]);
  const [currentMap, setCurrentMap] = useState(null);
  const [isCreatorOpen, setIsCreatorOpen] = useState(false);
  const [shareMap, setShareMap] = useState(null);
  
  // Features state (for current map)
  const [features, setFeatures] = useState([]);
  const [editingFeature, setEditingFeature] = useState(null);
  const [isEditorOpen, setIsEditorOpen] = useState(false);

  // Map management handlers
  const handleMapCreate = (mapData) => {
    const newMap = {
      ...mapData,
      id: Date.now(),
      feature_count: 0
    };
    setMaps(prev => [...prev, newMap]);
    setIsCreatorOpen(false);
    
    // Open the new map
    setCurrentMap(newMap);
    setFeatures([]);
    setCurrentView('map');
  };

  const handleMapSelect = (map) => {
    setCurrentMap(map);
    // In a real app, we'd load features from backend
    setFeatures([]);
    setCurrentView('map');
  };

  const handleMapDelete = (map) => {
    setMaps(prev => prev.filter(m => m.id !== map.id));
    if (currentMap?.id === map.id) {
      setCurrentMap(null);
      setFeatures([]);
      setCurrentView('gallery');
    }
  };

  const handleMapShare = (map) => {
    setShareMap(map);
  };

  const handleVisibilityChange = (map, isPublic) => {
    setMaps(prev => prev.map(m => 
      m.id === map.id ? { ...m, is_public: isPublic } : m
    ));
    if (shareMap?.id === map.id) {
      setShareMap({ ...shareMap, is_public: isPublic });
    }
  };

  const handleBackToGallery = () => {
    // Update feature count for current map
    if (currentMap) {
      setMaps(prev => prev.map(m => 
        m.id === currentMap.id ? { ...m, feature_count: features.length } : m
      ));
    }
    setCurrentView('gallery');
    setCurrentMap(null);
  };

  // Feature management handlers
  const handleFeatureCreated = ({ layer, type, geometry }) => {
    const newFeature = {
      id: Date.now(),
      feature_type: type === 'marker' ? 'point' : 'polygon',
      geometry,
      title: `New ${type === 'marker' ? 'Point' : 'Polygon'}`,
      description: 'Click edit to add details',
      category: '',
      stories: [],
      photos: []
    };
    
    setFeatures(prev => [...prev, newFeature]);
    
    // Automatically open editor for new features
    setEditingFeature(newFeature);
    setIsEditorOpen(true);
  };

  const handleFeatureEdit = (feature) => {
    setEditingFeature(feature);
    setIsEditorOpen(true);
  };

  const handleFeatureSave = (updatedFeature) => {
    setFeatures(prev => prev.map(f => 
      f.id === updatedFeature.id ? updatedFeature : f
    ));
    setIsEditorOpen(false);
    setEditingFeature(null);
  };

  const handleEditorCancel = () => {
    setIsEditorOpen(false);
    setEditingFeature(null);
  };

  const handleFeatureDelete = (feature) => {
    if (confirm(`Delete "${feature.title}"?`)) {
      setFeatures(prev => prev.filter(f => f.id !== feature.id));
    }
  };

  const handleFeaturesEdited = (editedFeatures) => {
    // Update geometries of edited features
    console.log('Features edited:', editedFeatures);
  };

  const handleFeaturesDeleted = (deletedLayers) => {
    // Match layers to features and remove them
    console.log('Features deleted:', deletedLayers);
  };

  // Render gallery view
  if (currentView === 'gallery') {
    return (
      <div className="app-container">
        <MapGallery
          maps={maps}
          onMapSelect={handleMapSelect}
          onMapCreate={() => setIsCreatorOpen(true)}
          onMapDelete={handleMapDelete}
          onMapShare={handleMapShare}
        />
        
        <MapCreator
          isOpen={isCreatorOpen}
          onSave={handleMapCreate}
          onCancel={() => setIsCreatorOpen(false)}
        />
        
        <ShareModal
          map={shareMap}
          isOpen={!!shareMap}
          onClose={() => setShareMap(null)}
          onVisibilityChange={handleVisibilityChange}
        />
      </div>
    );
  }

  // Render map view
  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-left">
          <button className="back-btn" onClick={handleBackToGallery}>
            ← Back to Gallery
          </button>
          <h1>{currentMap?.title || 'Untitled Map'}</h1>
        </div>
        <div className="header-info">
          <span className="feature-count">{features.length} features</span>
        </div>
      </header>
      <main className="map-container">
        <MapView 
          center={[currentMap?.center_lat || 37.7749, currentMap?.center_lng || -122.4194]} 
          zoom={currentMap?.zoom_level || 10}
        >
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
      
      <FeatureEditor
        feature={editingFeature}
        isOpen={isEditorOpen}
        onSave={handleFeatureSave}
        onCancel={handleEditorCancel}
      />
    </div>
  );
}

export default App
