import { useState } from 'react';
import './MapCreator.css';

/**
 * MapCreator Component
 * Modal form for creating a new map
 * 
 * @param {Object} props
 * @param {boolean} props.isOpen - Whether the modal is open
 * @param {Function} props.onSave - Callback when save is clicked
 * @param {Function} props.onCancel - Callback when cancel is clicked
 */
function MapCreator({ isOpen, onSave, onCancel }) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    is_public: false,
    center_lat: 37.7749,
    center_lng: -122.4194,
    zoom_level: 10
  });

  if (!isOpen) return null;

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.title.trim()) {
      onSave({
        ...formData,
        center_lat: parseFloat(formData.center_lat),
        center_lng: parseFloat(formData.center_lng),
        zoom_level: parseInt(formData.zoom_level),
        created_at: new Date().toISOString(),
        feature_count: 0
      });
      // Reset form
      setFormData({
        title: '',
        description: '',
        is_public: false,
        center_lat: 37.7749,
        center_lng: -122.4194,
        zoom_level: 10
      });
    }
  };

  return (
    <div className="map-creator-overlay" onClick={onCancel}>
      <div className="map-creator-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Create New Map</h2>
          <button className="close-btn" onClick={onCancel}>&times;</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <div className="form-group">
              <label htmlFor="title">Map Title *</label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                placeholder="Enter map title"
                required
                autoFocus
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                placeholder="Describe your map (optional)"
                rows="3"
              />
            </div>

            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="is_public"
                  checked={formData.is_public}
                  onChange={handleInputChange}
                />
                <span>Make this map public</span>
              </label>
              <p className="help-text">
                {formData.is_public 
                  ? '🌐 Anyone with the link can view this map' 
                  : '🔒 Only you can view this map'}
              </p>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="center_lat">Center Latitude</label>
                <input
                  type="number"
                  id="center_lat"
                  name="center_lat"
                  value={formData.center_lat}
                  onChange={handleInputChange}
                  step="0.0001"
                  min="-90"
                  max="90"
                />
              </div>

              <div className="form-group">
                <label htmlFor="center_lng">Center Longitude</label>
                <input
                  type="number"
                  id="center_lng"
                  name="center_lng"
                  value={formData.center_lng}
                  onChange={handleInputChange}
                  step="0.0001"
                  min="-180"
                  max="180"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="zoom_level">Initial Zoom Level</label>
              <input
                type="range"
                id="zoom_level"
                name="zoom_level"
                value={formData.zoom_level}
                onChange={handleInputChange}
                min="3"
                max="18"
              />
              <span className="zoom-value">{formData.zoom_level}</span>
            </div>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              Create Map
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default MapCreator;
