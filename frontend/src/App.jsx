import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify'; 
import 'react-toastify/dist/ReactToastify.css';   
import useAuthStore from './store/authStore';

// Páginas
import LoginPage from './pages/auth/LoginPage';
import DashboardPage from './pages/dashboard/DashboardPage';
import NotFoundPage from './pages/NotFoundPage';

// Layouts
import MainLayout from './components/layout/MainLayout';

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

       {/* Protected Routes con MainLayout */}
        <Route
          element={
            <PrivateRoute isAuthenticated={isAuthenticated}>
              <MainLayout />
            </PrivateRoute>
          }
        >
          <Route path="/dashboard" element={<DashboardPage />} />
        </Route>

        {/* Redirect */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;