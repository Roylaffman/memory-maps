import { useState } from 'react';
import { authAPI } from '../services/api';
import './AuthModal.css';

/**
 * AuthModal Component
 * Handles user login and registration
 * 
 * @param {Object} props
 * @param {boolean} props.isOpen - Whether the modal is open
 * @param {Function} props.onClose - Callback when modal is closed
 * @param {Function} props.onSuccess - Callback when auth succeeds
 */
function AuthModal({ isOpen, onClose, onSuccess }) {
  const [mode, setMode] = useState('login'); // 'login' or 'register'
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!isOpen) return null;

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (mode === 'register') {
        // Validate passwords match
        if (formData.password !== formData.confirmPassword) {
          setError('Passwords do not match');
          setLoading(false);
          return;
        }

        // Register (placeholder - needs backend endpoint)
        alert('Registration endpoint not yet implemented. Please use Django admin to create users.');
        setLoading(false);
        return;
      } else {
        // Login
        const data = await authAPI.login(formData.username, formData.password);
        
        if (onSuccess) {
          onSuccess(data);
        }
        
        onClose();
      }
    } catch (err) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    });
    setError(null);
    onClose();
  };

  const switchMode = () => {
    setMode(mode === 'login' ? 'register' : 'login');
    setError(null);
  };

  return (
    <div className="auth-modal-overlay" onClick={handleClose}>
      <div className="auth-modal" onClick={(e) => e.stopPropagation()}>
        <div className="auth-header">
          <h2>{mode === 'login' ? 'Welcome Back' : 'Create Account'}</h2>
          <button className="close-btn" onClick={handleClose}>&times;</button>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {error && (
            <div className="auth-error">
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              placeholder="Enter your username"
              required
              autoFocus
            />
          </div>

          {mode === 'register' && (
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="Enter your email"
                required
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Enter your password"
              required
            />
          </div>

          {mode === 'register' && (
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                placeholder="Confirm your password"
                required
              />
            </div>
          )}

          <button 
            type="submit" 
            className="auth-submit-btn"
            disabled={loading}
          >
            {loading ? 'Please wait...' : mode === 'login' ? 'Sign In' : 'Sign Up'}
          </button>

          <div className="auth-switch">
            {mode === 'login' ? (
              <p>
                Don't have an account?{' '}
                <button type="button" onClick={switchMode} className="switch-btn">
                  Sign up
                </button>
              </p>
            ) : (
              <p>
                Already have an account?{' '}
                <button type="button" onClick={switchMode} className="switch-btn">
                  Sign in
                </button>
              </p>
            )}
          </div>

          <div className="auth-note">
            <p>💡 <strong>Note:</strong> For now, create users via Django admin at <code>localhost:8000/admin</code></p>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AuthModal;
