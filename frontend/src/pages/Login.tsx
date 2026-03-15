import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore, User } from '../stores/authStore'
import { authApi } from '../services/api'
import { loginSchema, LoginFormData } from '../utils/validation'

export default function Login() {
  const navigate = useNavigate()
  const login = useAuthStore((state) => state.login)
  const [localError, setLocalError] = useState('')

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginFormData) => {
    setLocalError('')
    try {
      const loginResponse = await authApi.login(data.email, data.password)
      const accessToken = loginResponse.access_token

      // ПРЯМО сохраняем токен в sessionStorage СРАЗУ
      // Это нужно чтобы interceptor мог использовать токен для getCurrentUser()
      if (typeof window !== 'undefined') {
        window.sessionStorage.setItem('auth_token', accessToken)
      }

      // Теперь получаем полные данные пользователя с токеном
      const userInfo: User = await authApi.getCurrentUser()
      
      // Сохраняем пользователя в sessionStorage и обновляем store
      if (typeof window !== 'undefined') {
        window.sessionStorage.setItem('auth_user', JSON.stringify(userInfo))
      }
      login(accessToken, userInfo)

      console.log('[Login] Successfully logged in, navigating to home')
      navigate('/')
    } catch (err: any) {
      console.error('[Login] Login error:', err)
      setLocalError(err?.response?.data?.detail || err?.message || 'Ошибка входа')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md border border-gray-200">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl mb-4 shadow-lg">
            <span className="text-3xl">🔐</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            С возвращением!
          </h1>
          <p className="text-gray-600">
            Войдите для продолжения подготовки
          </p>
        </div>

        {localError && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded mb-6">
            <div className="flex items-start">
              <span className="text-red-500 mr-2">⚠️</span>
              <span className="text-red-700 text-sm">{localError}</span>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
              type="email"
              {...register('email')}
              className={`w-full px-4 py-3 rounded-lg border ${
                errors.email
                  ? 'border-red-500 focus:border-red-600'
                  : 'border-gray-300 focus:border-indigo-500'
              } bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all`}
              placeholder="you@example.com"
              autoComplete="email"
            />
            {errors.email && (
              <p className="mt-2 text-sm text-red-600 flex items-center gap-1">
                <span>⚠️</span>
                {errors.email.message}
              </p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Пароль
            </label>
            <input
              type="password"
              {...register('password')}
              className={`w-full px-4 py-3 rounded-lg border ${
                errors.password
                  ? 'border-red-500 focus:border-red-600'
                  : 'border-gray-300 focus:border-indigo-500'
              } bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all`}
              placeholder="••••••••"
              autoComplete="current-password"
            />
            {errors.password && (
              <p className="mt-2 text-sm text-red-600 flex items-center gap-1">
                <span>⚠️</span>
                {errors.password.message}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isSubmitting ? (
              <>
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Вход...
              </>
            ) : (
              <>
                <span>🚀</span>
                Войти
              </>
            )}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Нет аккаунта?{' '}
            <Link
              to="/register"
              className="text-indigo-600 font-semibold hover:underline"
            >
              Зарегистрироваться
            </Link>
          </p>
        </div>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="text-center">
            <p className="text-xs text-gray-500">
              Тестовый аккаунт: admin@example.com / admin123
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
