import { useState, useEffect } from 'react'
import { useAuthStore } from '../stores/authStore'
import { Sidebar } from '../components/admin/Sidebar'
import { api } from '../services/api'
import { toast } from '../stores/toastStore'

interface User {
  id: number
  email: string
  is_admin: boolean
  created_at: string
}

export default function AdminUsers() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [deleteConfirm, setDeleteConfirm] = useState<number | null>(null)
  const { isAuthenticated, isLoading } = useAuthStore()

  useEffect(() => {
    // Ждём завершения инициализации сессии
    if (!isLoading && isAuthenticated) {
      loadUsers()
    } else if (!isLoading && !isAuthenticated) {
      // Не аутентифицирован - не загружаем
      setLoading(false)
    }
  }, [isAuthenticated, isLoading])

  const loadUsers = async () => {
    setLoading(true)
    try {
      // Проверка токена
      const token = typeof window !== 'undefined' ? window.sessionStorage.getItem('auth_token') : null
      console.log('[AdminUsers] loadUsers, token exists:', !!token)
      
      const response = await api.get('/users/')
      console.log('[AdminUsers] Users loaded:', response.data)
      setUsers(response.data)
    } catch (error) {
      console.error('Failed to load users:', error)
      toast.error('Не удалось загрузить пользователей')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (userId: number) => {
    try {
      await api.delete(`/users/${userId}`)
      toast.success('Пользователь удален')
      setUsers(users.filter(u => u.id !== userId))
      setDeleteConfirm(null)
    } catch (error) {
      console.error('Failed to delete user:', error)
      toast.error('Не удалось удалить пользователя')
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="lg:ml-64">
        {/* Header */}
        <header className="bg-white shadow-sm border-b sticky top-0 z-10">
          <div className="px-6 py-4 flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">👥 Пользователи</h1>
              <p className="text-sm text-gray-500 mt-1">Управление пользователями системы</p>
            </div>
            <div className="flex items-center gap-3">
              <span className="px-3 py-1.5 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium">
                {users.length} пользователей
              </span>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="p-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center">
                  <span className="text-2xl">👥</span>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Всего пользователей</p>
                  <p className="text-2xl font-bold text-gray-900">{users.length}</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
                  <span className="text-2xl">👑</span>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Администраторы</p>
                  <p className="text-2xl font-bold text-gray-900">{users.filter(u => u.is_admin).length}</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                  <span className="text-2xl">👤</span>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Обычные пользователи</p>
                  <p className="text-2xl font-bold text-gray-900">{users.filter(u => !u.is_admin).length}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Users Table */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-100">
              <h3 className="text-lg font-semibold text-gray-900">Список пользователей</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Пользователь
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Роль
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Дата регистрации
                    </th>
                    <th className="px-6 py-4 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Действия
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {loading ? (
                    <tr>
                      <td colSpan={4} className="px-6 py-12 text-center">
                        <div className="flex items-center justify-center gap-2 text-gray-500">
                          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                          </svg>
                          Загрузка...
                        </div>
                      </td>
                    </tr>
                  ) : users.length === 0 ? (
                    <tr>
                      <td colSpan={4} className="px-6 py-12 text-center">
                        <div className="text-gray-400 text-4xl mb-3">📭</div>
                        <p className="text-gray-500">Пользователи не найдены</p>
                      </td>
                    </tr>
                  ) : (
                    users.map((user) => (
                      <tr key={user.id} className="hover:bg-gray-50 transition-colors">
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center">
                              <span className="text-white font-bold">
                                {user.email.charAt(0).toUpperCase()}
                              </span>
                            </div>
                            <div>
                              <p className="font-medium text-gray-900">{user.email}</p>
                              <p className="text-sm text-gray-500">ID: {user.id}</p>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          {user.is_admin ? (
                            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-700">
                              <span>👑</span> Администратор
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                              <span>👤</span> Пользователь
                            </span>
                          )}
                        </td>
                        <td className="px-6 py-4">
                          <span className="text-sm text-gray-600">
                            {formatDate(user.created_at)}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-right">
                          {deleteConfirm === user.id ? (
                            <div className="flex items-center justify-end gap-2">
                              <span className="text-sm text-red-600">Удалить?</span>
                              <button
                                onClick={() => handleDelete(user.id)}
                                className="px-3 py-1.5 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700"
                              >
                                Да
                              </button>
                              <button
                                onClick={() => setDeleteConfirm(null)}
                                className="px-3 py-1.5 bg-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-300"
                              >
                                Нет
                              </button>
                            </div>
                          ) : (
                            <button
                              onClick={() => setDeleteConfirm(user.id)}
                              disabled={user.email === 'admin@example.com'}
                              className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
                              title="Удалить пользователя"
                            >
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
