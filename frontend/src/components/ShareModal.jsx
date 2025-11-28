import { useState } from 'react';
import './ShareModal.css';

/**
 * ShareModal Component
 * Modal for sharing maps with visibility controls
 * 
 * @param {Object} props
 * @param {Object} props.map - Map to share
 * @param {boolean} props.isOpen - Whether the modal is open
 * @param {Function} props.onClose - Callback when modal is closed
 * @param {Function} props.onVisibilityChange - Callback when visibility is changed
 */
function ShareModal({ map, isOpen, onClose, onVisibilityChange }) {
  const [copied, setCopied] = useState(false);

  if (!isOpen || !map) return null;

  const shareUrl = `${window.location.origin}/maps/${map.id}`;

  const handleCopyLink = () => {
    navigator.clipboard.writeText(shareUrl).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const handleVisibilityToggle = () => {
    if (onVisibilityChange) {
      onVisibilityChange(map, !map.is_public);
    }
  };

  return (
    <div className="share-modal-overlay" onClick={onClose}>
      <div className="share-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Share Map</h2>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>

        <div className="modal-body">
          <div className="map-info">
            <h3>{map.title}</h3>
            {map.description && <p>{map.description}</p>}
          </div>

          <div className="visibility-section">
            <h4>Visibility</h4>
            <div className="visibility-toggle">
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={map.is_public}
                  onChange={handleVisibilityToggle}
                />
                <span className="toggle-slider"></span>
                <span className="toggle-text">
                  {map.is_public ? '🌐 Public' : '🔒 Private'}
                </span>
              </label>
            </div>
            <p className="visibility-description">
              {map.is_public 
                ? 'Anyone with the link can view this map'
                : 'Only you can view this map. Make it public to share with others.'}
            </p>
          </div>

          {map.is_public && (
            <div className="share-link-section">
              <h4>Share Link</h4>
              <div className="link-container">
                <input
                  type="text"
                  value={shareUrl}
                  readOnly
                  className="share-link-input"
                />
                <button
                  className="copy-btn"
                  onClick={handleCopyLink}
                >
                  {copied ? '✓ Copied!' : '📋 Copy'}
                </button>
              </div>
            </div>
          )}

          {!map.is_public && (
            <div className="private-notice">
              <p>💡 Make this map public to generate a shareable link</p>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button className="btn btn-primary" onClick={onClose}>
            Done
          </button>
        </div>
      </div>
    </div>
  );
}

export default ShareModal;
