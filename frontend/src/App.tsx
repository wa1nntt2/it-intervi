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
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />
}

function App() {
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
            <PrivateRoute>
              <Admin />
            </PrivateRoute>
          }
        />
        <Route
          path="/admin/sessions"
          element={
            <PrivateRoute>
              <AdminSessions />
            </PrivateRoute>
          }
        />
        <Route
          path="/admin/users"
          element={
            <PrivateRoute>
              <AdminUsers />
            </PrivateRoute>
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
