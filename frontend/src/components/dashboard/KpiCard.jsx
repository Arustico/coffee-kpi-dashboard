import { FiArrowUp, FiArrowDown } from 'react-icons/fi';

export default function KpiCard({ 
  title, 
  value, 
  icon: Icon, 
  color = 'blue',
  unit = '',
  change = null,
  isPositive = true 
}) {
  const colorClasses = {
    blue: 'bg-blue-50 border-blue-200 text-blue-600',
    green: 'bg-green-50 border-green-200 text-green-600',
    red: 'bg-red-50 border-red-200 text-red-600',
    yellow: 'bg-yellow-50 border-yellow-200 text-yellow-600',
    purple: 'bg-purple-50 border-purple-200 text-purple-600',
    coffee: 'bg-coffee-50 border-coffee-200 text-coffee-600',
  };

  return (
    <div className={`${colorClasses[color]} border rounded-lg p-6 shadow-sm hover:shadow-md transition`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 mb-2">{title}</p>
          <p className="text-3xl font-bold text-gray-900">
            {typeof value === 'number' ? value.toLocaleString('es-CO') : value}
            {unit && <span className="text-lg text-gray-600 ml-1">{unit}</span>}
          </p>
          {change !== null && (
            <div className="flex items-center gap-1 mt-2">
              {isPositive ? (
                <FiArrowUp className="text-green-600" size={16} />
              ) : (
                <FiArrowDown className="text-red-600" size={16} />
              )}
              <span className={`text-sm font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                {change}%
              </span>
            </div>
          )}
        </div>
        {Icon && (
          <div className="p-3 rounded-lg bg-white/50">
            <Icon size={28} />
          </div>
        )}
      </div>
    </div>
  );
}