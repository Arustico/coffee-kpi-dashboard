import api from './api';

const authService = {
  // Registrar usuario
  register: async (email, password, full_name, role_id = 1) => {
    try {
      const response = await api.post('/auth/register', {
        email,
        password,
        full_name,
        role_id,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Login
  login: async (email, password) => {
    try {
      const response = await api.post('/auth/login', {
        email,
        password,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Refrescar token
  refreshToken: async (refreshToken) => {
    try {
      const response = await api.post('/auth/refresh', {
        refresh_token: refreshToken,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Obtener usuario actual
  getCurrentUser: async () => {
    try {
      const response = await api.get('/auth/profile');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Logout (limpia el store)
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
};

export default authService;