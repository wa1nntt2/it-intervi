import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import { ThemeToggle } from '../components/ui/ThemeToggle'

export default function Home() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
      <header className="bg-white/10 backdrop-blur-md shadow-lg dark:bg-gray-800/20">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
              <span className="text-2xl">🎯</span>
            </div>
            <h1 className="text-2xl font-bold text-white dark:text-gray-100">IT Interview Trainer</h1>
          </div>
          <div className="flex items-center gap-4">
            <ThemeToggle />
            {isAuthenticated && (
              <>
                <button
                  onClick={() => navigate('/profile')}
                  className="bg-white/20 backdrop-blur-sm text-white px-4 py-2 rounded-lg hover:bg-white/30 transition-all flex items-center gap-2 dark:bg-gray-700/50 dark:text-gray-100 dark:hover:bg-gray-600/50"
                >
                  <span>👤</span>
                  <span className="hidden sm:inline">Профиль</span>
                </button>
                <span className="text-white/90 dark:text-gray-200 font-medium">{user?.email}</span>
                <button
                  onClick={handleLogout}
                  className="bg-white/20 text-white px-4 py-2 rounded-lg hover:bg-white/30 transition-colors backdrop-blur-sm dark:bg-gray-700/50 dark:text-gray-100 dark:hover:bg-gray-600/50"
                >
                  Выйти
                </button>
              </>
            )}
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="text-center">
          {/* Hero Section */}
          <div className="mb-6">
            <div className="inline-block mb-3">
              <span className="bg-white/20 backdrop-blur-sm text-white px-4 py-1.5 rounded-full text-sm font-medium dark:bg-gray-700/50 dark:text-gray-100">
                🚀 Твой путь к работе мечты
              </span>
            </div>
            <h2 className="text-4xl md:text-5xl font-extrabold text-white dark:text-gray-100 mb-3 leading-tight">
              Подготовься к собеседованию<br />
              <span className="text-yellow-300 dark:text-yellow-400">на работу мечты</span>
            </h2>
            <p className="text-lg text-white/90 dark:text-gray-300 mb-6 max-w-2xl mx-auto">
              Практикуйся отвечать на реальные вопросы по программированию.<br />
              <span className="font-semibold">Frontend • Backend • Fullstack • DevOps</span>
            </p>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-4 mb-6 max-w-4xl mx-auto">
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 text-white hover:bg-white/20 transition-all hover:scale-105 dark:bg-gray-800/30 dark:hover:bg-gray-700/30 dark:text-gray-100">
              <div className="text-3xl mb-2">📝</div>
              <h3 className="text-lg font-bold mb-1">Разные типы вопросов</h3>
              <p className="text-white/80 dark:text-gray-400 text-sm">Multiple Choice и упорядочивание — как на реальном собеседовании</p>
            </div>
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 text-white hover:bg-white/20 transition-all hover:scale-105 dark:bg-gray-800/30 dark:hover:bg-gray-700/30 dark:text-gray-100">
              <div className="text-3xl mb-2">📊</div>
              <h3 className="text-lg font-bold mb-1">Отслеживание прогресса</h3>
              <p className="text-white/80 dark:text-gray-400 text-sm">Следи за своими результатами и улучшайся с каждой попыткой</p>
            </div>
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 text-white hover:bg-white/20 transition-all hover:scale-105 dark:bg-gray-800/30 dark:hover:bg-gray-700/30 dark:text-gray-100">
              <div className="text-3xl mb-2">🎓</div>
              <h3 className="text-lg font-bold mb-1">Для всех уровней</h3>
              <p className="text-white/80 dark:text-gray-400 text-sm">Вопросы разной сложности: от Junior до Senior</p>
            </div>
          </div>

          {/* CTA Buttons */}
          {isAuthenticated ? (
            <div className="flex flex-col sm:flex-row justify-center gap-3 mb-6">
              <Link
                to="/session/new"
                className="group bg-white text-indigo-600 px-6 py-3 rounded-xl font-bold text-lg hover:bg-yellow-300 transition-all hover:scale-105 shadow-xl flex items-center justify-center gap-2 dark:bg-indigo-600 dark:text-white dark:hover:bg-indigo-700"
              >
                <span>🎯</span>
                Начать сессию
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </Link>
              <Link
                to="/admin"
                className="bg-white/20 backdrop-blur-sm text-white border-2 border-white/50 px-6 py-3 rounded-xl font-bold text-lg hover:bg-white/30 transition-all hover:scale-105 dark:bg-gray-800/50 dark:border-gray-600 dark:text-gray-100 dark:hover:bg-gray-700/50"
              >
                ⚙️ Админ-панель
              </Link>
            </div>
          ) : (
            <div className="flex flex-col sm:flex-row justify-center gap-3 mb-6">
              <Link
                to="/register"
                className="group bg-white text-indigo-600 px-6 py-3 rounded-xl font-bold text-lg hover:bg-yellow-300 transition-all hover:scale-105 shadow-xl flex items-center justify-center gap-2 dark:bg-indigo-600 dark:text-white dark:hover:bg-indigo-700"
              >
                <span>🚀</span>
                Начать бесплатно
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </Link>
              <Link
                to="/login"
                className="bg-white/20 backdrop-blur-sm text-white border-2 border-white/50 px-6 py-3 rounded-xl font-bold text-lg hover:bg-white/30 transition-all hover:scale-105 dark:bg-gray-800/50 dark:border-gray-600 dark:text-gray-100 dark:hover:bg-gray-700/50"
              >
                🔐 Войти
              </Link>
            </div>
          )}

          {/* Stats */}
          <div className="grid grid-cols-3 gap-6 max-w-xl mx-auto">
            <div className="text-white dark:text-gray-100">
              <div className="text-3xl font-extrabold mb-1">4+</div>
              <div className="text-white/80 dark:text-gray-400 text-sm">Профессии</div>
            </div>
            <div className="text-white dark:text-gray-100">
              <div className="text-3xl font-extrabold mb-1">∞</div>
              <div className="text-white/80 dark:text-gray-400 text-sm">Вопросов</div>
            </div>
            <div className="text-white dark:text-gray-100">
              <div className="text-3xl font-extrabold mb-1">24/7</div>
              <div className="text-white/80 dark:text-gray-400 text-sm">Доступно</div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white/10 backdrop-blur-md py-4 dark:bg-gray-800/20">
        <div className="max-w-7xl mx-auto px-4 text-center text-white/70 dark:text-gray-400">
          <p className="text-sm">
            💻 Создано для тех, кто хочет больше, чем просто работу
          </p>
        </div>
      </footer>
    </div>
  )
}
