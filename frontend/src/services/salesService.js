import api from './api';

const salesService = {
  // Listar todas las ventas
  getAllSales: async (skip = 0, limit = 10) => {
    try {
      const response = await api.get(`/sales?skip=${skip}&limit=${limit}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Obtener venta por ID
  getSaleById: async (saleId) => {
    try {
      const response = await api.get(`/sales/${saleId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Crear venta
  createSale: async (saleData) => {
    try {
      const response = await api.post('/sales', saleData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Actualizar venta
  updateSale: async (saleId, saleData) => {
    try {
      const response = await api.put(`/sales/${saleId}`, saleData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Eliminar venta
  deleteSale: async (saleId) => {
    try {
      const response = await api.delete(`/sales/${saleId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Listar empleados (para crear venta)
  getEmployees: async () => {
    try {
      const response = await api.get('/employees');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Listar turnos
  getTurns: async () => {
    try {
      const response = await api.get('/employees/turns');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Listar productos
  getProducts: async () => {
    try {
      const response = await api.get('/ingredients/products');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },
};

export default salesService;