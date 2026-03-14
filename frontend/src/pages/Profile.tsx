import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import { progressApi, interviewsApi, professionsApi } from '../services/api'
import { InterviewConfig, Profession } from '../types'

interface UserProgress {
  xp: number
  level: number
  level_name: string
  level_progress: number
  title: string
  stats: {
    total_sessions: number
    completed_sessions: number
    total_correct: number
    total_answered: number
    best_streak: number
  }
  achievements: Array<{
    id: number
    name: string
    description: string
    icon: string
    xp_reward: number
    unlocked: boolean
  }>
}

export default function Profile() {
  const navigate = useNavigate()
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  const logout = useAuthStore((state) => state.logout)
  const [progress, setProgress] = useState<UserProgress | null>(null)
  const [loading, setLoading] = useState(true)
  const [savedConfigs, setSavedConfigs] = useState<InterviewConfig[]>([])
  const [professions, setProfessions] = useState<Record<number, string>>({})

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login')
      return
    }
    loadProgress()
    loadSavedConfigs()

    // Обновляем прогресс при возврате на страницу (фокус окна)
    const handleFocus = () => {
      loadProgress()
      loadSavedConfigs()
    }
    window.addEventListener('focus', handleFocus)
    return () => window.removeEventListener('focus', handleFocus)
  }, [])

  const loadProgress = async () => {
    try {
      // Сначала пробуем получить из localStorage (если есть свежий прогресс)
      const cachedProgress = localStorage.getItem('userProgress')
      if (cachedProgress) {
        try {
          const parsed = JSON.parse(cachedProgress)
          // Проверяем что это валидный объект с прогрессом
          if (parsed && parsed.xp !== undefined) {
            setProgress(parsed)
          }
        } catch (e) {
          // Неверный формат, игнорируем
        }
      }

      // Затем загружаем актуальные данные с сервера
      const data = await progressApi.getMyProgress()
      setProgress(data)
      // Обновляем кэш
      localStorage.setItem('userProgress', JSON.stringify(data))
    } catch (error) {
      console.error('Failed to load progress:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadSavedConfigs = async () => {
    try {
      // Загружаем все профессии для маппинга
      const profs = await professionsApi.getAll()
      const profMap: Record<number, string> = {}
      ;(profs.items || profs).forEach((p: Profession) => {
        profMap[p.id] = p.name
      })
      setProfessions(profMap)

      // Загружаем конфигурации для всех профессий
      const allConfigs: InterviewConfig[] = []
      const professionIds = Object.keys(profMap).map(Number)
      
      for (const profId of professionIds) {
        try {
          const configs = await interviewsApi.getConfigsByProfession(profId)
          // Фильтруем только свои конфигурации
          const myConfigs = (configs || []).filter((c: InterviewConfig) => c.user_id !== null)
          allConfigs.push(...myConfigs)
        } catch (e) {
          // Игнорируем ошибки для отдельных профессий
        }
      }
      
      setSavedConfigs(allConfigs)
    } catch (error) {
      console.error('Failed to load saved configs:', error)
    }
  }

  const handleDeleteConfig = async (configId: number) => {
    if (!confirm('Удалить эту конфигурацию?')) return
    
    try {
      await interviewsApi.deleteConfig(configId)
      loadSavedConfigs()
    } catch (error) {
      console.error('Failed to delete config:', error)
      alert('Не удалось удалить конфигурацию')
    }
  }

  const handleStartFromConfig = async (configId: number) => {
    try {
      const result = await interviewsApi.createSessionFromConfig(configId)
      navigate(`/session/${result.session_id}`)
    } catch (error: any) {
      console.error('Failed to start session:', error)
      alert('Не удалось начать сессию')
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center">
        <div className="text-white text-2xl animate-pulse">🚀 Загрузка...</div>
      </div>
    )
  }

  if (!progress) return null

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 py-6 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <header className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-white/20 backdrop-blur-md rounded-xl flex items-center justify-center">
              <span className="text-2xl">🎮</span>
            </div>
            <h1 className="text-2xl font-bold text-white">Профиль</h1>
          </div>
          <button
            onClick={handleLogout}
            className="bg-white/20 backdrop-blur-md text-white px-4 py-2 rounded-xl hover:bg-white/30 transition-all"
          >
            Выйти
          </button>
        </header>

        {/* Level Card */}
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 mb-6">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-20 h-20 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-2xl flex items-center justify-center shadow-xl">
              <span className="text-4xl font-bold text-white">{progress.level}</span>
            </div>
            <div className="flex-1">
              <p className="text-white/70 text-sm uppercase tracking-wider">Ваш уровень</p>
              <p className="text-white font-bold text-2xl">{progress.level_name}</p>
              <p className="text-white/80 text-sm">{progress.title}</p>
            </div>
            <div className="text-right">
              <p className="text-white font-bold text-xl">{progress.xp} XP</p>
              <p className="text-white/70 text-sm">всего</p>
            </div>
          </div>
          
          <div className="relative h-4 bg-white/20 rounded-full overflow-hidden mb-2">
            <div
              className="absolute inset-y-0 left-0 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full transition-all duration-500"
              style={{ width: `${progress.level_progress}%` }}
            />
          </div>
          <p className="text-white/60 text-sm text-center">
            {progress.level_progress}% до следующего уровня
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-4">
            <p className="text-white/70 text-xs mb-1">Сессий</p>
            <p className="text-white font-bold text-2xl">{progress.stats.completed_sessions}</p>
          </div>
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-4">
            <p className="text-white/70 text-xs mb-1">Вопросов</p>
            <p className="text-white font-bold text-2xl">{progress.stats.total_answered}</p>
          </div>
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-4">
            <p className="text-white/70 text-xs mb-1">Правильно</p>
            <p className="text-white font-bold text-2xl">{progress.stats.total_correct}</p>
          </div>
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-4">
            <p className="text-white/70 text-xs mb-1">Серия</p>
            <p className="text-white font-bold text-2xl">🔥 {progress.stats.best_streak}</p>
          </div>
        </div>

        {/* Achievements */}
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 mb-6">
          <h2 className="text-xl font-bold text-white mb-4">🏆 Достижения</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {progress.achievements.map((ach) => (
              <div
                key={ach.id}
                className={`p-4 rounded-xl text-center transition-all ${
                  ach.unlocked
                    ? 'bg-gradient-to-br from-yellow-400/20 to-orange-500/20 border-2 border-yellow-400/50'
                    : 'bg-white/5 border-2 border-white/10 opacity-50'
                }`}
              >
                <div className="text-4xl mb-2">{ach.icon}</div>
                <p className="text-white font-bold text-sm mb-1">{ach.name}</p>
                <p className="text-white/70 text-xs mb-2">{ach.description}</p>
                {ach.unlocked ? (
                  <p className="text-yellow-400 text-xs font-semibold">+{ach.xp_reward} XP</p>
                ) : (
                  <p className="text-white/50 text-xs">🔒 Закрыто</p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Saved Interview Configs */}
        {savedConfigs.length > 0 && (
          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 mb-6">
            <h2 className="text-xl font-bold text-white mb-4">📋 Сохранённые собеседования</h2>
            <div className="grid md:grid-cols-2 gap-4">
              {savedConfigs.map((config) => (
                <div
                  key={config.id}
                  className="bg-white/5 rounded-xl p-4 border border-white/20 hover:border-yellow-400 transition-all"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h3 className="text-white font-bold text-base">{config.name}</h3>
                      <p className="text-white/60 text-xs">
                        {professions[config.profession_id] || 'Профессия'}
                      </p>
                    </div>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      config.difficulty === 'intern' ? 'bg-green-500' :
                      config.difficulty === 'junior' ? 'bg-blue-500' : 'bg-purple-500'
                    } text-white`}>
                      {config.difficulty === 'intern' ? '🌱' :
                       config.difficulty === 'junior' ? '📚' : '💼'}
                    </span>
                  </div>
                  
                  <div className="flex flex-wrap gap-1 mb-3">
                    {config.category_configs.slice(0, 3).map((cat, idx) => (
                      <span key={idx} className="text-white/70 text-xs bg-white/10 px-2 py-0.5 rounded">
                        {cat.question_count} вопр.
                      </span>
                    ))}
                    {config.category_configs.length > 3 && (
                      <span className="text-white/50 text-xs">+{config.category_configs.length - 3}</span>
                    )}
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => handleStartFromConfig(config.id)}
                      className="flex-1 bg-yellow-400/20 text-yellow-300 py-2 rounded-lg text-xs font-bold hover:bg-yellow-400/30 transition-all"
                    >
                      ▶️ Начать
                    </button>
                    <button
                      onClick={() => handleDeleteConfig(config.id)}
                      className="px-3 bg-red-500/20 text-red-300 py-2 rounded-lg text-xs font-bold hover:bg-red-500/30 transition-all"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Back to Home */}
        <div className="mt-6 text-center">
          <button
            onClick={() => navigate('/')}
            className="bg-white/20 backdrop-blur-md text-white px-6 py-3 rounded-xl font-bold hover:bg-white/30 transition-all"
          >
            ← На главную
          </button>
        </div>
      </div>
    </div>
  )
}
