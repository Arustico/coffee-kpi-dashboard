import api from './api';

const kpisService = {
  // Obtener dashboard metrics
  getDashboardMetrics: async () => {
    try {
      const response = await api.get('/kpis/dashboard');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Obtener revenue total
  getTotalRevenue: async () => {
    try {
      const response = await api.get('/kpis/revenue/total');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Obtener revenue por rango
  getRevenueByDateRange: async (startDate, endDate) => {
    try {
      const response = await api.post('/kpis/revenue/by-date-range', {
        start_date: startDate,
        end_date: endDate,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Obtener COGS
  getCogs: async () => {
    try {
      const response = await api.get('/kpis/cogs');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Obtener gross profit
  getGrossProfit: async () => {
    try {
      const response = await api.get('/kpis/gross-profit');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Obtener waste ratio
  getWasteRatio: async () => {
    try {
      const response = await api.get('/kpis/waste-ratio');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Obtener top productos
  getTopProducts: async (limit = 10) => {
    try {
      const response = await api.get(`/kpis/revenue/top-products?limit=${limit}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Obtener ventas del día
  getDailySales: async (date) => {
    try {
      const response = await api.get(`/kpis/sales/daily/${date}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },
};

export default kpisService;