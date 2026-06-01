Se creo el frontend con lo siguiente

```bash
# En la raíz del proyecto
cd ./coffee-kpi-dashboard

# Si no lo creaste aún:
npm create vite@latest frontend -- --template react

cd frontend
npm install
```

En el interior de la carpeta frontend se instalaron las siguientes librerías. 


```bash
# Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Router
npm install react-router-dom

# HTTP Client
npm install axios

# Estado global
npm install zustand

# Notificaciones
npm install react-toastify

# Gráficos
npm install recharts

# Iconos
npm install react-icons

# Utilidades
npm install clsx date-fns
```

Luego se crearon las carpetas con el fin de crear este arbol:

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/              # Componentes reutilizables
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── Navbar.jsx
│   │   ├── layout/              # Layouts
│   │   │   ├── MainLayout.jsx
│   │   │   └── AuthLayout.jsx
│   │   ├── auth/                # Componentes de auth
│   │   ├── dashboard/           # Componentes de dashboard
│   │   └── operations/          # Componentes de operaciones
│   ├── pages/
│   │   ├── auth/
│   │   │   ├── LoginPage.jsx
│   │   │   └── RegisterPage.jsx
│   │   ├── dashboard/
│   │   │   └── DashboardPage.jsx
│   │   └── operations/
│   │       ├── SalesPage.jsx
│   │       ├── IngredientsPage.jsx
│   │       ├── WastePage.jsx
│   │       └── ReportsPage.jsx
│   ├── hooks/                   # Hooks personalizados
│   │   ├── useAuth.js
│   │   ├── useFetch.js
│   │   └── useForm.js
│   ├── store/                   # Zustand stores
│   │   ├── authStore.js
│   │   └── appStore.js
│   ├── services/                # API calls
│   │   ├── api.js               # Cliente HTTP
│   │   ├── authService.js
│   │   ├── salesService.js
│   │   ├── ingredientsService.js
│   │   ├── wasteService.js
│   │   └── kpisService.js
│   ├── utils/
│   │   ├── formatters.js        # Funciones de formato
│   │   ├── validators.js        # Validaciones
│   │   └── constants.js
│   ├── constants/
│   │   └── apiEndpoints.js
│   ├── styles/
│   │   └── globals.css
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── .env.local
└── .gitignore

```












