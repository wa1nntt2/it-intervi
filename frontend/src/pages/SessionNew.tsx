import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { professionsApi, sessionsApi, progressApi } from '../services/api'
import { Profession } from '../types'

type Difficulty = 'intern' | 'junior' | 'middle'

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
  const [selectedProfession, setSelectedProfession] = useState<number | null>(null)
  const [selectedDifficulty, setSelectedDifficulty] = useState<Difficulty | null>(null)
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)
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

  const handleStart = async () => {
    if (!selectedProfession || !selectedDifficulty) return
    setCreating(true)
    try {
      const session = await sessionsApi.create(selectedProfession, selectedDifficulty)
      navigate(`/session/${session.id}`)
    } catch (err) {
      console.error('Failed to create session', err)
    } finally {
      setCreating(false)
    }
  }

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

  const getDifficultyConfig = (difficulty: Difficulty) => {
    const configs: Record<Difficulty, { bg: string; text: string; label: string; icon: string; description: string }> = {
      'intern': { 
        bg: 'from-green-400 to-emerald-500', 
        text: 'text-green-700', 
        label: 'Intern', 
        icon: '🌱',
        description: 'Базовые вопросы для начинающих'
      },
      'junior': { 
        bg: 'from-blue-400 to-cyan-500', 
        text: 'text-blue-700', 
        label: 'Junior', 
        icon: '📚',
        description: 'Вопросы для начального уровня'
      },
      'middle': { 
        bg: 'from-purple-500 to-pink-500', 
        text: 'text-purple-700', 
        label: 'Middle', 
        icon: '💼',
        description: 'Продвинутые вопросы для опытных'
      }
    }
    return configs[difficulty]
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
            Настройте сессию
          </h1>
          <p className="text-base text-white/90">
            Выберите профессию и сложность
          </p>
        </div>

        {/* Step 1: Professions */}
        <div className="mb-4">
          <div className="flex items-center gap-2 mb-3">
            <span className="w-7 h-7 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center text-white font-bold text-sm">1</span>
            <h2 className="text-lg font-bold text-white">Выберите профессию</h2>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {professions.map((profession) => (
              <div
                key={profession.id}
                onClick={() => setSelectedProfession(profession.id)}
                className={`group relative overflow-hidden rounded-xl cursor-pointer transition-all duration-300 hover:scale-105 ${
                  selectedProfession === profession.id
                    ? 'ring-2 ring-yellow-400 shadow-xl shadow-yellow-400/50'
                    : 'hover:shadow-lg'
                }`}
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${getProfessionGradient(profession.name)} opacity-90 group-hover:opacity-100 transition-opacity`} />
                <div className="relative p-3 text-white">
                  <div className="flex items-start gap-2">
                    <div className="text-2xl">{getProfessionIcon(profession.name)}</div>
                    <div className="flex-1">
                      <h3 className="text-sm font-bold mb-1">{profession.name}</h3>
                      {profession.description && (
                        <p className="text-white/90 text-xs leading-tight line-clamp-2">
                          {profession.description}
                        </p>
                      )}
                    </div>
                    <div className={`transition-all duration-300 ${
                      selectedProfession === profession.id ? 'opacity-100 scale-100' : 'opacity-0 scale-75'
                    }`}>
                      <div className="w-6 h-6 bg-yellow-400 rounded-full flex items-center justify-center">
                        <span className="text-indigo-600 text-sm font-bold">✓</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="absolute inset-0 bg-white/0 group-hover:bg-white/10 transition-colors" />
              </div>
            ))}
          </div>
        </div>

        {/* Step 2: Difficulty */}
        <div className="mb-4">
          <div className="flex items-center gap-2 mb-3">
            <span className="w-7 h-7 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center text-white font-bold text-sm">2</span>
            <h2 className="text-lg font-bold text-white">Выберите сложность</h2>
          </div>
          <div className="grid grid-cols-3 gap-3">
            {(['intern', 'junior', 'middle'] as Difficulty[]).map((difficulty) => {
              const config = getDifficultyConfig(difficulty)
              return (
                <div
                  key={difficulty}
                  onClick={() => setSelectedDifficulty(difficulty)}
                  className={`group relative overflow-hidden rounded-xl cursor-pointer transition-all duration-300 hover:scale-105 ${
                    selectedDifficulty === difficulty
                      ? 'ring-2 ring-yellow-400 shadow-xl shadow-yellow-400/50'
                      : 'hover:shadow-lg'
                  }`}
                >
                  <div className={`absolute inset-0 bg-gradient-to-br ${config.bg} opacity-90 group-hover:opacity-100 transition-opacity`} />
                  <div className="relative p-3 text-white text-center">
                    <div className="text-2xl mb-1">{config.icon}</div>
                    <h3 className="text-sm font-bold mb-0.5">{config.label}</h3>
                    <p className="text-white/90 text-xs">{config.description}</p>
                  </div>
                  <div className={`absolute top-1 right-1 transition-all duration-300 ${
                    selectedDifficulty === difficulty ? 'opacity-100 scale-100' : 'opacity-0 scale-75'
                  }`}>
                    <div className="w-5 h-5 bg-yellow-400 rounded-full flex items-center justify-center">
                      <span className="text-indigo-600 text-xs font-bold">✓</span>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <button
            onClick={handleStart}
            disabled={!selectedProfession || !selectedDifficulty || creating}
            className="group bg-white text-indigo-600 px-6 py-3 rounded-xl font-bold text-base hover:bg-yellow-300 transition-all hover:scale-105 shadow-xl disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
          >
            {creating ? (
              <>
                <span className="animate-spin">⏳</span>
                Создание...
              </>
            ) : (
              <>
                <span>🚀</span>
                Начать сессию
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </>
            )}
          </button>
          <button
            onClick={() => navigate('/')}
            className="bg-white/20 backdrop-blur-sm text-white border-2 border-white/50 px-6 py-3 rounded-xl font-bold text-base hover:bg-white/30 transition-all hover:scale-105"
          >
            ← Назад
          </button>
        </div>

        {/* Selected Info */}
        {(selectedProfession || selectedDifficulty) && (
          <div className="mt-4 text-center">
            <div className="inline-block bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
              <p className="text-white/80 text-xs">
                <span className="font-bold text-yellow-300">
                  {selectedProfession ? professions.find(p => p.id === selectedProfession)?.name : 'Профессия не выбрана'}
                </span>
              </p>
              {selectedDifficulty && (
                <p className="text-white/80 text-xs">
                  Уровень: <span className="font-bold text-yellow-300">{getDifficultyConfig(selectedDifficulty).label}</span>
                </p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
