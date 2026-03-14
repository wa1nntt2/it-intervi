import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { sessionsApi, questionsApi, progressApi } from '../services/api'
import { Question } from '../types'
import confetti from 'canvas-confetti'

// Функция для перемешивания массива (Fisher-Yates)
function shuffleArray<T>(array: T[]): { items: T[]; originalIndexMap: number[] } {
  const shuffled = [...array]
  const originalIndexMap = array.map((_, i) => i)
  
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
    ;[originalIndexMap[i], originalIndexMap[j]] = [originalIndexMap[j], originalIndexMap[i]]
  }
  
  return { items: shuffled, originalIndexMap }
}

export default function Session() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [questions, setQuestions] = useState<Question[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<number, number | number[]>>({})
  const [orderingAnswers, setOrderingAnswers] = useState<Record<number, string[]>>({})
  const [showResultModal, setShowResultModal] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showResults, setShowResults] = useState(false)
  const [score, setScore] = useState(0)
  
  // Перемешанные варианты ответов для каждого вопроса
  const [shuffledOptions, setShuffledOptions] = useState<Record<number, { items: string[]; originalIndexMap: number[] }>>({})

  useEffect(() => {
    const loadSession = async () => {
      if (!id) return
      try {
        const session = await sessionsApi.getById(parseInt(id))
        const questionsData = await Promise.all(
          session.question_ids.map((qId: number) => questionsApi.getById(qId))
        )
        setQuestions(questionsData)
        
        // Перемешиваем варианты ответов для каждого вопроса
        const shuffled: Record<number, { items: string[]; originalIndexMap: number[] }> = {}
        questionsData.forEach(q => {
          if (q.question_type === 'mcq' && q.options) {
            shuffled[q.id] = shuffleArray(q.options)
          }
        })
        setShuffledOptions(shuffled)
      } catch (err: any) {
        console.error('Failed to load session', err)
        if (err?.response?.status === 404) {
          setError('Сессия не найдена')
        }
      } finally {
        setLoading(false)
      }
    }
    loadSession()
  }, [id])

  const handleAnswer = (questionId: number, shuffledIndex: number) => {
    // Получаем оригинальный индекс ответа
    const mapping = shuffledOptions[questionId]
    if (mapping) {
      const originalIndex = mapping.originalIndexMap[shuffledIndex]
      setAnswers((prev) => ({ ...prev, [questionId]: originalIndex }))
    }
  }

  const handleShowResult = () => {
    setShowResultModal(true)
  }

  const handleNextQuestion = () => {
    setShowResultModal(false)
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1)
    } else {
      // Последний вопрос - показываем результаты сессии
      handleSubmit()
    }
  }

  const handleOrderingMove = (questionId: number, fromIndex: number, toIndex: number) => {
    if (fromIndex === toIndex) return
    const currentOrder = orderingAnswers[questionId] ||
      questions.find(q => q.id === questionId)?.options.map((_, i) => String(i)) || []
    const newOrder = [...currentOrder]
    const [removed] = newOrder.splice(fromIndex, 1)
    newOrder.splice(toIndex, 0, removed)
    setOrderingAnswers((prev) => ({ ...prev, [questionId]: newOrder }))
  }

  const isOrderingComplete = (questionId: number) => {
    const order = orderingAnswers[questionId]
    if (!order || order.length === 0) return false
    const currentOrder = orderingAnswers[questionId]
    const prevOrder = questions.find(q => q.id === questionId)?.options.map((_, i) => String(i))
    if (!prevOrder) return false
    return JSON.stringify(currentOrder) !== JSON.stringify(prevOrder)
  }

  const handleDragStart = (e: React.DragEvent, questionId: number, index: number) => {
    e.dataTransfer.setData('text/plain', JSON.stringify({ questionId, index }))
    e.dataTransfer.effectAllowed = 'move'
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
  }

  const handleDrop = (e: React.DragEvent, questionId: number, toIndex: number) => {
    e.preventDefault()
    const data = e.dataTransfer.getData('text/plain')
    if (!data) return
    try {
      const { questionId: fromQuestionId, index: fromIndex } = JSON.parse(data)
      if (fromQuestionId === questionId) {
        handleOrderingMove(questionId, fromIndex, toIndex)
      }
    } catch (err) {
      console.error('Drop error:', err)
    }
  }

  const handleSubmit = async () => {
    let correctCount = 0
    
    for (const question of questions) {
      if (question.question_type === 'ordering') {
        const userOrder = orderingAnswers[question.id]
        const correctOrder = question.correct_order?.map(i => String(i))
        const isCorrect = userOrder && correctOrder && JSON.stringify(userOrder) === JSON.stringify(correctOrder)
        if (isCorrect) {
          correctCount++
        }
        // TODO: сохранить ответ для ordering вопросов
      } else {
        const selectedOption = answers[question.id]
        const isCorrect = selectedOption === question.correct_option
        if (isCorrect) {
          correctCount++
        }
        // Сохраняем ответ в БД (и правильные, и неправильные)
        if (selectedOption !== undefined) {
          await questionsApi.submitAnswer(question.id, selectedOption as number)
        }
      }
    }
    
    // Начисляем XP
    const xpEarned = Math.round(correctCount * 10)
    try {
      await progressApi.addXp(xpEarned, correctCount, questions.length)
      // Сохраняем прогресс в localStorage для обновления в профиле
      const progressData = await progressApi.getMyProgress()
      localStorage.setItem('userProgress', JSON.stringify(progressData))
    } catch (err) {
      console.error('Failed to add XP:', err)
    }

    setScore(correctCount)
    setShowResults(true)
    await sessionsApi.complete(parseInt(id!), correctCount)
    
    // Запускаем конфетти если хороший результат
    const percentage = (correctCount / questions.length) * 100
    if (percentage >= 80) {
      confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#fbbf24', '#3b82f6', '#10b981', '#f472b6']
      })
    }
  }

  const getDifficultyConfig = (difficulty: string) => {
    const configs: Record<string, { bg: string; text: string; label: string; icon: string }> = {
      'intern': { bg: 'bg-green-500', text: 'text-green-700', label: 'Intern', icon: '🌱' },
      'junior': { bg: 'bg-blue-500', text: 'text-blue-700', label: 'Junior', icon: '📚' },
      'middle': { bg: 'bg-purple-500', text: 'text-purple-700', label: 'Middle', icon: '💼' }
    }
    return configs[difficulty] || configs['junior']
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center">
        <div className="text-white text-xs animate-pulse">🚀 Загрузка вопросов...</div>
      </div>
    )
  }

  if (error) {
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

  if (questions.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center">
        <div className="bg-white/10 backdrop-blur-md p-8 rounded-lg shadow-2xl text-center max-w-md">
          <div className="text-6xl mb-2">📭</div>
          <h1 className="text-xs font-bold text-white mb-2">Нет вопросов</h1>
          <p className="text-white/90 mb-2">Для выбранной профессии пока нет вопросов</p>
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

  if (showResults) {
    const percentage = Math.round((score / questions.length) * 100)
    const getResultEmoji = () => {
      if (percentage === 100) return '🏆'
      if (percentage >= 80) return '🎉'
      if (percentage >= 60) return '👍'
      if (percentage >= 40) return '📚'
      return '💪'
    }

    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center py-12 px-4">
        <div className="bg-white/10 backdrop-blur-md p-8 rounded-lg shadow-2xl text-center max-w-lg w-full">
          <div className="text-7xl mb-2 animate-bounce">{getResultEmoji()}</div>
          <h1 className="text-4xl font-extrabold text-white mb-2">Результаты</h1>
          
          {/* Score Circle */}
          <div className="relative w-40 h-40 mx-auto mb-2">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="80"
                cy="80"
                r="70"
                stroke="rgba(255,255,255,0.2)"
                strokeWidth="12"
                fill="none"
              />
              <circle
                cx="80"
                cy="80"
                r="70"
                stroke={percentage >= 60 ? '#fbbf24' : '#f87171'}
                strokeWidth="12"
                fill="none"
                strokeDasharray={`${(percentage / 100) * 440} 440`}
                className="transition-all duration-1000"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="text-4xl font-extrabold text-white">{score}/{questions.length}</div>
                <div className="text-white/80 text-xs">{percentage}%</div>
              </div>
            </div>
          </div>

          <p className="text-base text-white/90 mb-8">
            {percentage === 100 ? 'Идеально! 🌟' :
             percentage >= 80 ? 'Отличный результат! 👏' :
             percentage >= 60 ? 'Хорошо, но можно лучше! 💪' :
             'Продолжайте учиться! 📖'}
          </p>
          
          <div className="flex flex-col gap-3">
            <button
              onClick={() => navigate('/session/new')}
              className="bg-white text-indigo-600 px-8 py-4 rounded-lg font-bold text-xs hover:bg-yellow-300 transition-all hover:scale-105"
            >
              🔄 Ещё одна попытка
            </button>
            <button
              onClick={() => navigate('/')}
              className="bg-white/20 backdrop-blur-sm text-white border-2 border-white/50 px-8 py-4 rounded-lg font-bold text-xs hover:bg-white/30 transition-all hover:scale-105"
            >
              🏠 На главную
            </button>
          </div>
        </div>
      </div>
    )
  }

  const currentQuestion = questions[currentQuestionIndex]
  const isOrderingQuestion = currentQuestion.question_type === 'ordering'
  const currentOrdering = orderingAnswers[currentQuestion.id] ||
    currentQuestion.options.map((_, i) => String(i))
  
  const difficultyConfig = getDifficultyConfig(currentQuestion.difficulty)

  const isAnswered = isOrderingQuestion
    ? isOrderingComplete(currentQuestion.id)
    : answers[currentQuestion.id] !== undefined

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 py-4 px-3">
      <div className="max-w-3xl mx-auto">
        
        {/* Progress Header */}
        <div className="mb-2">
          <div className="flex justify-between items-center mb-2">
            <span className="text-white/90 font-medium text-xs">
              Вопрос {currentQuestionIndex + 1} из {questions.length}
            </span>
            <span className="text-white/70 text-xs">
              {Math.round(((currentQuestionIndex + 1) / questions.length) * 100)}%
            </span>
          </div>
          <div className="w-full bg-white/20 rounded-full h-2 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-yellow-400 to-yellow-300 transition-all duration-500"
              style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Question Card */}
        <div className="bg-white/10 backdrop-blur-md rounded-lg shadow-2xl overflow-hidden">
          {/* Card Header */}
          <div className="bg-white/20 px-4 py-3 flex items-center gap-3">
            <span className={`px-2 py-1 rounded-full text-xs font-bold text-white ${difficultyConfig.bg}`}>
              {difficultyConfig.icon} {difficultyConfig.label}
            </span>
            {isOrderingQuestion && (
              <span className="px-2 py-1 rounded-full text-xs font-bold text-white bg-blue-500">
                🔀 Упорядочивание
              </span>
            )}
          </div>

          {/* Question Content */}
          <div className="p-3">
            <h2 className="text-xs font-bold text-white mb-2 leading-relaxed">
              {currentQuestion.text}
            </h2>

            {isOrderingQuestion ? (
              <div className="space-y-3">
                {currentOrdering.map((optionIndex, position) => {
                  const originalIndex = parseInt(optionIndex)
                  const option = currentQuestion.options[originalIndex]
                  return (
                    <div
                      key={optionIndex}
                      draggable
                      onDragStart={(e) => handleDragStart(e, currentQuestion.id, position)}
                      onDragOver={handleDragOver}
                      onDrop={(e) => handleDrop(e, currentQuestion.id, position)}
                      className="group flex items-center gap-3 p-3 rounded-lg bg-white/10 backdrop-blur-sm border border-white/20 cursor-move hover:bg-white/20 hover:border-yellow-400 transition-all hover:scale-102"
                      title="Перетащите для изменения порядка"
                    >
                      <span className={`w-7 h-7 flex items-center justify-center rounded-full font-bold text-xs transition-all ${
                        position === originalIndex 
                          ? 'bg-white/20 text-white' 
                          : 'bg-yellow-400 text-indigo-600'
                      }`}>
                        {position + 1}
                      </span>
                      <span className="flex-1 text-white font-medium">{option}</span>
                      <span className="text-white/50 group-hover:text-white transition-colors">
                        ⠿
                      </span>
                    </div>
                  )
                })}
              </div>
            ) : (
              <div className="space-y-3">
                {(() => {
                  const shuffled = shuffledOptions[currentQuestion.id]
                  const optionsToRender = shuffled ? shuffled.items : currentQuestion.options
                  
                  return optionsToRender.map((option, shuffledIndex) => {
                    // Получаем оригинальный индекс для проверки ответа
                    const originalIndex = shuffled ? shuffled.originalIndexMap[shuffledIndex] : shuffledIndex
                    const isSelected = answers[currentQuestion.id] === originalIndex

                    return (
                      <button
                        key={shuffledIndex}
                        onClick={() => handleAnswer(currentQuestion.id, shuffledIndex)}
                        className={`w-full text-left p-3 rounded-lg border-2 transition-all duration-200 group ${
                          isSelected
                            ? 'bg-yellow-400 border-yellow-400 text-indigo-900 shadow-lg shadow-yellow-400/30 scale-102'
                            : 'bg-white/10 border-white/20 text-white hover:bg-white/20 hover:border-yellow-400/50'
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <span className={`w-7 h-7 flex items-center justify-center rounded-full font-bold text-xs transition-all ${
                            isSelected
                              ? 'bg-indigo-600 text-white'
                              : 'bg-white/20 text-white group-hover:bg-yellow-400 group-hover:text-indigo-600'
                          }`}>
                            {String.fromCharCode(65 + shuffledIndex)}
                          </span>
                          <span className="flex-1 font-medium">{option}</span>
                          {isSelected && (
                            <span className="text-xs">✓</span>
                          )}
                        </div>
                      </button>
                    )
                  })
                })()}
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="mt-8 flex justify-between gap-3">
              <button
                onClick={() => setCurrentQuestionIndex((prev) => Math.max(0, prev - 1))}
                disabled={currentQuestionIndex === 0}
                className="px-6 py-3 bg-white/20 backdrop-blur-sm text-white border-2 border-white/50 rounded-lg font-bold hover:bg-white/30 transition-all hover:scale-105 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:scale-100"
              >
                ← Назад
              </button>
              <button
                onClick={handleShowResult}
                disabled={!isAnswered}
                className="px-8 py-3 bg-gradient-to-r from-yellow-400 to-yellow-300 text-indigo-600 rounded-lg font-bold shadow-lg hover:shadow-xl transition-all hover:scale-105 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center gap-2"
              >
                {currentQuestionIndex < questions.length - 1 ? (
                  <>
                    Далее →
                  </>
                ) : (
                  <>
                    🏁 Завершить →
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Hint */}
        <div className="mt-4 text-center">
          <p className="text-white/60 text-xs">
            {!isOrderingQuestion && '💡 Выберите ответ и нажмите "Далее"'}
            {isOrderingQuestion && '💡 Расположите в порядке и нажмите "Далее"'}
          </p>
        </div>
      </div>

      {/* Result Modal */}
      {showResultModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-3">
          <div className="bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-8">
              {/* Header */}
              <div className="text-center mb-2">
                <div className="text-6xl mb-2">
                  {answers[currentQuestion.id] === currentQuestion.correct_option ? '🎉' : '📚'}
                </div>
                <h3 className={`text-3xl font-extrabold mb-2 ${
                  answers[currentQuestion.id] === currentQuestion.correct_option
                    ? 'text-green-300'
                    : 'text-yellow-300'
                }`}>
                  {answers[currentQuestion.id] === currentQuestion.correct_option
                    ? 'Правильно!'
                    : 'Неправильно'}
                </h3>
              </div>

              {/* Question */}
              <div className="bg-white/10 backdrop-blur-md rounded-lg p-5 mb-2">
                <h4 className="text-xs font-bold text-white/70 uppercase mb-2">Вопрос</h4>
                <p className="text-base font-bold text-white">{currentQuestion.text}</p>
              </div>

              {/* Your Answer */}
              <div className={`rounded-lg p-5 mb-2 ${
                answers[currentQuestion.id] === currentQuestion.correct_option
                  ? 'bg-green-500/20 border-2 border-green-400/50'
                  : 'bg-red-500/20 border-2 border-red-400/50'
              }`}>
                <h4 className="text-xs font-bold text-white/70 uppercase mb-2">Ваш ответ</h4>
                <div className="flex items-center gap-3">
                  <span className="text-xs">
                    {answers[currentQuestion.id] === currentQuestion.correct_option ? '✅' : '❌'}
                  </span>
                  <span className="text-xs font-medium text-white">
                    {currentQuestion.options[answers[currentQuestion.id] as number]}
                  </span>
                </div>
              </div>

              {/* Correct Answer (if wrong) */}
              {answers[currentQuestion.id] !== currentQuestion.correct_option && (
                <div className="bg-green-500/20 border-2 border-green-400/50 rounded-lg p-5 mb-2">
                  <h4 className="text-xs font-bold text-white/70 uppercase mb-2">Правильный ответ</h4>
                  <div className="flex items-center gap-3">
                    <span className="text-xs">✓</span>
                    <span className="text-xs font-medium text-white">
                      {currentQuestion.options[currentQuestion.correct_option!]}
                    </span>
                  </div>
                </div>
              )}

              {/* Explanation */}
              {currentQuestion.explanation && (
                <div className="bg-white/10 backdrop-blur-md rounded-lg p-5 mb-2">
                  <h4 className="text-xs font-bold text-white/70 uppercase mb-3 flex items-center gap-2">
                    <span className="text-base">💡</span>
                    Пояснение
                  </h4>
                  <p className="text-white/90 leading-relaxed whitespace-pre-line">
                    {currentQuestion.explanation}
                  </p>
                </div>
              )}

              {/* Action Button */}
              <button
                onClick={handleNextQuestion}
                className="w-full bg-gradient-to-r from-yellow-400 to-yellow-300 text-indigo-600 py-4 rounded-lg font-bold text-xs shadow-lg hover:shadow-xl transition-all hover:scale-105 flex items-center justify-center gap-2"
              >
                {currentQuestionIndex < questions.length - 1 ? (
                  <>
                    Следующий вопрос
                    <span>→</span>
                  </>
                ) : (
                  <>
                    🏁 Завершить и увидеть результат
                    <span>✓</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
