import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify'; 
import 'react-toastify/dist/ReactToastify.css';   
import useAuthStore from './store/authStore';

// Páginas
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import DashboardPage from './pages/dashboard/DashboardPage';
import NotFoundPage from './pages/NotFoundPage';

// Componentes
import PrivateRoute from './components/common/PrivateRoute';

function App() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  // PRUEBA TEMPORAL
  console.log('App cargó correctamente');
  console.log('isAuthenticated:', isAuthenticated);
  console.log('API URL:', import.meta.env.VITE_API_URL);

  return (
    <BrowserRouter>
      <ToastContainer 
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={true}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
      <Routes>
        {/* Auth Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <PrivateRoute isAuthenticated={isAuthenticated}>
              <DashboardPage />
            </PrivateRoute>
          }
        />

        {/* Redirect */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;