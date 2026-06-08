import { FiX } from 'react-icons/fi';

export default function SaleDetailModal({ sale, onClose }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 flex items-center justify-between p-6 border-b bg-white">
          <h2 className="text-2xl font-bold text-gray-900">Detalle de Venta #{sale.id}</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition"
          >
            <FiX size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Información General */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">Empleado</p>
              <p className="text-lg font-semibold text-gray-900">{sale.employee_name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Turno</p>
              <p className="text-lg font-semibold text-gray-900">{sale.turn_label}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Fecha</p>
              <p className="text-lg font-semibold text-gray-900">
                {new Date(sale.sold_at).toLocaleDateString('es-CO')}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Hora</p>
              <p className="text-lg font-semibold text-gray-900">
                {new Date(sale.sold_at).toLocaleTimeString('es-CO')}
              </p>
            </div>
          </div>

          {/* Items */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Productos</h3>
            <div className="border rounded-lg overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50 border-b">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Producto</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Cantidad</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Precio Unitario</th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Subtotal</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {sale.items?.map((item, index) => (
                    <tr key={index}>
                      <td className="px-4 py-3 text-sm text-gray-900">{item.product_name}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{item.quantity}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">
                        ${item.unit_price?.toLocaleString('es-CO', { maximumFractionDigits: 2 })}
                      </td>
                      <td className="px-4 py-3 text-sm font-semibold text-gray-900">
                        ${(item.quantity * item.unit_price)?.toLocaleString('es-CO', { maximumFractionDigits: 2 })}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Total */}
          <div className="flex justify-end">
            <div className="bg-coffee-50 border border-coffee-200 rounded-lg p-4">
              <p className="text-sm text-gray-600 mb-2">Total</p>
              <p className="text-3xl font-bold text-coffee-700">
                ${sale.total_amount?.toLocaleString('es-CO', { maximumFractionDigits: 2 })}
              </p>
            </div>
          </div>

          {/* Close Button */}
          <div className="flex justify-end border-t pt-6">
            <button
              onClick={onClose}
              className="px-6 py-2 bg-coffee-600 text-white rounded-lg hover:bg-coffee-700 transition"
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}