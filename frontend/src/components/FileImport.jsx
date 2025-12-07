import { useState } from 'react';
import { importAPI } from '../services/api';
import './FileImport.css';

/**
 * FileImport Component
 * Handles importing GeoJSON, KML, and CSV files via backend API
 * 
 * @param {Object} props
 * @param {boolean} props.isOpen - Whether the modal is open
 * @param {number} props.mapId - Current map ID for import
 * @param {Function} props.onImport - Callback with import results
 * @param {Function} props.onCancel - Callback when cancelled
 */
function FileImport({ isOpen, mapId, onImport, onCancel }) {
  const [file, setFile] = useState(null);
  const [importing, setImporting] = useState(false);
  const [error, setError] = useState(null);
  const [preview, setPreview] = useState(null);
  const [importResult, setImportResult] = useState(null);

  if (!isOpen) return null;

  const handleFileSelect = async (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setError(null);
    setPreview(null);
    setImportResult(null);

    // Validate file type
    const fileName = selectedFile.name.toLowerCase();
    const isGeoJSON = fileName.endsWith('.geojson') || fileName.endsWith('.json');
    const isKML = fileName.endsWith('.kml');
    const isKMZ = fileName.endsWith('.kmz');
    const isCSV = fileName.endsWith('.csv');

    if (!isGeoJSON && !isKML && !isKMZ && !isCSV) {
      setError('Please select a GeoJSON (.geojson, .json), KML (.kml), KMZ (.kmz), or CSV (.csv) file');
      setFile(null);
      return;
    }

    // Preview file info
    setPreview({
      name: selectedFile.name,
      size: (selectedFile.size / 1024).toFixed(2) + ' KB',
      type: isGeoJSON ? 'GeoJSON' : isKML ? 'KML' : isKMZ ? 'KMZ' : 'CSV'
    });
  };

  const handleImport = async () => {
    if (!file || !mapId) return;

    setImporting(true);
    setError(null);
    setImportResult(null);

    try {
      const fileName = file.name.toLowerCase();
      let result;

      if (fileName.endsWith('.geojson') || fileName.endsWith('.json')) {
        // Import GeoJSON via backend
        result = await importAPI.importGeoJSON(mapId, file);
      } else if (fileName.endsWith('.kml') || fileName.endsWith('.kmz')) {
        // Import KML/KMZ via backend
        result = await importAPI.importKML(mapId, file);
      } else if (fileName.endsWith('.csv')) {
        // Import CSV coordinates via backend
        result = await importAPI.importCoordinates(mapId, file, {
          lat_col: 'lat',
          lng_col: 'lng',
          name_col: 'name'
        });
      }

      if (result.success) {
        setImportResult({
          success: true,
          imported: result.imported,
          warnings: result.warnings || [],
          features: result.features || []
        });
        
        // Notify parent component
        onImport(result);
      } else {
        setError(result.errors?.join(', ') || 'Import failed');
      }
    } catch (err) {
      console.error('Import error:', err);
      setError(`Error importing file: ${err.message}`);
    } finally {
      setImporting(false);
    }
  };

  const handleClose = () => {
    setFile(null);
    setPreview(null);
    setError(null);
    onCancel();
  };

  return (
    <div className="file-import-overlay" onClick={handleClose}>
      <div className="file-import-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Import GIS Data</h2>
          <button className="close-btn" onClick={handleClose}>&times;</button>
        </div>

        <div className="modal-body">
          {!importResult ? (
            <>
              <div className="import-info">
                <p>Import features from GIS files or coordinate data</p>
                <ul>
                  <li>✓ GeoJSON (.geojson, .json)</li>
                  <li>✓ KML/KMZ (.kml, .kmz)</li>
                  <li>✓ CSV Coordinates (.csv)</li>
                </ul>
              </div>

              <div className="file-upload-area">
                <input
                  type="file"
                  id="file-input"
                  accept=".geojson,.json,.kml,.kmz,.csv"
                  onChange={handleFileSelect}
                  style={{ display: 'none' }}
                />
                <label htmlFor="file-input" className="upload-label">
                  {file ? '📄 Change File' : '📁 Select File'}
                </label>
              </div>

              {preview && (
                <div className="file-preview">
                  <h4>File Preview</h4>
                  <div className="preview-details">
                    <div className="preview-row">
                      <span className="label">Name:</span>
                      <span className="value">{preview.name}</span>
                    </div>
                    <div className="preview-row">
                      <span className="label">Type:</span>
                      <span className="value">{preview.type}</span>
                    </div>
                    <div className="preview-row">
                      <span className="label">Size:</span>
                      <span className="value">{preview.size}</span>
                    </div>
                  </div>
                </div>
              )}

              {error && (
                <div className="error-message">
                  ⚠️ {error}
                </div>
              )}
            </>
          ) : (
            <div className="import-result">
              <div className="result-success">
                <h3>✓ Import Successful!</h3>
                <p>Imported {importResult.imported} feature{importResult.imported !== 1 ? 's' : ''}</p>
              </div>
              
              {importResult.warnings && importResult.warnings.length > 0 && (
                <div className="result-warnings">
                  <h4>⚠ Warnings:</h4>
                  <ul>
                    {importResult.warnings.map((warning, idx) => (
                      <li key={idx}>{warning}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {importResult.features && importResult.features.length > 0 && (
                <div className="result-features">
                  <h4>Imported Features:</h4>
                  <ul>
                    {importResult.features.slice(0, 10).map((feature, idx) => (
                      <li key={idx}>
                        {feature.title || `Feature ${feature.id}`}
                      </li>
                    ))}
                    {importResult.features.length > 10 && (
                      <li>... and {importResult.features.length - 10} more</li>
                    )}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="modal-footer">
          {!importResult ? (
            <>
              <button className="btn btn-secondary" onClick={handleClose}>
                Cancel
              </button>
              <button 
                className="btn btn-primary" 
                onClick={handleImport}
                disabled={!file || importing}
              >
                {importing ? 'Importing...' : 'Import Features'}
              </button>
            </>
          ) : (
            <button className="btn btn-primary" onClick={handleClose}>
              Done
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default FileImport;
