import { 
  FiDollarSign, 
  FiTrendingDown, 
  FiPercent, 
  FiShoppingCart,
  FiRefreshCw,
  FiTrash2
} from 'react-icons/fi';
import KpiCard from '../../components/dashboard/KpiCard';
import useFetch from '../../hooks/useFetch';
import kpisService from '../../services/kpisService';

export default function DashboardPage() {
  const { data: metrics, loading, error, refetch } = useFetch(() =>
    kpisService.getDashboardMetrics()
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin">
            <FiRefreshCw size={48} className="text-coffee-600" />
          </div>
          <p className="text-gray-600 mt-4">Cargando dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <p className="text-red-600 font-semibold">Error al cargar el dashboard</p>
        <p className="text-red-600 text-sm mt-2">{error}</p>
        <button
          onClick={refetch}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
        >
          Reintentar
        </button>
      </div>
    );
  }

  if (!metrics) {
    return <p className="text-gray-600">No hay datos disponibles</p>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <button
          onClick={refetch}
          className="flex items-center gap-2 px-4 py-2 bg-coffee-600 text-white rounded-lg hover:bg-coffee-700 transition"
        >
          <FiRefreshCw size={18} />
          Actualizar
        </button>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Revenue */}
        <KpiCard
          title="Ingresos Totales"
          value={metrics.total_revenue?.toFixed(2) || 0}
          unit="$"
          icon={FiDollarSign}
          color="green"
        />

        {/* COGS */}
        <KpiCard
          title="Costo de Bienes"
          value={metrics.total_cogs?.toFixed(2) || 0}
          unit="$"
          icon={FiTrendingDown}
          color="red"
        />

        {/* Gross Profit */}
        <KpiCard
          title="Ganancia Bruta"
          value={metrics.gross_profit?.toFixed(2) || 0}
          unit="$"
          icon={FiDollarSign}
          color="blue"
        />

        {/* Gross Margin */}
        <KpiCard
          title="Margen Bruto"
          value={metrics.gross_margin_percentage?.toFixed(2) || 0}
          unit="%"
          icon={FiPercent}
          color="purple"
        />

        {/* Waste Cost */}
        <KpiCard
          title="Costo de Merma"
          value={metrics.waste_cost?.toFixed(2) || 0}
          unit="$"
          icon={FiTrash2}
          color="yellow"
        />

        {/* Waste Ratio */}
        <KpiCard
          title="Waste Ratio"
          value={metrics.waste_ratio_percentage?.toFixed(2) || 0}
          unit="%"
          icon={FiPercent}
          color="red"
        />

        {/* Total Sales */}
        <KpiCard
          title="Total de Ventas"
          value={metrics.total_sales || 0}
          icon={FiShoppingCart}
          color="coffee"
        />

        {/* Active Products */}
        <KpiCard
          title="Productos Activos"
          value={metrics.active_products || 0}
          icon={FiShoppingCart}
          color="blue"
        />
      </div>

      {/* Additional Info */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        {/* Summary */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Resumen</h2>
          <div className="space-y-3">
            <div className="flex justify-between items-center pb-3 border-b">
              <span className="text-gray-600">Total de Ingresos:</span>
              <span className="font-semibold text-gray-900">
                ${metrics.total_revenue?.toLocaleString('es-CO', { maximumFractionDigits: 2 })}
              </span>
            </div>
            <div className="flex justify-between items-center pb-3 border-b">
              <span className="text-gray-600">Costo de Bienes:</span>
              <span className="font-semibold text-gray-900">
                ${metrics.total_cogs?.toLocaleString('es-CO', { maximumFractionDigits: 2 })}
              </span>
            </div>
            <div className="flex justify-between items-center pb-3 border-b">
              <span className="text-gray-600">Ganancia Neta:</span>
              <span className="font-semibold text-green-600">
                ${metrics.gross_profit?.toLocaleString('es-CO', { maximumFractionDigits: 2 })}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Waste Ratio:</span>
              <span className="font-semibold text-red-600">
                {metrics.waste_ratio_percentage?.toFixed(2)}%
              </span>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Estadísticas Rápidas</h2>
          <div className="space-y-3">
            <div className="flex justify-between items-center pb-3 border-b">
              <span className="text-gray-600">Total de Ventas:</span>
              <span className="font-semibold text-gray-900">{metrics.total_sales}</span>
            </div>
            <div className="flex justify-between items-center pb-3 border-b">
              <span className="text-gray-600">Productos Activos:</span>
              <span className="font-semibold text-gray-900">{metrics.active_products}</span>
            </div>
            <div className="flex justify-between items-center pb-3 border-b">
              <span className="text-gray-600">Margen de Ganancia:</span>
              <span className="font-semibold text-green-600">
                {metrics.gross_margin_percentage?.toFixed(2)}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Costo de Merma:</span>
              <span className="font-semibold text-yellow-600">
                ${metrics.waste_cost?.toLocaleString('es-CO', { maximumFractionDigits: 2 })}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}