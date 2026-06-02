import { useState } from 'react';
import { Link } from 'react-router-dom';
import { FiMail, FiLock, FiUser, FiLoader } from 'react-icons/fi';
import useAuth from '../../hooks/useAuth';

export default function RegisterPage() {
  const { register, loading, error } = useAuth();

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    passwordConfirm: '',
    full_name: '',
  });

  const [formError, setFormError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    setFormError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validaciones
    if (!formData.email || !formData.password || !formData.full_name) {
      setFormError('Todos los campos son requeridos');
      return;
    }

    if (formData.password.length < 8) {
      setFormError('La contraseña debe tener al menos 8 caracteres');
      return;
    }

    if (formData.password !== formData.passwordConfirm) {
      setFormError('Las contraseñas no coinciden');
      return;
    }

    if (formData.full_name.length < 2) {
      setFormError('El nombre debe tener al menos 2 caracteres');
      return;
    }

    try {
      await register(
        formData.email,
        formData.password,
        formData.full_name,
        1 // role_id default: barista
      );
    } catch (err) {
      // El error ya se muestra en el toast
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-coffee-50 to-coffee-100 px-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-coffee-700 mb-2">
            ☕ Coffee KPI
          </h1>
          <p className="text-gray-600">Crea tu cuenta</p>
        </div>

        {/* Card */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
            Registro
          </h2>

          {/* Error general */}
          {formError && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600 text-sm">{formError}</p>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Full Name */}
            <div>
              <label htmlFor="full_name" className="block text-sm font-medium text-gray-700 mb-2">
                Nombre Completo
              </label>
              <div className="relative">
                <FiUser className="absolute left-3 top-3 text-gray-400" />
                <input
                  type="text"
                  id="full_name"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  placeholder="Tu nombre completo"
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-coffee-500 focus:border-transparent outline-none transition"
                  disabled={loading}
                />
              </div>
            </div>

            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <div className="relative">
                <FiMail className="absolute left-3 top-3 text-gray-400" />
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="tu@email.com"
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-coffee-500 focus:border-transparent outline-none transition"
                  disabled={loading}
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Contraseña
              </label>
              <div className="relative">
                <FiLock className="absolute left-3 top-3 text-gray-400" />
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Mínimo 8 caracteres"
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-coffee-500 focus:border-transparent outline-none transition"
                  disabled={loading}
                />
              </div>
            </div>

            {/* Password Confirm */}
            <div>
              <label htmlFor="passwordConfirm" className="block text-sm font-medium text-gray-700 mb-2">
                Confirmar Contraseña
              </label>
              <div className="relative">
                <FiLock className="absolute left-3 top-3 text-gray-400" />
                <input
                  type="password"
                  id="passwordConfirm"
                  name="passwordConfirm"
                  value={formData.passwordConfirm}
                  onChange={handleChange}
                  placeholder="Repite tu contraseña"
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-coffee-500 focus:border-transparent outline-none transition"
                  disabled={loading}
                />
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full mt-6 bg-coffee-600 hover:bg-coffee-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading && <FiLoader className="animate-spin" />}
              {loading ? 'Registrando...' : 'Registrarse'}
            </button>
          </form>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">O</span>
            </div>
          </div>

          {/* Login Link */}
          <p className="text-center text-gray-600 text-sm">
            ¿Ya tienes cuenta?{' '}
            <Link
              to="/login"
              className="text-coffee-600 hover:text-coffee-700 font-semibold transition"
            >
              Inicia sesión aquí
            </Link>
          </p>
        </div>

        {/* Footer */}
        <p className="text-center text-gray-500 text-xs mt-6">
          © 2026 Coffee KPI Dashboard. Todos los derechos reservados.
        </p>
      </div>
    </div>
  );
}