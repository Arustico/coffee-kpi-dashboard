import { Link, useLocation } from 'react-router-dom';
import { 
  FiHome, 
  FiShoppingCart, 
  FiPackage, 
  FiTrash2, 
  FiBarChart2, 
  FiUsers,
  FiChevronLeft
} from 'react-icons/fi';
import clsx from 'clsx';

export default function Sidebar({ isOpen, onToggle }) {
  const location = useLocation();

  const menuItems = [
    { label: 'Dashboard', icon: FiHome, href: '/dashboard', id: 'dashboard' },
    { label: 'Ventas', icon: FiShoppingCart, href: '/dashboard/sales', id: 'sales' },
    { label: 'Insumos', icon: FiPackage, href: '/dashboard/ingredients', id: 'ingredients' },
    { label: 'Merma', icon: FiTrash2, href: '/dashboard/waste', id: 'waste' },
    { label: 'Reportes', icon: FiBarChart2, href: '/dashboard/reports', id: 'reports' },
    { label: 'Admin', icon: FiUsers, href: '/dashboard/admin', id: 'admin' },
  ];

  const isActive = (href) => location.pathname === href;

  return (
    <div
      className={clsx(
        'bg-coffee-700 text-white transition-all duration-300 flex flex-col shadow-lg',
        isOpen ? 'w-64' : 'w-20'
      )}
    >
      {/* Logo */}
      <div className="p-4 border-b border-coffee-600 flex items-center justify-between">
        {isOpen && (
          <h1 className="text-2xl font-bold">☕ KPI</h1>
        )}
        <button
          onClick={onToggle}
          className="p-2 hover:bg-coffee-600 rounded-lg transition"
        >
          <FiChevronLeft size={20} />
        </button>
      </div>

      {/* Menu Items */}
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.href);

          return (
            <Link
              key={item.id}
              to={item.href}
              className={clsx(
                'flex items-center gap-3 px-4 py-3 rounded-lg transition duration-200',
                active
                  ? 'bg-coffee-600 text-white'
                  : 'text-coffee-100 hover:bg-coffee-600'
              )}
              title={item.label}
            >
              <Icon size={20} />
              {isOpen && <span className="font-medium">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-coffee-600 text-xs text-coffee-100 text-center">
        {isOpen && <p>v0.2.0</p>}
      </div>
    </div>
  );
}