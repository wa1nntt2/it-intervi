import { useEffect, useRef } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './stores/authStore'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Session from './pages/Session'
import SessionNew from './pages/SessionNew'
import InterviewSetup from './pages/InterviewSetup'
import Admin from './pages/Admin'
import AdminSessions from './pages/AdminSessions'
import AdminUsers from './pages/AdminUsers'
import ProfileEnhanced from './pages/ProfileEnhanced'
import NotFound from './pages/NotFound'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  const isLoading = useAuthStore((state) => state.isLoading)

  // Показываем загрузку во время инициализации сессии
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center">
        <div className="text-white text-lg animate-pulse">🚀 Загрузка...</div>
      </div>
    )
  }

  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />
}

function AdminRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, user, isLoading } = useAuthStore()

  // Показываем загрузку во время инициализации сессии
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center">
        <div className="text-white text-lg animate-pulse">🚀 Загрузка...</div>
      </div>
    )
  }

  // Если не аутентифицирован - редирект на login
  if (!isAuthenticated) {
    return <Navigate to="/login" />
  }

  // Если не админ - редирект на главную
  if (!user?.is_admin) {
    return <Navigate to="/" />
  }

  return <>{children}</>
}

function App() {
  const initializeSession = useAuthStore((state) => state.initializeSession)
  const hasInitialized = useRef(false)

  // Инициализация сессии при загрузке приложения (только один раз)
  useEffect(() => {
    console.log('[App] useEffect triggered, hasInitialized:', hasInitialized.current)
    if (!hasInitialized.current) {
      hasInitialized.current = true
      console.log('[App] Calling initializeSession()')
      initializeSession()
    }
  }, [initializeSession])

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/session/new"
          element={
            <PrivateRoute>
              <SessionNew />
            </PrivateRoute>
          }
        />
        <Route
          path="/interview/:professionId/setup"
          element={
            <PrivateRoute>
              <InterviewSetup />
            </PrivateRoute>
          }
        />
        <Route
          path="/session/:id"
          element={
            <PrivateRoute>
              <Session />
            </PrivateRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <AdminRoute>
              <Admin />
            </AdminRoute>
          }
        />
        <Route
          path="/admin/sessions"
          element={
            <AdminRoute>
              <AdminSessions />
            </AdminRoute>
          }
        />
        <Route
          path="/admin/users"
          element={
            <AdminRoute>
              <AdminUsers />
            </AdminRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <PrivateRoute>
              <ProfileEnhanced />
            </PrivateRoute>
          }
        />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
