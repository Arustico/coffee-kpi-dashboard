import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import useAuthStore from '../store/authStore';
import authService from '../services/authService';

const useAuth = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const { setUser, setTokens, logout: logoutStore, user } = useAuthStore();

  // Registro
  const register = async (email, password, full_name, role_id = 1) => {
    setLoading(true);
    setError(null);
    try {
      const data = await authService.register(email, password, full_name, role_id);
      
      // Guardar tokens
      setTokens(data.access_token, data.refresh_token);
      setUser(data.user);

      toast.success('¡Registro exitoso!');
      navigate('/dashboard');
      
      return data;
    } catch (err) {
      const message = err.detail || 'Error al registrar';
      setError(message);
      toast.error(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Login
  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const data = await authService.login(email, password);
      
      // Guardar tokens
      setTokens(data.access_token, data.refresh_token);
      setUser(data.user);

      toast.success('¡Bienvenido!');
      navigate('/dashboard');
      
      return data;
    } catch (err) {
      const message = err.detail || 'Email o contraseña incorrectos';
      setError(message);
      toast.error(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Logout
  const logout = () => {
    authService.logout();
    logoutStore();
    toast.success('Sesión cerrada');
    navigate('/login');
  };

  return {
    user,
    loading,
    error,
    register,
    login,
    logout,
  };
};

export default useAuth;