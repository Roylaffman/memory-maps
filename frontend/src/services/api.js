/**
 * API Service
 * Centralized API client for communicating with Django backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1/memory-maps';

class APIError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.data = data;
  }
}

/**
 * Make an API request
 */
async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    headers: {
      ...options.headers,
    },
    ...options,
  };

  // Add Content-Type for JSON requests (but not for FormData)
  if (!(options.body instanceof FormData)) {
    config.headers['Content-Type'] = 'application/json';
  }

  // Add auth token if available (JWT)
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, config);
    
    // Handle non-JSON responses
    const contentType = response.headers.get('content-type');
    const isJSON = contentType && contentType.includes('application/json');
    
    const data = isJSON ? await response.json() : await response.text();

    if (!response.ok) {
      throw new APIError(
        data.detail || data.error || 'Request failed',
        response.status,
        data
      );
    }

    return data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError(error.message, 0, null);
  }
}

// =============================================================================
// MAP API
// =============================================================================

export const mapAPI = {
  /**
   * Get all maps (user's maps + public maps)
   */
  async getAll() {
    return request('/maps/');
  },

  /**
   * Get user's maps only
   */
  async getMyMaps() {
    return request('/maps/my_maps/');
  },

  /**
   * Get public maps only
   */
  async getPublicMaps() {
    return request('/maps/public_maps/');
  },

  /**
   * Get a single map by ID
   */
  async getById(id) {
    return request(`/maps/${id}/`);
  },

  /**
   * Create a new map
   */
  async create(mapData) {
    return request('/maps/', {
      method: 'POST',
      body: JSON.stringify(mapData),
    });
  },

  /**
   * Update a map
   */
  async update(id, mapData) {
    return request(`/maps/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(mapData),
    });
  },

  /**
   * Delete a map
   */
  async delete(id) {
    return request(`/maps/${id}/`, {
      method: 'DELETE',
    });
  },

  /**
   * Get all features for a map
   */
  async getFeatures(mapId) {
    return request(`/maps/${mapId}/features/`);
  },
};

// =============================================================================
// FEATURE API
// =============================================================================

export const featureAPI = {
  /**
   * Get all features (with optional filters)
   */
  async getAll(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return request(`/features/${queryString ? `?${queryString}` : ''}`);
  },

  /**
   * Get a single feature by ID
   */
  async getById(id) {
    return request(`/features/${id}/`);
  },

  /**
   * Create a new feature
   */
  async create(featureData) {
    return request('/features/', {
      method: 'POST',
      body: JSON.stringify(featureData),
    });
  },

  /**
   * Update a feature
   */
  async update(id, featureData) {
    return request(`/features/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(featureData),
    });
  },

  /**
   * Delete a feature
   */
  async delete(id) {
    return request(`/features/${id}/`, {
      method: 'DELETE',
    });
  },

  /**
   * Get all content (stories + photos) for a feature
   */
  async getContent(featureId) {
    return request(`/features/${featureId}/content/`);
  },
};

// =============================================================================
// STORY API
// =============================================================================

export const storyAPI = {
  /**
   * Get all stories (with optional filters)
   */
  async getAll(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return request(`/stories/${queryString ? `?${queryString}` : ''}`);
  },

  /**
   * Get a single story by ID
   */
  async getById(id) {
    return request(`/stories/${id}/`);
  },

  /**
   * Create a new story
   */
  async create(storyData) {
    return request('/stories/', {
      method: 'POST',
      body: JSON.stringify(storyData),
    });
  },

  /**
   * Update a story
   */
  async update(id, storyData) {
    return request(`/stories/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(storyData),
    });
  },

  /**
   * Delete a story
   */
  async delete(id) {
    return request(`/stories/${id}/`, {
      method: 'DELETE',
    });
  },
};

// =============================================================================
// PHOTO API
// =============================================================================

export const photoAPI = {
  /**
   * Get all photos (with optional filters)
   */
  async getAll(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return request(`/photos/${queryString ? `?${queryString}` : ''}`);
  },

  /**
   * Get a single photo by ID
   */
  async getById(id) {
    return request(`/photos/${id}/`);
  },

  /**
   * Upload a new photo
   */
  async upload(featureId, file, caption = '') {
    const formData = new FormData();
    formData.append('feature', featureId);
    formData.append('image', file);
    if (caption) {
      formData.append('caption', caption);
    }

    return request('/photos/', {
      method: 'POST',
      body: formData,
      // No headers - let browser set Content-Type for FormData with boundary
    });
  },

  /**
   * Update a photo
   */
  async update(id, photoData) {
    return request(`/photos/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(photoData),
    });
  },

  /**
   * Delete a photo
   */
  async delete(id) {
    return request(`/photos/${id}/`, {
      method: 'DELETE',
    });
  },
};

// =============================================================================
// IMPORT API
// =============================================================================

export const importAPI = {
  /**
   * Import GeoJSON file to a map
   */
  async importGeoJSON(mapId, file) {
    const formData = new FormData();
    formData.append('file', file);

    return request(`/maps/${mapId}/import_geojson/`, {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData,
    });
  },

  /**
   * Import KML/KMZ file to a map
   */
  async importKML(mapId, file) {
    const formData = new FormData();
    formData.append('file', file);

    return request(`/maps/${mapId}/import_kml/`, {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData,
    });
  },

  /**
   * Import coordinates from CSV to a map
   */
  async importCoordinates(mapId, file, options = {}) {
    const formData = new FormData();
    formData.append('file', file);
    
    if (options.lat_col) formData.append('lat_col', options.lat_col);
    if (options.lng_col) formData.append('lng_col', options.lng_col);
    if (options.name_col) formData.append('name_col', options.name_col);

    return request(`/maps/${mapId}/import_coordinates/`, {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData,
    });
  },
};

// =============================================================================
// AUTH API (placeholder for future implementation)
// =============================================================================

export const authAPI = {
  /**
   * Login user
   */
  async login(username, password) {
    // Use absolute URL for auth endpoint
    const authUrl = 'http://localhost:8000/api/auth/login/';
    
    const response = await fetch(authUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new APIError(error.detail || 'Login failed', response.status, error);
    }
    
    const data = await response.json();
    
    // JWT returns 'access' and 'refresh' tokens
    if (data.access) {
      localStorage.setItem('auth_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
    }
    
    // Get user info
    const user = await authAPI.getCurrentUser();
    
    return { token: data.access, user };
  },

  /**
   * Logout user
   */
  async logout() {
    try {
      const authUrl = 'http://localhost:8000/api/auth/logout/';
      const token = localStorage.getItem('auth_token');
      
      await fetch(authUrl, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
    } finally {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
    }
  },

  /**
   * Get current user
   */
  async getCurrentUser() {
    const authUrl = 'http://localhost:8000/api/auth/user/';
    const token = localStorage.getItem('auth_token');
    
    const response = await fetch(authUrl, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
    if (!response.ok) {
      throw new APIError('Failed to get user', response.status, null);
    }
    
    return response.json();
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    return !!localStorage.getItem('auth_token');
  },
};

export { APIError };
