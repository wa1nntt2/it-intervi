import { useState, useEffect } from 'react'
import { Sidebar } from '../components/admin/Sidebar'
import { StatCard } from '../components/admin/StatCard'
import { sessionsApi, professionsApi } from '../services/api'
import { Profession } from '../types'

interface Session {
  id: number
  profession_id: number
  profession_name: string
  user_id: number | null
  user_email: string | null
  question_ids: number[]
  status: 'active' | 'completed' | 'failed'
  score: number
  created_at: string
  completed_at: string | null
}

interface SessionStats {
  total: number
  active: number
  completed: number
  failed: number
  average_score: number
  today_sessions: number
  this_week_sessions: number
  this_month_sessions: number
}

export default function AdminSessions() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sessions, setSessions] = useState<Session[]>([])
  const [stats, setStats] = useState<SessionStats | null>(null)
  const [professions, setProfessions] = useState<Profession[]>([])
  const [loading, setLoading] = useState(true)

  // Фильтры
  const [selectedStatus, setSelectedStatus] = useState<string>('')
  const [selectedProfession, setSelectedProfession] = useState<string>('')
  const [dateFrom, setDateFrom] = useState<string>('')
  const [dateTo, setDateTo] = useState<string>('')

  // Пагинация
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 15

  useEffect(() => {
    loadStats()
    loadSessions()
    loadProfessions()
  }, [selectedStatus, selectedProfession, dateFrom, dateTo])

  const loadStats = async () => {
    try {
      const data = await sessionsApi.getStats()
      setStats(data)
    } catch (error) {
      console.error('Failed to load stats:', error)
    }
  }

  const loadSessions = async () => {
    setLoading(true)
    try {
      const filters: any = {}
      if (selectedStatus) filters.status = selectedStatus
      if (selectedProfession) filters.profession_id = parseInt(selectedProfession)
      if (dateFrom) filters.date_from = dateFrom
      if (dateTo) filters.date_to = dateTo
      const response = await sessionsApi.getAll(filters)
      // API теперь возвращает { items: [...], meta: {...} }
      const sessionsData = response.items || response
      setSessions(sessionsData)
    } catch (error) {
      console.error('Failed to load sessions:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadProfessions = async () => {
    const response = await professionsApi.getAll()
    // API теперь возвращает { items: [...], meta: {...} }
    const data = response.items || response
    setProfessions(data)
  }

  const handleDeleteSession = async (id: number) => {
    if (!confirm('Вы уверены, что хотите удалить эту сессию?')) return
    try {
      await sessionsApi.delete(id)
      loadSessions()
      loadStats()
    } catch (error) {
      console.error('Failed to delete session:', error)
    }
  }

  const getStatusBadge = (status: string) => {
    const colors: Record<string, string> = {
      active: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
    }
    const labels: Record<string, string> = {
      active: 'Активна',
      completed: 'Завершена',
      failed: 'Провалена',
    }
    return (
      <span className={`px-3 py-1 rounded-full text-xs font-medium ${colors[status]}`}>
        {labels[status]}
      </span>
    )
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  // Фильтрация и пагинация
  const filteredSessions = sessions
  const totalPages = Math.ceil(filteredSessions.length / itemsPerPage)
  const paginatedSessions = filteredSessions.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  )

  // Экспорт в CSV
  const handleExportCSV = () => {
    const headers = ['ID', 'Профессия', 'Пользователь', 'Статус', 'Оценка', 'Дата создания', 'Дата завершения']
    const rows = sessions.map(s => [
      s.id,
      s.profession_name,
      s.user_email || 'Аноним',
      s.status,
      s.score,
      s.created_at,
      s.completed_at || ''
    ])
    
    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n')
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `sessions_${new Date().toISOString().split('T')[0]}.csv`
    link.click()
  }

  const resetFilters = () => {
    setSelectedStatus('')
    setSelectedProfession('')
    setDateFrom('')
    setDateTo('')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="lg:ml-64">
        {/* Верхняя панель */}
        <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
          <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden text-gray-500 hover:text-gray-700"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">⏱️ Сессии</h1>
                <p className="text-sm text-gray-500 mt-1">Управление сессиями</p>
              </div>
            </div>

            <button
              onClick={handleExportCSV}
              className="flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 shadow-md transition-all"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span className="font-medium">Экспорт CSV</span>
            </button>
          </div>
        </header>

        <main className="p-6">
          {/* Статистика */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
              <StatCard
                title="Всего сессий"
                value={stats.total}
                icon={
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                }
                color="indigo"
                subtitle={`+${stats.today_sessions} сегодня`}
              />
              <StatCard
                title="Активные"
                value={stats.active}
                icon={
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                }
                color="blue"
              />
              <StatCard
                title="Завершенные"
                value={stats.completed}
                icon={
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                }
                color="green"
                subtitle={`${stats.average_score}% средний балл`}
              />
              <StatCard
                title="Проваленные"
                value={stats.failed}
                icon={
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                }
                color="red"
              />
            </div>
          )}

          {/* Дополнительная статистика */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white shadow-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-blue-100 text-sm font-medium">За сегодня</span>
                  <svg className="w-5 h-5 text-blue-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <p className="text-3xl font-bold">{stats.today_sessions}</p>
                <p className="text-blue-200 text-sm mt-1">сессий сегодня</p>
              </div>

              <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-6 text-white shadow-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-purple-100 text-sm font-medium">За неделю</span>
                  <svg className="w-5 h-5 text-purple-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <p className="text-3xl font-bold">{stats.this_week_sessions}</p>
                <p className="text-purple-200 text-sm mt-1">сессий за 7 дней</p>
              </div>

              <div className="bg-gradient-to-br from-pink-500 to-pink-600 rounded-2xl p-6 text-white shadow-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-pink-100 text-sm font-medium">За месяц</span>
                  <svg className="w-5 h-5 text-pink-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <p className="text-3xl font-bold">{stats.this_month_sessions}</p>
                <p className="text-pink-200 text-sm mt-1">сессий за 30 дней</p>
              </div>
            </div>
          )}

          {/* Фильтры */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 mb-6 p-5">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
                <h3 className="text-lg font-semibold text-gray-900">Фильтры</h3>
              </div>
              {(selectedStatus || selectedProfession || dateFrom || dateTo) && (
                <button
                  onClick={resetFilters}
                  className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
                >
                  ✕ Сбросить
                </button>
              )}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <select
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
              >
                <option value="">Все статусы</option>
                <option value="active">🔵 Активные</option>
                <option value="completed">🟢 Завершенные</option>
                <option value="failed">🔴 Проваленные</option>
              </select>
              <select
                value={selectedProfession}
                onChange={(e) => setSelectedProfession(e.target.value)}
                className="px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
              >
                <option value="">Все профессии</option>
                {professions.map((p) => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>
              <input
                type="date"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                className="px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
              <input
                type="date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                className="px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Таблица сессий */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
              <h3 className="text-lg font-semibold text-gray-900">Список сессий</h3>
              <span className="text-sm text-gray-500">
                {filteredSessions.length} сессий
              </span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      ID
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Профессия
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Пользователь
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Статус
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Оценка
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Дата создания
                    </th>
                    <th className="px-6 py-4 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Действия
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {loading ? (
                    <tr>
                      <td colSpan={7} className="px-6 py-8 text-center text-gray-500">
                        <div className="flex items-center justify-center gap-2">
                          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                          </svg>
                          Загрузка...
                        </div>
                      </td>
                    </tr>
                  ) : filteredSessions.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="px-6 py-12 text-center">
                        <div className="text-gray-400 mb-2">📭</div>
                        <p className="text-gray-500">Сессии не найдены</p>
                      </td>
                    </tr>
                  ) : (
                    paginatedSessions.map((session) => (
                      <tr key={session.id} className="hover:bg-gray-50 transition-colors">
                        <td className="px-6 py-4">
                          <span className="text-sm font-mono text-gray-600">#{session.id}</span>
                        </td>
                        <td className="px-6 py-4">
                          <span className="text-sm font-medium text-gray-900">{session.profession_name}</span>
                        </td>
                        <td className="px-6 py-4">
                          {session.user_email ? (
                            <span className="text-sm text-gray-600">{session.user_email}</span>
                          ) : (
                            <span className="text-sm text-gray-400 italic">Аноним</span>
                          )}
                        </td>
                        <td className="px-6 py-4">
                          {getStatusBadge(session.status)}
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-2">
                            <div className="w-24 bg-gray-200 rounded-full h-2">
                              <div
                                className={`h-2 rounded-full ${
                                  (session.score / session.question_ids.length * 100) >= 80 ? 'bg-green-500' :
                                  (session.score / session.question_ids.length * 100) >= 50 ? 'bg-yellow-500' : 'bg-red-500'
                                }`}
                                style={{ width: `${(session.score / session.question_ids.length * 100).toFixed(0)}%` }}
                              />
                            </div>
                            <span className="text-sm font-medium text-gray-700">
                              {session.score}/{session.question_ids.length} ({(session.score / session.question_ids.length * 100).toFixed(1)}%)
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <span className="text-sm text-gray-600">{formatDate(session.created_at)}</span>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <div className="flex justify-end gap-2">
                            <button
                              onClick={() => handleDeleteSession(session.id)}
                              className="text-red-600 hover:text-red-900 hover:bg-red-50 p-2 rounded-lg transition-colors"
                              title="Удалить"
                            >
                              🗑️
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

            {/* Пагинация */}
            {totalPages > 1 && (
              <div className="px-6 py-4 border-t border-gray-100 flex items-center justify-between bg-gray-50">
                <p className="text-sm text-gray-500">
                  Показано <span className="font-medium text-gray-900">{(currentPage - 1) * itemsPerPage + 1}</span> -{' '}
                  <span className="font-medium text-gray-900">{Math.min(currentPage * itemsPerPage, filteredSessions.length)}</span> из{' '}
                  <span className="font-medium text-gray-900">{filteredSessions.length}</span>
                </p>
                <div className="flex gap-2">
                  <button
                    onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                    disabled={currentPage === 1}
                    className="px-4 py-2 border border-gray-200 rounded-lg hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    ← Назад
                  </button>
                  <span className="px-4 py-2 text-gray-500 bg-white border border-gray-200 rounded-lg">
                    {currentPage} / {totalPages}
                  </span>
                  <button
                    onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                    disabled={currentPage === totalPages}
                    className="px-4 py-2 border border-gray-200 rounded-lg hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Вперед →
                  </button>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}
