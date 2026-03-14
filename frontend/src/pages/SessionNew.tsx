import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { professionsApi, progressApi } from '../services/api'
import { Profession } from '../types'

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
  }
}

export default function SessionNew() {
  const navigate = useNavigate()
  const [professions, setProfessions] = useState<Profession[]>([])
  const [loading, setLoading] = useState(true)
  const [userProgress, setUserProgress] = useState<UserProgress | null>(null)

  useEffect(() => {
    const abortController = new AbortController()

    const loadData = async () => {
      try {
        const [professionsResponse, progressData] = await Promise.all([
          professionsApi.getAll(),
          progressApi.getMyProgress().catch(() => null)
        ])

        if (abortController.signal.aborted) return

        // API теперь возвращает { items: [...], meta: {...} }
        const professionsData = professionsResponse.items || professionsResponse
        setProfessions(professionsData)
        if (progressData) setUserProgress(progressData)
      } catch (err) {
        if (abortController.signal.aborted) return
        console.error('Failed to load data', err)
      } finally {
        if (!abortController.signal.aborted) {
          setLoading(false)
        }
      }
    }

    loadData()

    return () => {
      abortController.abort()
    }
  }, [])

  const getProfessionIcon = (name: string) => {
    const icons: Record<string, string> = {
      'Frontend': '🎨',
      'Backend': '⚙️',
      'Fullstack': '🚀',
      'DevOps': '🔧'
    }
    return icons[name.split(' ')[0]] || '💻'
  }

  const getProfessionGradient = (name: string) => {
    const gradients: Record<string, string> = {
      'Frontend': 'from-pink-500 to-rose-500',
      'Backend': 'from-blue-500 to-cyan-500',
      'Fullstack': 'from-purple-500 to-pink-500',
      'DevOps': 'from-orange-500 to-amber-500'
    }
    return gradients[name.split(' ')[0]] || 'from-gray-500 to-slate-500'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center">
        <div className="text-white text-2xl animate-pulse">🚀 Загрузка...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 py-6 px-3">
      <div className="max-w-4xl mx-auto">
        {/* Header с уровнем пользователя */}
        <div className="mb-4">
          {userProgress ? (
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-3 mb-4">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg flex items-center justify-center shadow-lg">
                    <span className="text-lg font-bold text-white">{userProgress.level}</span>
                  </div>
                  <div>
                    <p className="text-white/70 text-xs uppercase tracking-wider">Ваш уровень</p>
                    <p className="text-white font-bold text-base">{userProgress.level_name}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-white/70 text-xs">{userProgress.xp} XP</p>
                  <p className="text-white font-semibold text-sm">{userProgress.title}</p>
                </div>
              </div>
              <div className="relative h-2 bg-white/20 rounded-full overflow-hidden">
                <div
                  className="absolute inset-y-0 left-0 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full transition-all duration-500"
                  style={{ width: `${userProgress.level_progress}%` }}
                />
              </div>
              <p className="text-white/60 text-xs mt-1">
                {userProgress.level_progress}% до следующего уровня
              </p>
            </div>
          ) : (
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-3 mb-4 text-center">
              <p className="text-white/80 text-sm">🎮 Пройдите первую сессию чтобы получить уровень!</p>
            </div>
          )}
        </div>

        {/* Header */}
        <div className="text-center mb-6">
          <div className="inline-block mb-2 animate-bounce">
            <span className="bg-white/20 backdrop-blur-sm text-white px-3 py-1 rounded-full text-xs font-medium">
              🎯 Подготовка к сессии
            </span>
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white mb-2">
            Выберите профессию
          </h1>
          <p className="text-base text-white/90">
            После выбора вы сможете настроить темы и количество вопросов
          </p>
        </div>

        {/* Professions Grid */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          {professions.map((profession) => (
            <div
              key={profession.id}
              onClick={() => navigate(`/interview/${profession.id}/setup`)}
              className={`group relative overflow-hidden rounded-xl cursor-pointer transition-all duration-300 hover:scale-105 hover:shadow-xl`}
            >
              <div className={`absolute inset-0 bg-gradient-to-br ${getProfessionGradient(profession.name)} opacity-90 group-hover:opacity-100 transition-opacity`} />
              <div className="relative p-4 text-white">
                <div className="flex items-start gap-3">
                  <div className="text-3xl">{getProfessionIcon(profession.name)}</div>
                  <div className="flex-1">
                    <h3 className="text-base font-bold mb-1">{profession.name}</h3>
                    {profession.description && (
                      <p className="text-white/90 text-xs leading-tight line-clamp-2">
                        {profession.description}
                      </p>
                    )}
                  </div>
                </div>
              </div>
              <div className="absolute inset-0 bg-white/0 group-hover:bg-white/10 transition-colors" />
            </div>
          ))}
        </div>

        {/* Info */}
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 text-center">
          <p className="text-white/80 text-sm">
            👈 Выберите профессию чтобы настроить собеседование
          </p>
          <p className="text-white/60 text-xs mt-2">
            Вы сможете выбрать темы, количество вопросов и уровень сложности
          </p>
        </div>
      </div>
    </div>
  )
}
