import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore, User } from '../stores/authStore'
import { authApi } from '../services/api'

export default function Register() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const login = useAuthStore((state) => state.login)
  const navigate = useNavigate()

  const validatePassword = (pwd: string): string | null => {
    if (pwd.length < 8) {
      return 'Пароль должен содержать минимум 8 символов'
    }
    if (!/[A-Z]/.test(pwd)) {
      return 'Пароль должен содержать хотя бы одну заглавную букву'
    }
    if (!/[a-z]/.test(pwd)) {
      return 'Пароль должен содержать хотя бы одну строчную букву'
    }
    if (!/\d/.test(pwd)) {
      return 'Пароль должен содержать хотя бы одну цифру'
    }
    return null
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    if (password !== confirmPassword) {
      setError('Пароли не совпадают')
      return
    }
    
    const passwordError = validatePassword(password)
    if (passwordError) {
      setError(passwordError)
      return
    }
    
    setLoading(true)
    try {
      await authApi.register(email, password)
      const loginResponse = await authApi.login(email, password)
      const accessToken = loginResponse.access_token
      
      // Получаем информацию о пользователе
      const userInfo: User = await authApi.getCurrentUser()
      
      // Сохраняем токен и данные пользователя в store
      login(accessToken, userInfo)
      navigate('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка регистрации')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-bold text-gray-900 mb-6 text-center">Регистрация</h1>
        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>
        )}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-indigo-500"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Пароль</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-indigo-500"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              Минимум 8 символов, заглавная буква, строчная буква и цифра
            </p>
          </div>
          <div className="mb-6">
            <label className="block text-gray-700 mb-2">Подтвердите пароль</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-indigo-500"
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 disabled:opacity-50"
          >
            {loading ? 'Регистрация...' : 'Зарегистрироваться'}
          </button>
        </form>
        <p className="mt-4 text-center text-gray-600">
          Уже есть аккаунт?{' '}
          <Link to="/login" className="text-indigo-600 hover:underline">
            Войти
          </Link>
        </p>
      </div>
    </div>
  )
}
