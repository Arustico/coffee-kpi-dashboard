import { useState, useEffect } from 'react';
import { 
  FiPlus, 
  FiTrash2, 
  FiEye, 
  FiRefreshCw,
  FiSearch,
  FiX
} from 'react-icons/fi';
import { toast } from 'react-toastify';
import useFetch from '../../hooks/useFetch';
import salesService from '../../services/salesService';
import SaleModal from '../../components/operations/SaleModal';
import SaleDetailModal from '../../components/operations/SaleDetailModal';

export default function SalesPage() {
  const [sales, setSales] = useState([]);
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Modals
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedSale, setSelectedSale] = useState(null);

  const { data, loading, error, refetch } = useFetch(() =>
    salesService.getAllSales(skip, limit)
  );

  useEffect(() => {
    if (data) {
      setSales(data.items || []);
    }
  }, [data]);

  const handleDeleteSale = async (saleId) => {
    if (!window.confirm('¿Estás seguro de que deseas eliminar esta venta?')) {
      return;
    }

    try {
      await salesService.deleteSale(saleId);
      toast.success('Venta eliminada exitosamente');
      refetch();
    } catch (err) {
      toast.error(err.detail || 'Error al eliminar venta');
    }
  };

  const handleViewDetail = async (saleId) => {
    try {
      const sale = await salesService.getSaleById(saleId);
      setSelectedSale(sale);
      setShowDetailModal(true);
    } catch (err) {
      toast.error(err.detail || 'Error al cargar venta');
    }
  };

  const handleCreateSale = async (saleData) => {
    try {
      await salesService.createSale(saleData);
      toast.success('Venta creada exitosamente');
      setShowCreateModal(false);
      refetch();
    } catch (err) {
      toast.error(err.detail || 'Error al crear venta');
    }
  };

  // Filtrar ventas
  const filteredSales = sales.filter(sale => 
    sale.id.toString().includes(searchTerm) ||
    sale.employee_name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <FiRefreshCw size={48} className="text-coffee-600 animate-spin" />
          <p className="text-gray-600 mt-4">Cargando ventas...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Ventas</h1>
        <div className="flex gap-2">
          <button
            onClick={refetch}
            className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition"
          >
            <FiRefreshCw size={18} />
            Actualizar
          </button>
          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-2 px-4 py-2 bg-coffee-600 text-white rounded-lg hover:bg-coffee-700 transition"
          >
            <FiPlus size={18} />
            Nueva Venta
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="relative">
          <FiSearch className="absolute left-3 top-3 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Buscar por ID o empleado..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-coffee-500 focus:border-transparent outline-none"
          />
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {/* Table */}
      <div className="bg-white rounded-lg shadow overflow-x-auto">
        {filteredSales.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <p>No hay ventas registradas</p>
          </div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">ID</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Empleado</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Turno</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Total</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Fecha</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {filteredSales.map((sale) => (
                <tr key={sale.id} className="hover:bg-gray-50 transition">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">#{sale.id}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{sale.employee_name}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{sale.turn_label}</td>
                  <td className="px-6 py-4 text-sm font-semibold text-green-600">
                    ${sale.total_amount?.toLocaleString('es-CO', { maximumFractionDigits: 2 })}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {new Date(sale.sold_at).toLocaleDateString('es-CO')}
                  </td>
                  <td className="px-6 py-4 text-sm space-x-2 flex">
                    <button
                      onClick={() => handleViewDetail(sale.id)}
                      className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition"
                      title="Ver detalles"
                    >
                      <FiEye size={18} />
                    </button>
                    <button
                      onClick={() => handleDeleteSale(sale.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                      title="Eliminar venta"
                    >
                      <FiTrash2 size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between">
        <p className="text-gray-600 text-sm">
          Mostrando {filteredSales.length} de {data?.total || 0} ventas
        </p>
        <div className="flex gap-2">
          <button
            onClick={() => setSkip(Math.max(0, skip - limit))}
            disabled={skip === 0}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
          >
            Anterior
          </button>
          <button
            onClick={() => setSkip(skip + limit)}
            disabled={skip + limit >= (data?.total || 0)}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
          >
            Siguiente
          </button>
        </div>
      </div>

      {/* Modals */}
      {showCreateModal && (
        <SaleModal
          onClose={() => setShowCreateModal(false)}
          onSubmit={handleCreateSale}
        />
      )}

      {showDetailModal && selectedSale && (
        <SaleDetailModal
          sale={selectedSale}
          onClose={() => setShowDetailModal(false)}
        />
      )}
    </div>
  );
}