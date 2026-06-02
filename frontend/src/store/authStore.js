import { create } from 'zustand';

const useAuthStore = create((set) => ({
  user: null,
  accessToken: localStorage.getItem('access_token'),
  refreshToken: localStorage.getItem('refresh_token'),
  isAuthenticated: !!localStorage.getItem('access_token'),

  // Acciones
  setUser: (user) => set({ user }),

  setTokens: (accessToken, refreshToken) => {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
    set({
      accessToken,
      refreshToken,
      isAuthenticated: true,
    });
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    set({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
    });
  },

  setAuthenticated: (isAuthenticated) => {
    set({ isAuthenticated });
  },
}));

export default useAuthStore;