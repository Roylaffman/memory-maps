import { useState, useEffect } from 'react'
import MapView from './components/MapView'
import DrawingControls from './components/DrawingControls'
import MapFeatures from './components/MapFeatures'
import FeatureEditor from './components/FeatureEditor'
import MapGallery from './components/MapGallery'
import MapCreator from './components/MapCreator'
import ShareModal from './components/ShareModal'
import FileImport from './components/FileImport'
import AuthModal from './components/AuthModal'
import { mapAPI, featureAPI, storyAPI, photoAPI, authAPI } from './services/api'
import './App.css'

function App() {
  // View state: 'gallery' or 'map'
  const [currentView, setCurrentView] = useState('gallery');
  
  // Maps state
  const [maps, setMaps] = useState([]);
  const [currentMap, setCurrentMap] = useState(null);
  const [isCreatorOpen, setIsCreatorOpen] = useState(false);
  const [shareMap, setShareMap] = useState(null);
  const [loadingMaps, setLoadingMaps] = useState(false);
  
  // Features state (for current map)
  const [features, setFeatures] = useState([]);
  const [editingFeature, setEditingFeature] = useState(null);
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [isImportOpen, setIsImportOpen] = useState(false);
  const [loadingFeatures, setLoadingFeatures] = useState(false);
  
  // Error state
  const [error, setError] = useState(null);
  
  // Auth state
  const [isAuthenticated, setIsAuthenticated] = useState(authAPI.isAuthenticated());
  const [currentUser, setCurrentUser] = useState(null);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  // Load maps on mount
  useEffect(() => {
    loadMaps();
    if (isAuthenticated) {
      loadCurrentUser();
    }
  }, []);

  const loadCurrentUser = async () => {
    try {
      const user = await authAPI.getCurrentUser();
      setCurrentUser(user);
    } catch (err) {
      console.error('Error loading user:', err);
      // Token might be invalid
      setIsAuthenticated(false);
    }
  };

  const handleAuthSuccess = (data) => {
    setIsAuthenticated(true);
    setCurrentUser(data.user);
    loadMaps(); // Reload maps with auth
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setIsAuthenticated(false);
      setCurrentUser(null);
      loadMaps(); // Reload to show only public maps
    }
  };

  // Load features when map changes
  useEffect(() => {
    if (currentMap && currentView === 'map') {
      loadFeatures(currentMap.id);
    }
  }, [currentMap, currentView]);

  // API Functions
  const loadMaps = async () => {
    setLoadingMaps(true);
    setError(null);
    try {
      const data = await mapAPI.getAll();
      setMaps(data.results || data);
    } catch (err) {
      console.error('Error loading maps:', err);
      setError('Failed to load maps. Using offline mode.');
      // Keep existing maps in offline mode
    } finally {
      setLoadingMaps(false);
    }
  };

  const loadFeatures = async (mapId) => {
    setLoadingFeatures(true);
    setError(null);
    try {
      const data = await mapAPI.getFeatures(mapId);
      setFeatures(data.results || data);
    } catch (err) {
      console.error('Error loading features:', err);
      setError('Failed to load features. Using offline mode.');
      // Keep existing features in offline mode
    } finally {
      setLoadingFeatures(false);
    }
  };

  // Map management handlers
  const handleMapCreate = async (mapData) => {
    try {
      const newMap = await mapAPI.create(mapData);
      setMaps(prev => [newMap, ...prev]);
      setIsCreatorOpen(false);
      
      // Open the new map
      setCurrentMap(newMap);
      setFeatures([]);
      setCurrentView('map');
    } catch (err) {
      console.error('Error creating map:', err);
      alert('Failed to create map: ' + err.message);
    }
  };

  const handleMapSelect = (map) => {
    setCurrentMap(map);
    setFeatures([]);
    setCurrentView('map');
    // Features will be loaded by useEffect
  };

  const handleMapDelete = async (map) => {
    try {
      await mapAPI.delete(map.id);
      setMaps(prev => prev.filter(m => m.id !== map.id));
      if (currentMap?.id === map.id) {
        setCurrentMap(null);
        setFeatures([]);
        setCurrentView('gallery');
      }
    } catch (err) {
      console.error('Error deleting map:', err);
      alert('Failed to delete map: ' + err.message);
    }
  };

  const handleMapShare = (map) => {
    setShareMap(map);
  };

  const handleVisibilityChange = async (map, isPublic) => {
    try {
      const updatedMap = await mapAPI.update(map.id, { is_public: isPublic });
      setMaps(prev => prev.map(m => 
        m.id === map.id ? updatedMap : m
      ));
      if (shareMap?.id === map.id) {
        setShareMap(updatedMap);
      }
    } catch (err) {
      console.error('Error updating map visibility:', err);
      alert('Failed to update visibility: ' + err.message);
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
  const handleFeatureCreated = async ({ layer, type, geometry }) => {
    let featureType, featureTitle;
    
    if (type === 'marker') {
      featureType = 'point';
      featureTitle = 'New Point';
    } else if (type === 'polyline') {
      featureType = 'line';
      featureTitle = 'New Line';
    } else {
      featureType = 'polygon';
      featureTitle = 'New Polygon';
    }
    
    const featureData = {
      map: currentMap.id,
      feature_type: featureType,
      geometry,
      title: featureTitle,
      description: 'Click edit to add details',
      category: '',
    };
    
    try {
      const newFeature = await featureAPI.create(featureData);
      setFeatures(prev => [...prev, newFeature]);
      
      // Automatically open editor for new features
      setEditingFeature(newFeature);
      setIsEditorOpen(true);
    } catch (err) {
      console.error('Error creating feature:', err);
      alert('Failed to create feature: ' + err.message);
    }
  };

  const handleFeatureEdit = (feature) => {
    setEditingFeature(feature);
    setIsEditorOpen(true);
  };

  const handleFeatureSave = async (updatedFeature) => {
    try {
      // Update feature basic info
      const featureUpdate = {
        title: updatedFeature.title,
        description: updatedFeature.description,
        category: updatedFeature.category,
      };
      
      const savedFeature = await featureAPI.update(updatedFeature.id, featureUpdate);
      
      // Handle stories (create new ones)
      if (updatedFeature.stories && updatedFeature.stories.length > 0) {
        for (const story of updatedFeature.stories) {
          if (!story.id) {
            // New story
            await storyAPI.create({
              feature: updatedFeature.id,
              title: story.title,
              content: story.content,
            });
          }
        }
      }
      
      // Handle photos (upload new ones)
      if (updatedFeature.photos && updatedFeature.photos.length > 0) {
        for (const photo of updatedFeature.photos) {
          if (photo.file && !photo.id) {
            // New photo
            await photoAPI.upload(updatedFeature.id, photo.file, photo.caption);
          }
        }
      }
      
      // Reload features to get updated data
      await loadFeatures(currentMap.id);
      
      setIsEditorOpen(false);
      setEditingFeature(null);
    } catch (err) {
      console.error('Error saving feature:', err);
      alert('Failed to save feature: ' + err.message);
    }
  };

  const handleEditorCancel = () => {
    setIsEditorOpen(false);
    setEditingFeature(null);
  };

  const handleFeatureDelete = async (feature) => {
    if (confirm(`Delete "${feature.title}"?`)) {
      try {
        await featureAPI.delete(feature.id);
        setFeatures(prev => prev.filter(f => f.id !== feature.id));
      } catch (err) {
        console.error('Error deleting feature:', err);
        alert('Failed to delete feature: ' + err.message);
      }
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

  const handleFileImport = async (importResult) => {
    // Reload features from backend after import
    if (currentMap && importResult.success) {
      await loadFeatures(currentMap.id);
      setIsImportOpen(false);
      console.log(`Imported ${importResult.imported} features`);
    }
  };

  // Render gallery view
  if (currentView === 'gallery') {
    return (
      <div className="app-container">
        <header className="app-header gallery-header">
          <h1>Personal Memory Maps</h1>
          <div className="header-actions">
            {isAuthenticated ? (
              <div className="user-menu">
                <span className="user-name">👤 {currentUser?.username || 'User'}</span>
                <button className="logout-btn" onClick={handleLogout}>
                  Logout
                </button>
              </div>
            ) : (
              <button className="login-btn" onClick={() => setIsAuthModalOpen(true)}>
                Sign In
              </button>
            )}
          </div>
        </header>
        
        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}
        
        {loadingMaps ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Loading maps...</p>
          </div>
        ) : (
          <MapGallery
            maps={maps}
            onMapSelect={handleMapSelect}
            onMapCreate={() => setIsCreatorOpen(true)}
            onMapDelete={handleMapDelete}
            onMapShare={handleMapShare}
          />
        )}
        
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
        
        <AuthModal
          isOpen={isAuthModalOpen}
          onClose={() => setIsAuthModalOpen(false)}
          onSuccess={handleAuthSuccess}
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
          <button className="import-btn" onClick={() => setIsImportOpen(true)}>
            📁 Import
          </button>
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
      
      <FileImport
        isOpen={isImportOpen}
        mapId={currentMap?.id}
        onImport={handleFileImport}
        onCancel={() => setIsImportOpen(false)}
      />
      
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onSuccess={handleAuthSuccess}
      />
    </div>
  );
}

export default App
