import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { interviewsApi, sessionsApi, professionsApi } from '../services/api'
import { Category, InterviewConfig, Profession } from '../types'
import { useAuthStore } from '../stores/authStore'

export default function InterviewSetup() {
  const { professionId } = useParams<{ professionId: string }>()
  const navigate = useNavigate()
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)

  const [profession, setProfession] = useState<Profession | null>(null)
  const [categories, setCategories] = useState<Category[]>([])
  const [savedConfigs, setSavedConfigs] = useState<InterviewConfig[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Состояние для создания новой конфигурации
  const [selectedCategories, setSelectedCategories] = useState<Record<number, number>>({})
  const [difficulty, setDifficulty] = useState<'intern' | 'junior' | 'middle'>('junior')
  const [configName, setConfigName] = useState('')
  const [showConfigForm, setShowConfigForm] = useState(false)

  useEffect(() => {
    const loadData = async () => {
      if (!professionId) return
      try {
        const [professionData, categoriesData, configsData] = await Promise.all([
          professionsApi.getById(parseInt(professionId)),
          interviewsApi.getCategoriesByProfession(parseInt(professionId)),
          isAuthenticated ? interviewsApi.getConfigsByProfession(parseInt(professionId)) : Promise.resolve([])
        ])
        setProfession(professionData)
        setCategories(categoriesData)
        setSavedConfigs(configsData || [])
      } catch (err: any) {
        console.error('Failed to load data', err)
        setError('Не удалось загрузить данные')
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [professionId, isAuthenticated])

  const handleCategoryToggle = (categoryId: number) => {
    setSelectedCategories((prev) => {
      const newSelected = { ...prev }
      if (newSelected[categoryId]) {
        delete newSelected[categoryId]
      } else {
        newSelected[categoryId] = 5 // По умолчанию 5 вопросов
      }
      return newSelected
    })
  }

  const handleQuestionCountChange = (categoryId: number, count: number) => {
    setSelectedCategories((prev) => ({
      ...prev,
      [categoryId]: Math.max(1, Math.min(20, count))
    }))
  }

  const handleSaveConfig = async () => {
    if (!configName.trim() || Object.keys(selectedCategories).length === 0) {
      setError('Введите название и выберите хотя бы одну категорию')
      return
    }

    try {
      await interviewsApi.createConfig({
        name: configName,
        profession_id: parseInt(professionId!),
        difficulty,
        category_configs: Object.entries(selectedCategories).map(([categoryId, count]) => ({
          category_id: parseInt(categoryId),
          question_count: count
        }))
      })
      // Перезагрузить список конфигураций
      const configsData = await interviewsApi.getConfigsByProfession(parseInt(professionId!))
      setSavedConfigs(configsData || [])
      setShowConfigForm(false)
      setConfigName('')
      setSelectedCategories({})
    } catch (err: any) {
      console.error('Failed to save config', err)
      setError('Не удалось сохранить конфигурацию')
    }
  }

  const handleStartFromConfig = async (configId: number) => {
    try {
      const result = await interviewsApi.createSessionFromConfig(configId)
      navigate(`/session/${result.session_id}`)
    } catch (err: any) {
      console.error('Failed to create session', err)
      setError(err.response?.data?.detail || 'Не удалось создать сессию')
    }
  }

  const handleQuickStart = async () => {
    if (Object.keys(selectedCategories).length === 0) {
      setError('Выберите хотя бы одну категорию')
      return
    }

    // Создаем сессию напрямую без сохранения конфигурации
    try {
      // Сначала создаём временную конфигурацию (но не сохраняем в БД)
      // API создаст сессию на основе переданных параметров
      const categoriesPayload = Object.entries(selectedCategories).map(([categoryId, count]) => ({
        category_id: parseInt(categoryId),
        question_count: count
      }))

      // Создаём временную конфигурацию только для создания сессии
      const tempConfig = await interviewsApi.createConfig({
        name: `Quick_${Date.now()}`,
        profession_id: parseInt(professionId!),
        difficulty,
        category_configs: categoriesPayload,
        is_public: false
      })

      // Создаем сессию из конфигурации
      const result = await interviewsApi.createSessionFromConfig(tempConfig.id)
      
      // Сразу удаляем временную конфигурацию
      await interviewsApi.deleteConfig(tempConfig.id).catch(() => {})
      
      navigate(`/session/${result.session_id}`)
    } catch (err: any) {
      console.error('Failed to start session', err)
      setError('Не удалось начать сессию')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center">
        <div className="text-white text-xs animate-pulse">🚀 Загрузка...</div>
      </div>
    )
  }

  if (error && !categories.length) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center">
        <div className="bg-white/10 backdrop-blur-md p-8 rounded-lg shadow-2xl text-center max-w-md">
          <div className="text-6xl mb-2">❌</div>
          <h1 className="text-xs font-bold text-white mb-2">Ошибка</h1>
          <p className="text-white/90 mb-2">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="bg-white text-indigo-600 px-6 py-3 rounded-lg font-bold hover:bg-yellow-300 transition-all hover:scale-105"
          >
            🏠 На главную
          </button>
        </div>
      </div>
    )
  }

  const totalQuestions = Object.values(selectedCategories).reduce((a, b) => a + b, 0)

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 py-8 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/')}
            className="text-white/80 hover:text-white mb-4 flex items-center gap-2"
          >
            ← На главную
          </button>
          <h1 className="text-4xl font-extrabold text-white mb-2">
            {profession?.name || 'Настройка собеседования'}
          </h1>
          <p className="text-white/80">
            Выберите темы и количество вопросов для подготовки
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Левая колонка - Категории */}
          <div className="lg:col-span-2 space-y-4">
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6">
              <h2 className="text-xl font-bold text-white mb-4">📚 Выберите темы</h2>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {categories.map((category) => (
                  <div
                    key={category.id}
                    onClick={() => handleCategoryToggle(category.id)}
                    className={`relative overflow-hidden p-4 rounded-xl border-2 transition-all duration-300 cursor-pointer group ${
                      selectedCategories[category.id]
                        ? 'bg-gradient-to-br from-yellow-400/40 to-orange-400/40 border-yellow-400 shadow-lg shadow-yellow-400/40 scale-[1.02]'
                        : 'bg-gradient-to-br from-white/5 to-white/10 border-white/20 hover:border-white/40 hover:shadow-md hover:shadow-white/10'
                    }`}
                  >
                    {/* Фоновый декоративный элемент */}
                    <div className={`absolute -right-4 -top-4 w-20 h-20 rounded-full transition-all duration-500 ${
                      selectedCategories[category.id]
                        ? 'bg-yellow-400/30 scale-100'
                        : 'bg-white/5 scale-0 group-hover:scale-100'
                    }`} />
                    
                    {/* Галочка в углу */}
                    <div className={`absolute top-3 right-3 transition-all duration-300 ${
                      selectedCategories[category.id]
                        ? 'opacity-100 scale-100 rotate-0'
                        : 'opacity-0 scale-50 -rotate-45'
                    }`}>
                      <div className="w-7 h-7 bg-yellow-400 rounded-full flex items-center justify-center shadow-lg">
                        <span className="text-indigo-600 font-bold text-sm">✓</span>
                      </div>
                    </div>

                    {/* Контент */}
                    <div className="relative z-10">
                      <h3 className={`text-base font-bold mb-2 transition-colors duration-300 ${
                        selectedCategories[category.id] ? 'text-yellow-200' : 'text-white'
                      }`}>
                        {category.name}
                      </h3>
                      {category.description && (
                        <p className={`text-xs leading-relaxed line-clamp-2 transition-colors duration-300 ${
                          selectedCategories[category.id] ? 'text-yellow-100/90' : 'text-white/60'
                        }`}>
                          {category.description}
                        </p>
                      )}
                      
                      {/* Ползунок количества вопросов */}
                      {selectedCategories[category.id] && (
                        <div className="mt-4 pt-3 border-t border-yellow-400/30" onClick={(e) => e.stopPropagation()}>
                          <div className="flex items-center justify-between mb-2">
                            <label className="text-yellow-200 text-xs font-medium">Количество вопросов:</label>
                            <span className="text-yellow-300 text-lg font-bold bg-gradient-to-r from-yellow-400/30 to-orange-400/30 px-3 py-1 rounded-lg border border-yellow-400/50">
                              {selectedCategories[category.id]}
                            </span>
                          </div>
                          <input
                            type="range"
                            min="1"
                            max="20"
                            value={selectedCategories[category.id] || 5}
                            onChange={(e) => handleQuestionCountChange(category.id, parseInt(e.target.value))}
                            className="w-full h-2 bg-white/20 rounded-full appearance-none cursor-pointer accent-yellow-400 hover:accent-yellow-300 transition-all"
                          />
                          <div className="flex justify-between text-xs text-yellow-200/60 mt-1.5 font-medium">
                            <span>1</span>
                            <span>10</span>
                            <span>20</span>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {categories.length === 0 && (
                <div className="text-center py-8">
                  <div className="text-4xl mb-2">📭</div>
                  <p className="text-white/70">Категории пока не добавлены</p>
                </div>
              )}
            </div>
          </div>

          {/* Правая колонка - Настройки и сохранённые конфигурации */}
          <div className="space-y-4">
            {/* Настройки сложности */}
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6">
              <h2 className="text-xl font-bold text-white mb-4">⚙️ Настройки</h2>
              
              <div className="mb-4">
                <label className="text-white/80 text-xs block mb-2">Уровень сложности</label>
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value as 'intern' | 'junior' | 'middle')}
                  className="w-full px-3 py-2 rounded-lg bg-white/20 text-white border border-white/30 focus:border-yellow-400"
                >
                  <option value="intern">Intern 🌱</option>
                  <option value="junior">Junior 📚</option>
                  <option value="middle">Middle 💼</option>
                </select>
              </div>

              <div className="bg-white/10 rounded-lg p-3 mb-4">
                <div className="text-white/70 text-xs mb-1">Всего вопросов:</div>
                <div className="text-2xl font-bold text-white">{totalQuestions}</div>
              </div>

              <button
                onClick={handleQuickStart}
                disabled={totalQuestions === 0}
                className="w-full bg-gradient-to-r from-yellow-400 to-yellow-300 text-indigo-600 py-3 rounded-lg font-bold shadow-lg hover:shadow-xl transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
              >
                🚀 Начать собеседование
              </button>

              <button
                onClick={() => setShowConfigForm(!showConfigForm)}
                className="w-full mt-3 bg-white/20 backdrop-blur-sm text-white border-2 border-white/50 py-3 rounded-lg font-bold hover:bg-white/30 transition-all"
              >
                💾 Сохранить конфигурацию
              </button>
            </div>

            {/* Форма сохранения конфигурации */}
            {showConfigForm && (
              <div className="bg-white/10 backdrop-blur-md rounded-xl p-6">
                <h3 className="text-lg font-bold text-white mb-4">Сохранить конфигурацию</h3>
                
                <input
                  type="text"
                  value={configName}
                  onChange={(e) => setConfigName(e.target.value)}
                  placeholder="Название (например, Junior DevOps)"
                  className="w-full px-3 py-2 rounded-lg bg-white/20 text-white placeholder-white/50 border border-white/30 focus:border-yellow-400 mb-4"
                />

                <div className="flex gap-2">
                  <button
                    onClick={handleSaveConfig}
                    disabled={!configName.trim() || Object.keys(selectedCategories).length === 0}
                    className="flex-1 bg-green-500 text-white py-2 rounded-lg font-bold hover:bg-green-600 transition-all disabled:opacity-50"
                  >
                    Сохранить
                  </button>
                  <button
                    onClick={() => setShowConfigForm(false)}
                    className="flex-1 bg-white/20 text-white py-2 rounded-lg font-bold hover:bg-white/30 transition-all"
                  >
                    Отмена
                  </button>
                </div>
              </div>
            )}

            {/* Сохранённые конфигурации */}
            {savedConfigs.length > 0 && (
              <div className="bg-white/10 backdrop-blur-md rounded-xl p-6">
                <h2 className="text-xl font-bold text-white mb-4">📋 Сохранённые</h2>
                
                <div className="space-y-3">
                  {savedConfigs.map((config) => (
                    <div
                      key={config.id}
                      className="bg-white/5 rounded-lg p-3 border border-white/20 hover:border-yellow-400 transition-all"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-white font-bold text-sm">{config.name}</h3>
                        <span className={`text-xs px-2 py-0.5 rounded-full ${
                          config.difficulty === 'intern' ? 'bg-green-500' :
                          config.difficulty === 'junior' ? 'bg-blue-500' : 'bg-purple-500'
                        } text-white`}>
                          {config.difficulty === 'intern' ? '🌱' :
                           config.difficulty === 'junior' ? '📚' : '💼'}
                        </span>
                      </div>
                      
                      <div className="text-white/60 text-xs mb-2">
                        {config.category_configs.length} тем •{' '}
                        {config.category_configs.reduce((a, b) => a + b.question_count, 0)} вопросов
                      </div>

                      <button
                        onClick={() => handleStartFromConfig(config.id)}
                        className="w-full bg-yellow-400/20 text-yellow-300 py-2 rounded-lg text-xs font-bold hover:bg-yellow-400/30 transition-all"
                      >
                        ▶️ Начать
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
