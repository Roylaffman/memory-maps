import { useState, useEffect } from 'react';
import './FeatureEditor.css';

/**
 * FeatureEditor Component
 * Modal form for editing feature details, adding stories, and uploading photos
 * 
 * @param {Object} props
 * @param {Object} props.feature - Feature to edit
 * @param {Function} props.onSave - Callback when save is clicked
 * @param {Function} props.onCancel - Callback when cancel is clicked
 * @param {boolean} props.isOpen - Whether the modal is open
 */
function FeatureEditor({ feature, onSave, onCancel, isOpen }) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
  });

  const [stories, setStories] = useState([]);
  const [photos, setPhotos] = useState([]);
  const [newStory, setNewStory] = useState({ title: '', content: '' });
  const [showStoryForm, setShowStoryForm] = useState(false);

  // Initialize form data when feature changes
  useEffect(() => {
    if (feature) {
      setFormData({
        title: feature.title || '',
        description: feature.description || '',
        category: feature.category || '',
      });
      setStories(feature.stories || []);
      setPhotos(feature.photos || []);
    }
  }, [feature]);

  if (!isOpen || !feature) return null;

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handlePhotoUpload = (e) => {
    const files = Array.from(e.target.files);
    const newPhotos = files.map(file => ({
      file,
      url: URL.createObjectURL(file),
      caption: '',
      uploaded_at: new Date().toISOString()
    }));
    setPhotos(prev => [...prev, ...newPhotos]);
  };

  const handlePhotoRemove = (index) => {
    setPhotos(prev => prev.filter((_, i) => i !== index));
  };

  const handlePhotoCaptionChange = (index, caption) => {
    setPhotos(prev => prev.map((photo, i) => 
      i === index ? { ...photo, caption } : photo
    ));
  };

  const handleAddStory = () => {
    if (newStory.title.trim() && newStory.content.trim()) {
      setStories(prev => [...prev, {
        ...newStory,
        created_at: new Date().toISOString()
      }]);
      setNewStory({ title: '', content: '' });
      setShowStoryForm(false);
    }
  };

  const handleRemoveStory = (index) => {
    setStories(prev => prev.filter((_, i) => i !== index));
  };

  const handleSave = () => {
    const updatedFeature = {
      ...feature,
      ...formData,
      stories,
      photos
    };
    onSave(updatedFeature);
  };

  return (
    <div className="feature-editor-overlay" onClick={onCancel}>
      <div className="feature-editor-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Edit Feature</h2>
          <button className="close-btn" onClick={onCancel}>&times;</button>
        </div>

        <div className="modal-body">
          {/* Basic Information */}
          <section className="form-section">
            <h3>Basic Information</h3>
            <div className="form-group">
              <label htmlFor="title">Title *</label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                placeholder="Enter feature title"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                placeholder="Enter feature description"
                rows="4"
              />
            </div>

            <div className="form-group">
              <label htmlFor="category">Category</label>
              <input
                type="text"
                id="category"
                name="category"
                value={formData.category}
                onChange={handleInputChange}
                placeholder="e.g., Garden, Building, Trail"
              />
            </div>
          </section>

          {/* Photos Section */}
          <section className="form-section">
            <h3>Photos ({photos.length})</h3>
            <div className="photo-upload-area">
              <input
                type="file"
                id="photo-upload"
                accept="image/*"
                multiple
                onChange={handlePhotoUpload}
                style={{ display: 'none' }}
              />
              <label htmlFor="photo-upload" className="upload-btn">
                📷 Add Photos
              </label>
            </div>

            {photos.length > 0 && (
              <div className="photo-grid">
                {photos.map((photo, index) => (
                  <div key={index} className="photo-item">
                    <img src={photo.url || photo.image} alt={photo.caption || `Photo ${index + 1}`} />
                    <input
                      type="text"
                      placeholder="Add caption..."
                      value={photo.caption}
                      onChange={(e) => handlePhotoCaptionChange(index, e.target.value)}
                      className="photo-caption-input"
                    />
                    <button
                      className="remove-photo-btn"
                      onClick={() => handlePhotoRemove(index)}
                      title="Remove photo"
                    >
                      &times;
                    </button>
                  </div>
                ))}
              </div>
            )}
          </section>

          {/* Stories Section */}
          <section className="form-section">
            <div className="section-header">
              <h3>Stories ({stories.length})</h3>
              {!showStoryForm && (
                <button
                  className="add-story-btn"
                  onClick={() => setShowStoryForm(true)}
                >
                  + Add Story
                </button>
              )}
            </div>

            {showStoryForm && (
              <div className="story-form">
                <div className="form-group">
                  <input
                    type="text"
                    placeholder="Story title"
                    value={newStory.title}
                    onChange={(e) => setNewStory(prev => ({ ...prev, title: e.target.value }))}
                  />
                </div>
                <div className="form-group">
                  <textarea
                    placeholder="Write your story..."
                    value={newStory.content}
                    onChange={(e) => setNewStory(prev => ({ ...prev, content: e.target.value }))}
                    rows="4"
                  />
                </div>
                <div className="story-form-actions">
                  <button className="btn btn-primary" onClick={handleAddStory}>
                    Save Story
                  </button>
                  <button
                    className="btn btn-secondary"
                    onClick={() => {
                      setShowStoryForm(false);
                      setNewStory({ title: '', content: '' });
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {stories.length > 0 && (
              <div className="stories-list">
                {stories.map((story, index) => (
                  <div key={index} className="story-item">
                    <div className="story-header">
                      <strong>{story.title}</strong>
                      <button
                        className="remove-story-btn"
                        onClick={() => handleRemoveStory(index)}
                        title="Remove story"
                      >
                        &times;
                      </button>
                    </div>
                    <p>{story.content}</p>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>

        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onCancel}>
            Cancel
          </button>
          <button className="btn btn-primary" onClick={handleSave}>
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
}

export default FeatureEditor;
