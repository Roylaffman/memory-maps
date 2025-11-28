import { useState } from 'react';
import './MapGallery.css';

/**
 * MapGallery Component
 * Displays a list of maps with search, filtering, and management capabilities
 * 
 * @param {Object} props
 * @param {Array} props.maps - Array of map objects
 * @param {Function} props.onMapSelect - Callback when a map is selected
 * @param {Function} props.onMapCreate - Callback to create new map
 * @param {Function} props.onMapDelete - Callback to delete a map
 * @param {Function} props.onMapShare - Callback to share a map
 */
function MapGallery({ maps = [], onMapSelect, onMapCreate, onMapDelete, onMapShare }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterVisibility, setFilterVisibility] = useState('all'); // all, public, private

  // Filter maps based on search and visibility
  const filteredMaps = maps.filter(map => {
    const matchesSearch = map.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         (map.description || '').toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesVisibility = filterVisibility === 'all' ||
                             (filterVisibility === 'public' && map.is_public) ||
                             (filterVisibility === 'private' && !map.is_public);
    
    return matchesSearch && matchesVisibility;
  });

  const handleMapClick = (map) => {
    if (onMapSelect) {
      onMapSelect(map);
    }
  };

  const handleDeleteClick = (e, map) => {
    e.stopPropagation();
    if (confirm(`Delete map "${map.title}"? This will also delete all features, stories, and photos.`)) {
      onMapDelete(map);
    }
  };

  const handleShareClick = (e, map) => {
    e.stopPropagation();
    if (onMapShare) {
      onMapShare(map);
    }
  };

  return (
    <div className="map-gallery">
      <div className="gallery-header">
        <h1>My Maps</h1>
        <button className="btn btn-primary" onClick={onMapCreate}>
          + Create New Map
        </button>
      </div>

      <div className="gallery-controls">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search maps..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <span className="search-icon">🔍</span>
        </div>

        <div className="filter-buttons">
          <button
            className={`filter-btn ${filterVisibility === 'all' ? 'active' : ''}`}
            onClick={() => setFilterVisibility('all')}
          >
            All ({maps.length})
          </button>
          <button
            className={`filter-btn ${filterVisibility === 'public' ? 'active' : ''}`}
            onClick={() => setFilterVisibility('public')}
          >
            Public ({maps.filter(m => m.is_public).length})
          </button>
          <button
            className={`filter-btn ${filterVisibility === 'private' ? 'active' : ''}`}
            onClick={() => setFilterVisibility('private')}
          >
            Private ({maps.filter(m => !m.is_public).length})
          </button>
        </div>
      </div>

      {filteredMaps.length === 0 ? (
        <div className="empty-state">
          {searchQuery ? (
            <>
              <p>No maps found matching "{searchQuery}"</p>
              <button className="btn btn-secondary" onClick={() => setSearchQuery('')}>
                Clear Search
              </button>
            </>
          ) : (
            <>
              <p>You haven't created any maps yet</p>
              <button className="btn btn-primary" onClick={onMapCreate}>
                Create Your First Map
              </button>
            </>
          )}
        </div>
      ) : (
        <div className="maps-grid">
          {filteredMaps.map(map => (
            <div
              key={map.id}
              className="map-card"
              onClick={() => handleMapClick(map)}
            >
              <div className="map-card-header">
                <h3>{map.title}</h3>
                <span className={`visibility-badge ${map.is_public ? 'public' : 'private'}`}>
                  {map.is_public ? '🌐 Public' : '🔒 Private'}
                </span>
              </div>

              {map.description && (
                <p className="map-description">{map.description}</p>
              )}

              <div className="map-stats">
                <span className="stat">
                  📍 {map.feature_count || 0} features
                </span>
                <span className="stat">
                  📅 {new Date(map.created_at).toLocaleDateString()}
                </span>
              </div>

              <div className="map-card-actions">
                <button
                  className="action-btn share-btn"
                  onClick={(e) => handleShareClick(e, map)}
                  title="Share map"
                >
                  🔗 Share
                </button>
                <button
                  className="action-btn delete-btn"
                  onClick={(e) => handleDeleteClick(e, map)}
                  title="Delete map"
                >
                  🗑️ Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default MapGallery;
