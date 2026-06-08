import { FiMenu, FiLogOut, FiUser } from 'react-icons/fi';
import useAuthStore from '../../store/authStore';
import useAuth from '../../hooks/useAuth';

export default function Header({ onMenuClick }) {
  const user = useAuthStore((state) => state.user);
  const { logout } = useAuth();

  return (
    <header className="bg-white shadow-md px-6 py-4 flex items-center justify-between border-b border-gray-200">
      {/* Left Side - Menu */}
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuClick}
          className="p-2 hover:bg-gray-100 rounded-lg transition"
          title="Abrir/cerrar menú"
        >
          <FiMenu size={24} className="text-gray-700" />
        </button>
        <h1 className="text-2xl font-bold text-coffee-700">Coffee KPI Dashboard</h1>
      </div>

      {/* Right Side - User Info */}
      <div className="flex items-center gap-4">
        {/* User Info */}
        <div className="flex items-center gap-3 pr-4 border-r border-gray-200">
          <div className="w-10 h-10 bg-coffee-600 rounded-full flex items-center justify-center text-white font-bold">
            {user?.full_name?.charAt(0)?.toUpperCase() || 'U'}
          </div>
          <div className="hidden sm:block">
            <p className="text-sm font-semibold text-gray-800">
              {user?.full_name || 'Usuario'}
            </p>
            <p className="text-xs text-gray-500">{user?.email || 'email@example.com'}</p>
          </div>
        </div>

        {/* Logout Button */}
        <button
          onClick={logout}
          className="flex items-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition"
          title="Cerrar sesión"
        >
          <FiLogOut size={18} />
          <span className="hidden sm:inline">Salir</span>
        </button>
      </div>
    </header>
  );
}