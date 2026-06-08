import { useState, useEffect } from 'react';
import { FiX, FiPlus, FiTrash2 } from 'react-icons/fi';
import { toast } from 'react-toastify';
import useFetch from '../../hooks/useFetch';
import salesService from '../../services/salesService';

export default function SaleModal({ onClose, onSubmit }) {
  const [items, setItems] = useState([{ product_id: null, quantity: 1, unit_price: 0 }]);
  const [formData, setFormData] = useState({
    employee_id: null,
    turn_id: null,
  });

  const { data: employees } = useFetch(() => salesService.getEmployees());
  const { data: turns } = useFetch(() => salesService.getTurns());
  const { data: products } = useFetch(() => salesService.getProducts());

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: parseInt(value),
    }));
  };

  const handleItemChange = (index, field, value) => {
    const newItems = [...items];
    newItems[index][field] = field === 'quantity' || field === 'unit_price' ? parseFloat(value) : parseInt(value);
    setItems(newItems);
  };

  const handleAddItem = () => {
    setItems([...items, { product_id: null, quantity: 1, unit_price: 0 }]);
  };

  const handleRemoveItem = (index) => {
    setItems(items.filter((_, i) => i !== index));
  };

  const calculateTotal = () => {
    return items.reduce((total, item) => total + (item.quantity * item.unit_price), 0);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!formData.employee_id || !formData.turn_id) {
      toast.error('Debe seleccionar empleado y turno');
      return;
    }

    if (items.some(item => !item.product_id || item.quantity <= 0)) {
      toast.error('Todos los items deben tener producto y cantidad válida');
      return;
    }

    const saleData = {
      ...formData,
      items: items.map(item => ({
        product_id: item.product_id,
        quantity: item.quantity,
        unit_price: item.unit_price,
      })),
      total_amount: calculateTotal(),
    };

    onSubmit(saleData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 flex items-center justify-between p-6 border-b bg-white">
          <h2 className="text-2xl font-bold text-gray-900">Nueva Venta</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition"
          >
            <FiX size={24} />
          </button>
        </div>

        {/* Content */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Empleado y Turno */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Empleado *
              </label>
              <select
                name="employee_id"
                value={formData.employee_id || ''}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-coffee-500 outline-none"
              >
                <option value="">Seleccionar empleado</option>
                {employees?.items?.map((emp) => (
                  <option key={emp.id} value={emp.id}>
                    {emp.full_name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Turno *
              </label>
              <select
                name="turn_id"
                value={formData.turn_id || ''}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-coffee-500 outline-none"
              >
                <option value="">Seleccionar turno</option>
                {turns?.items?.map((turn) => (
                  <option key={turn.id} value={turn.id}>
                    {turn.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Items */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <label className="block text-sm font-medium text-gray-700">
                Productos *
              </label>
              <button
                type="button"
                onClick={handleAddItem}
                className="flex items-center gap-2 px-3 py-1 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
              >
                <FiPlus size={16} />
                Agregar Item
              </button>
            </div>

            <div className="space-y-3 border rounded-lg p-4 bg-gray-50">
              {items.map((item, index) => (
                <div key={index} className="flex gap-3 items-end bg-white p-3 rounded-lg border">
                  <div className="flex-1">
                    <label className="block text-xs font-medium text-gray-600 mb-1">
                      Producto
                    </label>
                    <select
                      value={item.product_id || ''}
                      onChange={(e) => handleItemChange(index, 'product_id', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-coffee-500 outline-none text-sm"
                    >
                      <option value="">Seleccionar</option>
                      {products?.items?.map((prod) => (
                        <option key={prod.id} value={prod.id}>
                          {prod.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="w-24">
                    <label className="block text-xs font-medium text-gray-600 mb-1">
                      Cantidad
                    </label>
                    <input
                      type="number"
                      value={item.quantity}
                      onChange={(e) => handleItemChange(index, 'quantity', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-coffee-500 outline-none text-sm"
                      min="1"
                    />
                  </div>

                  <div className="w-24">
                    <label className="block text-xs font-medium text-gray-600 mb-1">
                      Precio
                    </label>
                    <input
                      type="number"
                      value={item.unit_price}
                      onChange={(e) => handleItemChange(index, 'unit_price', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-coffee-500 outline-none text-sm"
                      min="0"
                      step="0.01"
                    />
                  </div>

                  <button
                    type="button"
                    onClick={() => handleRemoveItem(index)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                  >
                    <FiTrash2 size={18} />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Total */}
          <div className="flex justify-end">
            <div className="bg-coffee-50 border border-coffee-200 rounded-lg p-4">
              <p className="text-sm text-gray-600 mb-2">Total</p>
              <p className="text-3xl font-bold text-coffee-700">
                ${calculateTotal().toLocaleString('es-CO', { maximumFractionDigits: 2 })}
              </p>
            </div>
          </div>

          {/* Buttons */}
          <div className="flex gap-2 justify-end border-t pt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-6 py-2 bg-coffee-600 text-white rounded-lg hover:bg-coffee-700 transition"
            >
              Registrar Venta
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}