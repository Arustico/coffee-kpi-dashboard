import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-red-600">404</h1>
        <p className="text-gray-600 mt-4">Página no encontrada</p>
        <Link to="/" className="text-coffee-600 hover:underline mt-4 inline-block">
          Volver al dashboard
        </Link>
      </div>
    </div>
  );
}