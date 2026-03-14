import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import { progressApi, sessionsApi, questionsApi } from '../services/api'
import { Session, Question } from '../types'

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

interface SessionHistory extends Session {
  profession_name: string
  percentage: number
}

interface WrongAnswer {
  question_id: number
  question_text: string
  your_answer: string
  correct_answer: string
  explanation?: string
  category?: string
}

export default function Profile() {
  const navigate = useNavigate()
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  const logout = useAuthStore((state) => state.logout)
  const [progress, setProgress] = useState<UserProgress | null>(null)
  const [loading, setLoading] = useState(true)
  const [sessionHistory, setSessionHistory] = useState<SessionHistory[]>([])
  const [wrongAnswers, setWrongAnswers] = useState<WrongAnswer[]>([])
  const [activeTab, setActiveTab] = useState<'overview' | 'history' | 'mistakes'>('overview')

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login')
      return
    }
    loadProfileData()
  }, [])

  const loadProfileData = async () => {
    try {
      setLoading(true)
      const [progressData, sessionsData] = await Promise.all([
        progressApi.getMyProgress(),
        sessionsApi.getAll({ status: 'completed' })
      ])
      
      setProgress(progressData)
      
      // Загружаем историю сессий
      const sessionsWithDetails = await Promise.all(
        (sessionsData.items || sessionsData).slice(0, 10).map(async (s: Session) => {
          const profession = await fetch(`/api/professions/${s.profession_id}`).then(r => r.json())
          return {
            ...s,
            profession_name: profession.name,
            percentage: s.question_ids.length > 0 ? Math.round((s.score / s.question_ids.length) * 100) : 0
          }
        })
      )
      setSessionHistory(sessionsWithDetails)
      
      // Загружаем неправильные ответы
      await loadWrongAnswers()
      
    } catch (error) {
      console.error('Failed to load profile data:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadWrongAnswers = async () => {
    try {
      // Загружаем неправильные ответы через API
      const wrongData = await fetch('/api/progress/wrong-answers?limit=10', {
        headers: {
          'Authorization': `Bearer ${useAuthStore.getState().token}`
        }
      }).then(r => r.json())
      
      setWrongAnswers(wrongData || [])
    } catch (error) {
      console.error('Failed to load wrong answers:', error)
      setWrongAnswers([])
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center">
        <div className="text-white text-2xl animate-pulse">🚀 Загрузка профиля...</div>
      </div>
    )
  }

  if (!progress) return null

  const getLevelColor = (level: number) => {
    if (level < 5) return 'from-green-400 to-emerald-500'
    if (level < 10) return 'from-blue-400 to-cyan-500'
    if (level < 15) return 'from-purple-400 to-pink-500'
    return 'from-yellow-400 to-orange-500'
  }

  const getLevelTitle = (level: number) => {
    if (level < 5) return 'Новичок'
    if (level < 10) return 'Продвинутый'
    if (level < 15) return 'Эксперт'
    return 'Мастер'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 py-6 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate('/')}
              className="text-white/80 hover:text-white"
            >
              ← На главную
            </button>
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
            <div className={`w-24 h-24 bg-gradient-to-br ${getLevelColor(progress.level)} rounded-2xl flex items-center justify-center shadow-xl`}>
              <span className="text-5xl font-bold text-white">{progress.level}</span>
            </div>
            <div className="flex-1">
              <p className="text-white/70 text-sm uppercase tracking-wider">Ваш уровень</p>
              <p className="text-white font-bold text-3xl">{progress.level_name}</p>
              <p className="text-white/80 text-sm">{getLevelTitle(progress.level)} • {progress.title}</p>
            </div>
            <div className="text-right">
              <p className="text-white font-bold text-2xl">{progress.xp} XP</p>
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

        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeTab === 'overview'
                ? 'bg-white text-indigo-600'
                : 'bg-white/20 text-white hover:bg-white/30'
            }`}
          >
            📊 Обзор
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeTab === 'history'
                ? 'bg-white text-indigo-600'
                : 'bg-white/20 text-white hover:bg-white/30'
            }`}
          >
            📜 История сессий
          </button>
          <button
            onClick={() => setActiveTab('mistakes')}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeTab === 'mistakes'
                ? 'bg-white text-indigo-600'
                : 'bg-white/20 text-white hover:bg-white/30'
            }`}
          >
            ❌ Ошибки
          </button>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <>
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

            {/* Accuracy Card */}
            {progress.stats.total_answered > 0 && (
              <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 mb-6">
                <h3 className="text-lg font-bold text-white mb-4">📈 Точность ответов</h3>
                <div className="flex items-center gap-4">
                  <div className="flex-1">
                    <div className="relative h-6 bg-white/20 rounded-full overflow-hidden">
                      <div
                        className="absolute inset-y-0 left-0 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full transition-all duration-500"
                        style={{ width: `${(progress.stats.total_correct / progress.stats.total_answered) * 100}%` }}
                      />
                    </div>
                  </div>
                  <p className="text-white font-bold text-xl">
                    {Math.round((progress.stats.total_correct / progress.stats.total_answered) * 100)}%
                  </p>
                </div>
              </div>
            )}

            {/* Achievements */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6">
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
          </>
        )}

        {/* History Tab */}
        {activeTab === 'history' && (
          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6">
            <h2 className="text-xl font-bold text-white mb-4">📜 История сессий</h2>
            {sessionHistory.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">📭</div>
                <p className="text-white/80">У вас пока нет завершённых сессий</p>
                <button
                  onClick={() => navigate('/session/new')}
                  className="mt-4 bg-white text-indigo-600 px-6 py-3 rounded-lg font-bold hover:bg-yellow-300 transition-all"
                >
                  Начать первую сессию
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                {sessionHistory.map((session) => (
                  <div
                    key={session.id}
                    className="bg-white/5 rounded-xl p-4 border border-white/20 hover:border-yellow-400 transition-all"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div>
                        <h3 className="text-white font-bold">{session.profession_name}</h3>
                        <p className="text-white/60 text-xs">
                          {new Date(session.created_at).toLocaleDateString('ru-RU', {
                            day: 'numeric',
                            month: 'long',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </p>
                      </div>
                      <div className="text-right">
                        <div className={`text-2xl font-bold ${
                          session.percentage >= 80 ? 'text-green-400' :
                          session.percentage >= 60 ? 'text-yellow-400' : 'text-red-400'
                        }`}>
                          {session.percentage}%
                        </div>
                        <p className="text-white/60 text-xs">
                          {session.score}/{session.question_ids.length}
                        </p>
                      </div>
                    </div>
                    <div className="relative h-2 bg-white/20 rounded-full overflow-hidden">
                      <div
                        className={`absolute inset-y-0 left-0 rounded-full transition-all duration-500 ${
                          session.percentage >= 80 ? 'bg-green-400' :
                          session.percentage >= 60 ? 'bg-yellow-400' : 'bg-red-400'
                        }`}
                        style={{ width: `${session.percentage}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Mistakes Tab */}
        {activeTab === 'mistakes' && (
          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6">
            <h2 className="text-xl font-bold text-white mb-4">❌ Неправильные ответы</h2>
            {wrongAnswers.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🎉</div>
                <p className="text-white/80">Отлично! У вас нет ошибок в последних сессиях</p>
              </div>
            ) : (
              <div className="space-y-4">
                {wrongAnswers.map((answer, idx) => (
                  <div
                    key={idx}
                    className="bg-white/5 rounded-xl p-4 border border-white/20"
                  >
                    <div className="flex items-start gap-3 mb-3">
                      <span className="text-2xl">❌</span>
                      <div className="flex-1">
                        <p className="text-white font-medium mb-2">{answer.question_text}</p>
                        <div className="grid md:grid-cols-2 gap-3">
                          <div className="bg-red-500/20 border border-red-400/50 rounded-lg p-3">
                            <p className="text-red-300 text-xs mb-1">Ваш ответ:</p>
                            <p className="text-white text-sm">{answer.your_answer}</p>
                          </div>
                          <div className="bg-green-500/20 border border-green-400/50 rounded-lg p-3">
                            <p className="text-green-300 text-xs mb-1">Правильный ответ:</p>
                            <p className="text-white text-sm">{answer.correct_answer}</p>
                          </div>
                        </div>
                        {answer.explanation && (
                          <div className="mt-3 bg-blue-500/20 border border-blue-400/50 rounded-lg p-3">
                            <p className="text-blue-300 text-xs mb-1">💡 Пояснение:</p>
                            <p className="text-white/90 text-sm">{answer.explanation}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
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
