import { Popup } from 'react-leaflet';
import './FeaturePopup.css';

/**
 * FeaturePopup Component
 * Displays feature information in a popup when clicked
 * 
 * @param {Object} props
 * @param {Object} props.feature - Feature data
 * @param {string} props.feature.title - Feature title
 * @param {string} props.feature.description - Feature description
 * @param {string} props.feature.category - Feature category
 * @param {Array} props.feature.stories - Associated stories
 * @param {Array} props.feature.photos - Associated photos
 * @param {Function} props.onEdit - Callback when edit button is clicked
 * @param {Function} props.onDelete - Callback when delete button is clicked
 */
function FeaturePopup({ feature, onEdit, onDelete }) {
  const { title, description, category, stories = [], photos = [] } = feature;

  return (
    <Popup className="feature-popup" maxWidth={300}>
      <div className="popup-content">
        <div className="popup-header">
          <h3>{title || 'Untitled Feature'}</h3>
          {category && <span className="category-badge">{category}</span>}
        </div>
        
        {description && (
          <div className="popup-description">
            <p>{description}</p>
          </div>
        )}

        {photos.length > 0 && (
          <div className="popup-photos">
            {photos.slice(0, 3).map((photo, idx) => (
              <img 
                key={idx} 
                src={photo.url || photo.image} 
                alt={photo.caption || `Photo ${idx + 1}`}
                className="popup-photo"
              />
            ))}
            {photos.length > 3 && (
              <span className="more-photos">+{photos.length - 3} more</span>
            )}
          </div>
        )}

        {stories.length > 0 && (
          <div className="popup-stories">
            <h4>Stories ({stories.length})</h4>
            {stories.slice(0, 2).map((story, idx) => (
              <div key={idx} className="story-preview">
                <strong>{story.title}</strong>
                <p>{story.content?.substring(0, 100)}...</p>
              </div>
            ))}
            {stories.length > 2 && (
              <span className="more-stories">+{stories.length - 2} more stories</span>
            )}
          </div>
        )}

        <div className="popup-actions">
          {onEdit && (
            <button 
              className="btn btn-edit" 
              onClick={() => onEdit(feature)}
            >
              Edit
            </button>
          )}
          {onDelete && (
            <button 
              className="btn btn-delete" 
              onClick={() => onDelete(feature)}
            >
              Delete
            </button>
          )}
        </div>
      </div>
    </Popup>
  );
}

export default FeaturePopup;
