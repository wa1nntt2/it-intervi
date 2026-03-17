import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'

export function Header() {
  const { isAuthenticated, user } = useAuthStore()
  const logout = useAuthStore((state) => state.logout)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-xl font-bold text-indigo-600">
          IT Interview Trainer
        </Link>
        <nav className="flex gap-4">
          {isAuthenticated ? (
            <>
              {/* Ссылка на админку только для администраторов */}
              {user?.is_admin && (
                <Link to="/admin" className="text-gray-600 hover:text-gray-900">
                  Админ
                </Link>
              )}
              <button onClick={handleLogout} className="text-gray-600 hover:text-gray-900">
                Выход
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-gray-600 hover:text-gray-900">
                Вход
              </Link>
              <Link to="/register" className="text-gray-600 hover:text-gray-900">
                Регистрация
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
