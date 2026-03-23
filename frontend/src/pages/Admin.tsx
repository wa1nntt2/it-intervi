import { useState, useEffect, useCallback } from 'react'
import { professionsApi, questionsApi, interviewsApi } from '../services/api'
import { Profession, Question, Category } from '../types'
import { Sidebar } from '../components/admin/Sidebar'
import { Modal } from '../components/admin/Modal'
import { StatCard } from '../components/admin/StatCard'
import { QuestionEditor } from '../components/admin/QuestionEditor'
import { AddCategoryModal } from '../components/admin/AddCategoryModal'
import { DifficultyDistribution } from '../components/admin/DifficultyDistribution'
import { ProfessionDistribution } from '../components/admin/ProfessionDistribution'
import { ImportExportModal } from '../components/admin/ImportExportModal'
import { ProfessionCards } from '../components/admin/ProfessionCards'
import { ProfessionDropdown } from '../components/admin/ProfessionDropdown'
import { QuestionPreview } from '../components/admin/QuestionPreview'
import { BulkActions } from '../components/admin/BulkActions'
import { ConfirmDialog } from '../components/ui/ConfirmDialog'
import { toast } from '../stores/toastStore'

export default function Admin() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [professions, setProfessions] = useState<Profession[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [questions, setQuestions] = useState<Question[]>([])
  const [loading, setLoading] = useState(true)

  // Фильтры
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedProfession, setSelectedProfession] = useState<string>('')
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('')
  const [selectedType, setSelectedType] = useState<string>('')
  const [selectedCategory, setSelectedCategory] = useState<string>('')

  // Модальные окна
  const [isEditorOpen, setIsEditorOpen] = useState(false)
  const [editingQuestion, setEditingQuestion] = useState<Question | null>(null)
  const [isImportExportOpen, setIsImportExportOpen] = useState(false)
  const [isAddCategoryOpen, setIsAddCategoryOpen] = useState(false)

  // Массовое удаление
  const [selectedQuestions, setSelectedQuestions] = useState<number[]>([])
  const [isDeleteConfirmOpen, setIsDeleteConfirmOpen] = useState(false)
  const [questionToDelete, setQuestionToDelete] = useState<number | null>(null)
  const [isBulkDelete, setIsBulkDelete] = useState(false)  // Массовое или одиночное удаление
  
  // Массовое изменение
  const [isBulkActionsOpen, setIsBulkActionsOpen] = useState(false)
  
  // Предпросмотр вопроса
  const [previewQuestion, setPreviewQuestion] = useState<Question | null>(null)
  
  // Валидация
  const [validationWarnings, setValidationWarnings] = useState<Record<number, string[]>>({})

  // Вид выбора профессии (card/grid)
  const [professionViewMode, setProfessionViewMode] = useState<'cards' | 'dropdown'>('cards')

  // Пагинация
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10

  // Подсчет вопросов по профессиям
  const questionCounts: Record<number, number> = {}
  questions.forEach(q => {
    questionCounts[q.profession_id] = (questionCounts[q.profession_id] || 0) + 1
  })

  useEffect(() => {
    loadProfessions()
  }, [])

  useEffect(() => {
    if (professions.length > 0) {
      loadCategories()
    }
  }, [professions])

  // Перезагрузка вопросов при изменении фильтров
  useEffect(() => {
    if (professions.length > 0) {
      loadQuestions()
    }
  }, [selectedProfession, selectedDifficulty, selectedType, selectedCategory, searchQuery])

  // Обработчик открытия модального окна добавления категории
  useEffect(() => {
    const handleOpenAddCategory = () => {
      setIsAddCategoryOpen(true)
    }
    window.addEventListener('openAddCategory', handleOpenAddCategory)
    return () => window.removeEventListener('openAddCategory', handleOpenAddCategory)
  }, [])

  const loadProfessions = async () => {
    const data = await professionsApi.getAll()
    setProfessions(data)
  }

  const loadCategories = async () => {
    const allCategories: Category[] = []
    for (const profession of professions) {
      try {
        const cats = await interviewsApi.getCategoriesByProfession(profession.id)
        allCategories.push(...cats)
      } catch (e) {
        console.error(`Failed to load categories for profession ${profession.id}`)
      }
    }
    setCategories(allCategories)
  }

  const loadQuestions = useCallback(async () => {
    setLoading(true)
    try {
      // Загружаем все вопросы постранично с фильтрами
      let allQuestions: Question[] = []
      let page = 1
      const pageSize = 100
      let hasMore = true

      // Собираем фильтры
      const filters: Record<string, any> = {}
      if (selectedProfession) filters.professionId = parseInt(selectedProfession)
      if (selectedDifficulty) filters.difficulty = selectedDifficulty
      if (selectedType) filters.questionType = selectedType
      if (selectedCategory) filters.categoryId = parseInt(selectedCategory)
      if (searchQuery) filters.search = searchQuery

      while (hasMore) {
        const response = await questionsApi.getAll(
          filters.professionId,
          page,
          pageSize,
          filters.search,
          filters.categoryId,
          filters.difficulty,
          filters.questionType
        )
        const questionsData = response.items || response
        allQuestions = [...allQuestions, ...questionsData]

        // Проверяем есть ли ещё страницы
        if (response.meta && response.meta.total_pages > page) {
          page++
        } else {
          hasMore = false
        }
      }

      setQuestions(allQuestions)
      validateQuestions(allQuestions)
    } catch (error) {
      console.error('Failed to load questions:', error)
    } finally {
      setLoading(false)
    }
  }, [selectedProfession, selectedDifficulty, selectedType, selectedCategory, searchQuery])

  // Валидация вопросов
  const validateQuestions = (questions: Question[]) => {
    const warnings: Record<number, string[]> = {}
    questions.forEach(q => {
      const qWarnings: string[] = []
      if (q.text.length < 10) qWarnings.push('Вопрос слишком короткий')
      if (q.options.length < 2) qWarnings.push('Меньше 2 вариантов ответа')
      if (q.options.some((opt, i) => q.options.filter((_, j) => j !== i).includes(opt))) {
        qWarnings.push('Есть повторяющиеся варианты')
      }
      if (!q.explanation) qWarnings.push('Нет пояснения')
      if (qWarnings.length > 0) warnings[q.id] = qWarnings
    })
    setValidationWarnings(warnings)
  }

  // Горячие клавиши
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Игнорируем если фокус в input/textarea
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return
      
      if (e.ctrlKey || e.metaKey) {
        switch (e.key.toLowerCase()) {
          case 'n': // Ctrl+N - новый вопрос
            e.preventDefault()
            setEditingQuestion(null)
            setIsEditorOpen(true)
            break
          case 'f': // Ctrl+F - фокус на поиск
            e.preventDefault()
            document.getElementById('question-search')?.focus()
            break
        }
      }
      if (e.key === 'Escape') {
        setPreviewQuestion(null)
        setIsBulkActionsOpen(false)
      }
    }
    
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  // Фильтрация вопросов (теперь выполняется на сервере)
  const filteredQuestions = questions

  // Пагинация
  const totalPages = Math.ceil(filteredQuestions.length / itemsPerPage)
  const paginatedQuestions = filteredQuestions.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  )

  // Статистика
  const stats = {
    total: questions.length,
    mcq: questions.filter((q) => q.question_type === 'mcq').length,
    ordering: questions.filter((q) => q.question_type === 'ordering').length,
    intern: questions.filter((q) => q.difficulty === 'intern').length,
    junior: questions.filter((q) => q.difficulty === 'junior').length,
    middle: questions.filter((q) => q.difficulty === 'middle').length,
  }

  const handleCreateQuestion = async (data: any) => {
    await questionsApi.create({
      ...data,
      profession_id: parseInt(data.profession_id),
      category_ids: data.category_ids || [],
      explanation: data.explanation || '',
    })
    setIsEditorOpen(false)
    loadQuestions()
  }

  const handleUpdateQuestion = async (data: any) => {
    if (!editingQuestion) return
    await questionsApi.update(editingQuestion.id, {
      ...data,
      profession_id: parseInt(data.profession_id),
      category_ids: data.category_ids || [],
      explanation: data.explanation || '',
    })
    setIsEditorOpen(false)
    setEditingQuestion(null)
    loadQuestions()
  }

  const handleDeleteQuestion = async (id: number) => {
    setQuestionToDelete(id)
    setIsBulkDelete(false)  // Одиночное удаление
    setIsDeleteConfirmOpen(true)
  }

  const handleConfirmDelete = async () => {
    if (questionToDelete === null) return
    try {
      await questionsApi.delete(questionToDelete)
      toast.success('Вопрос удален')
      loadQuestions()
    } catch (error) {
      toast.error('Ошибка при удалении вопроса')
    } finally {
      setIsDeleteConfirmOpen(false)
      setQuestionToDelete(null)
    }
  }

  const handleToggleQuestionSelection = (id: number) => {
    setSelectedQuestions((prev) =>
      prev.includes(id) ? prev.filter((q) => q !== id) : [...prev, id]
    )
  }

  const handleSelectAllQuestions = () => {
    if (selectedQuestions.length === paginatedQuestions.length) {
      setSelectedQuestions([])
    } else {
      setSelectedQuestions(paginatedQuestions.map((q) => q.id))
    }
  }

  const handleBulkDelete = async () => {
    try {
      await Promise.all(selectedQuestions.map((id) => questionsApi.delete(id)))
      toast.success(`Удалено ${selectedQuestions.length} вопросов`)
      setSelectedQuestions([])
      setQuestionToDelete(null)
      setIsBulkDelete(false)
      setIsDeleteConfirmOpen(false)
      loadQuestions()
    } catch (error) {
      toast.error('Ошибка при удалении вопросов')
    }
  }

  const handleDuplicateQuestion = async (id: number) => {
    try {
      await questionsApi.duplicate(id)
      loadQuestions()
    } catch (error) {
      console.error('Failed to duplicate:', error)
    }
  }

  const handleBulkChange = async (updates: { profession_id?: number; difficulty?: string }) => {
    try {
      await questionsApi.bulkUpdate(selectedQuestions, updates)
      setIsBulkActionsOpen(false)
      setSelectedQuestions([])
      loadQuestions()
    } catch (error) {
      console.error('Failed to bulk update:', error)
    }
  }

  const handlePreview = (question: Question) => {
    setPreviewQuestion(question)
  }

  const openEditModal = (question: Question) => {
    setEditingQuestion(question)
    setIsEditorOpen(true)
  }

  const openCreateModal = () => {
    setEditingQuestion(null)
    setIsEditorOpen(true)
  }

  const getDifficultyBadge = (difficulty: string) => {
    const colors = {
      intern: 'bg-green-100 text-green-800',
      junior: 'bg-blue-100 text-blue-800',
      middle: 'bg-purple-100 text-purple-800',
    }
    const labels = {
      intern: 'Intern',
      junior: 'Junior',
      middle: 'Middle',
    }
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[difficulty as keyof typeof colors]}`}>
        {labels[difficulty as keyof typeof labels]}
      </span>
    )
  }

  const getTypeBadge = (type: string) => {
    const colors = {
      mcq: 'bg-indigo-100 text-indigo-800',
      ordering: 'bg-purple-100 text-purple-800',
    }
    const labels = {
      mcq: 'MCQ',
      ordering: 'Порядок',
    }
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[type as keyof typeof colors]}`}>
        {labels[type as keyof typeof labels]}
      </span>
    )
  }

  const getProfessionName = (id: number) => {
    const profession = professions.find((p) => p.id === id)
    return profession ? profession.name : 'Неизвестно'
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Основной контент */}
      <div className="lg:ml-64">
        {/* Верхняя панель */}
        <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
          <div className="flex items-center justify-between px-6 py-4">
            {/* Поиск */}
            <div className="flex items-center gap-4 flex-1">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden text-gray-500 hover:text-gray-700"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">📝 Вопросы</h1>
                <p className="text-sm text-gray-500 mt-1">Управление вопросами</p>
              </div>
              <div className="relative max-w-md w-full">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </span>
                <input
                  type="text"
                  placeholder="Поиск вопросов..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-gray-100 border-0 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500 transition-all"
                />
              </div>
            </div>

            {/* Правая часть */}
            <div className="flex items-center gap-3">
              {/* Кнопка Импорт/Экспорт */}
              <button
                onClick={() => setIsImportExportOpen(true)}
                className="flex items-center gap-2 px-4 py-2.5 border border-gray-200 text-gray-700 rounded-xl hover:bg-gray-50 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                </svg>
                <span className="font-medium hidden sm:inline">Импорт/Экспорт</span>
              </button>

              {/* Разделитель */}
              <div className="w-px h-8 bg-gray-200"></div>

              {/* Кнопка Добавить */}
              <button
                onClick={openCreateModal}
                className="flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-indigo-500 to-indigo-600 text-white rounded-xl hover:from-indigo-600 hover:to-indigo-700 shadow-md hover:shadow-lg transition-all"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                <span className="font-medium">Добавить</span>
              </button>
            </div>
          </div>

          {/* Вкладки */}
          <div className="px-6 border-t border-gray-100">
            <div className="flex items-center gap-8">
              <button className="py-3 border-b-2 border-indigo-500 text-indigo-600 font-medium text-sm">
                Все вопросы
              </button>
              <button className="py-3 border-b-2 border-transparent text-gray-500 hover:text-gray-700 font-medium text-sm transition-colors">
                Избранные
              </button>
              <button className="py-3 border-b-2 border-transparent text-gray-500 hover:text-gray-700 font-medium text-sm transition-colors">
                Архив
              </button>
            </div>
          </div>
        </header>

        <main className="p-6">
          {/* Карточки статистики */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            <StatCard
              title="Всего вопросов"
              value={stats.total}
              icon={
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              }
              color="indigo"
              subtitle={`из ${professions.length} профессий`}
            />
            <StatCard
              title="MCQ вопросы"
              value={stats.mcq}
              icon={
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              }
              color="green"
              progress={stats.total > 0 ? Math.round((stats.mcq / stats.total) * 100) : 0}
            />
            <StatCard
              title="Вопросы на порядок"
              value={stats.ordering}
              icon={
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                </svg>
              }
              color="purple"
              progress={stats.total > 0 ? Math.round((stats.ordering / stats.total) * 100) : 0}
            />
            <StatCard
              title="Профессий"
              value={professions.length}
              icon={
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              }
              color="cyan"
            />
          </div>

          {/* Графики распределения */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <DifficultyDistribution
              intern={stats.intern}
              junior={stats.junior}
              middle={stats.middle}
            />
            <ProfessionDistribution
              professions={professions}
              questions={questions}
            />
          </div>

          {/* Выбор профессии */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 mb-6 p-5">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <h3 className="text-lg font-semibold text-gray-900">Выбор профессии</h3>
              </div>
              <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setProfessionViewMode('cards')}
                  className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                    professionViewMode === 'cards'
                      ? 'bg-white text-indigo-600 shadow-sm'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  📊 Плитки
                </button>
                <button
                  onClick={() => setProfessionViewMode('dropdown')}
                  className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                    professionViewMode === 'dropdown'
                      ? 'bg-white text-indigo-600 shadow-sm'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  📋 Список
                </button>
              </div>
            </div>

            {professionViewMode === 'cards' ? (
              <ProfessionCards
                professions={professions}
                questionCounts={questionCounts}
                selectedProfession={selectedProfession}
                onChange={setSelectedProfession}
              />
            ) : (
              <ProfessionDropdown
                professions={professions}
                questionCounts={questionCounts}
                selectedProfession={selectedProfession}
                onChange={setSelectedProfession}
              />
            )}
          </div>

          {/* Фильтры */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 mb-6 p-5">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
                <h3 className="text-lg font-semibold text-gray-900">Дополнительные фильтры</h3>
              </div>
              {(searchQuery || selectedDifficulty || selectedType || selectedCategory) && (
                <button
                  onClick={() => {
                    setSearchQuery('')
                    setSelectedDifficulty('')
                    setSelectedType('')
                    setSelectedCategory('')
                  }}
                  className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
                >
                  ✕ Сбросить
                </button>
              )}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <select
                value={selectedDifficulty}
                onChange={(e) => setSelectedDifficulty(e.target.value)}
                className="border border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="">Все уровни</option>
                <option value="intern">🌱 Intern</option>
                <option value="junior">📚 Junior</option>
                <option value="middle">💼 Middle</option>
              </select>

              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="border border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="">Все типы</option>
                <option value="mcq">Multiple Choice</option>
                <option value="ordering">Упорядочивание</option>
              </select>

              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="border border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="">Все категории</option>
                {categories.map((cat) => (
                  <option key={cat.id} value={cat.id}>
                    {cat.name} ({professions.find(p => p.id === cat.profession_id)?.name || 'Unknown'})
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Таблица вопросов */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
              <div className="flex items-center gap-4">
                <h3 className="text-lg font-semibold text-gray-900">Список вопросов</h3>
                {selectedQuestions.length > 0 && (
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-indigo-600 font-medium bg-indigo-50 px-3 py-1 rounded-full">
                      Выбрано: {selectedQuestions.length}
                    </span>
                    <button
                      onClick={() => setIsBulkActionsOpen(true)}
                      className="text-sm text-indigo-600 hover:text-indigo-700 font-medium flex items-center gap-1"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      Изменить
                    </button>
                    <button
                      onClick={() => {
                        setIsBulkDelete(true)  // Массовое удаление
                        setIsDeleteConfirmOpen(true)
                      }}
                      className="text-sm text-red-600 hover:text-red-700 font-medium flex items-center gap-1"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                      Удалить
                    </button>
                  </div>
                )}
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">Ctrl+N: Новый</span>
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">Ctrl+F: Поиск</span>
                <span className="text-sm text-gray-500">
                  {filteredQuestions.length} из {questions.length}
                </span>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left">
                      <input
                        type="checkbox"
                        checked={selectedQuestions.length === paginatedQuestions.length && paginatedQuestions.length > 0}
                        onChange={handleSelectAllQuestions}
                        className="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                      />
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Вопрос
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Тема
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Профессия
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Тип
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Сложность
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
                  ) : paginatedQuestions.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="px-6 py-12 text-center">
                        <div className="text-gray-400 mb-2">📭</div>
                        <p className="text-gray-500">Вопросы не найдены</p>
                      </td>
                    </tr>
                  ) : (
                    paginatedQuestions.map((q) => (
                      <tr
                        key={q.id}
                        className={`hover:bg-gray-50 transition-colors ${
                          selectedQuestions.includes(q.id) ? 'bg-indigo-50' : ''
                        }`}
                      >
                        <td className="px-6 py-4">
                          <input
                            type="checkbox"
                            checked={selectedQuestions.includes(q.id)}
                            onChange={() => handleToggleQuestionSelection(q.id)}
                            className="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                          />
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-start gap-2">
                            <p className="text-sm text-gray-900 line-clamp-2 max-w-md">{q.text}</p>
                            {validationWarnings[q.id] && (
                              <div className="relative group">
                                <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full cursor-help">⚠️</span>
                                <div className="absolute right-full top-0 mr-2 bg-gray-900 text-white text-xs rounded-lg py-2 px-3 w-48 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10">
                                  <ul className="list-disc list-inside space-y-1">
                                    {validationWarnings[q.id].map((w, i) => (
                                      <li key={i}>{w}</li>
                                    ))}
                                  </ul>
                                </div>
                              </div>
                            )}
                          </div>
                          {/* Категории */}
                          {(q as any).category_ids && (q as any).category_ids.length > 0 && (
                            <div className="flex flex-wrap gap-1 mt-2">
                              {(q as any).category_ids.map((catId: number) => {
                                const cat = categories.find(c => c.id === catId)
                                return cat ? (
                                  <span
                                    key={catId}
                                    className="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full"
                                    title={cat.description || ''}
                                  >
                                    {cat.name}
                                  </span>
                                ) : null
                              })}
                            </div>
                          )}
                        </td>
                        <td className="px-6 py-4">
                          {(q as any).category_ids && (q as any).category_ids.length > 0 ? (
                            <div className="flex flex-wrap gap-1">
                              {(q as any).category_ids.slice(0, 3).map((catId: number) => {
                                const cat = categories.find(c => c.id === catId)
                                return cat ? (
                                  <span
                                    key={catId}
                                    className="text-xs bg-indigo-50 text-indigo-700 px-2 py-1 rounded-full font-medium"
                                    title={cat.description || ''}
                                  >
                                    {cat.name}
                                  </span>
                                ) : null
                              })}
                              {(q as any).category_ids.length > 3 && (
                                <span className="text-xs text-gray-500 px-1 py-1">
                                  +{(q as any).category_ids.length - 3}
                                </span>
                              )}
                            </div>
                          ) : (
                            <span className="text-xs text-gray-400 italic">Нет темы</span>
                          )}
                        </td>
                        <td className="px-6 py-4">
                          <span className="text-sm text-gray-600 font-medium">
                            {getProfessionName(q.profession_id)}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          {getTypeBadge(q.question_type)}
                        </td>
                        <td className="px-6 py-4">
                          {getDifficultyBadge(q.difficulty)}
                        </td>
                        <td className="px-6 py-4 text-right">
                          <div className="flex justify-end gap-2">
                            <button
                              onClick={() => handlePreview(q)}
                              className="text-purple-600 hover:text-purple-900 hover:bg-purple-50 p-2 rounded-lg transition-colors"
                              title="Предпросмотр (P)"
                            >
                              👁️
                            </button>
                            <button
                              onClick={() => handleDuplicateQuestion(q.id)}
                              className="text-gray-600 hover:text-gray-900 hover:bg-gray-100 p-2 rounded-lg transition-colors"
                              title="Дублировать"
                            >
                              📋
                            </button>
                            <button
                              onClick={() => openEditModal(q)}
                              className="text-indigo-600 hover:text-indigo-900 hover:bg-indigo-50 p-2 rounded-lg transition-colors"
                              title="Редактировать"
                            >
                              ✏️
                            </button>
                            <button
                              onClick={() => handleDeleteQuestion(q.id)}
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
                  <span className="font-medium text-gray-900">{Math.min(currentPage * itemsPerPage, filteredQuestions.length)}</span> из{' '}
                  <span className="font-medium text-gray-900">{filteredQuestions.length}</span>
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

      {/* Модальное окно редактора */}
      <Modal
        isOpen={isEditorOpen}
        onClose={() => {
          setIsEditorOpen(false)
          setEditingQuestion(null)
        }}
        title={editingQuestion ? '✏️ Редактировать вопрос' : '➕ Новый вопрос'}
      >
        <QuestionEditor
          question={editingQuestion}
          professions={professions}
          categories={categories}
          onSubmit={editingQuestion ? handleUpdateQuestion : handleCreateQuestion}
          onCancel={() => {
            setIsEditorOpen(false)
            setEditingQuestion(null)
          }}
        />
      </Modal>

      {/* Модальное окно добавления категории */}
      <AddCategoryModal
        isOpen={isAddCategoryOpen}
        onClose={() => setIsAddCategoryOpen(false)}
        onSuccess={() => {
          loadCategories()
          toast.success('Категория создана')
        }}
        professions={professions}
        professionId={selectedProfession ? parseInt(selectedProfession) : undefined}
      />

      {/* Модальное окно подтверждения удаления */}
      {isDeleteConfirmOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={() => setIsDeleteConfirmOpen(false)}>
          <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6" onClick={(e) => e.stopPropagation()}>
            <div className="text-center mb-6">
              <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                {isBulkDelete ? 'Массовое удаление' : 'Удаление вопроса'}
              </h3>
              <p className="text-gray-600">
                {isBulkDelete ? (
                  <>Вы уверены, что хотите удалить <span className="font-bold text-red-600">{selectedQuestions.length}</span> вопросов? Это действие нельзя отменить.</>
                ) : (
                  <>Вы уверены, что хотите удалить этот вопрос? Это действие нельзя отменить.</>
                )}
              </p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => {
                  setIsDeleteConfirmOpen(false)
                  setQuestionToDelete(null)
                }}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-xl font-semibold text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Отмена
              </button>
              <button
                onClick={() => {
                  if (isBulkDelete) {
                    handleBulkDelete()
                  } else {
                    handleConfirmDelete()
                  }
                }}
                className="flex-1 px-4 py-3 bg-red-600 text-white rounded-xl font-semibold hover:bg-red-700 transition-colors"
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Модальное окно импорта/экспорта */}
      <ImportExportModal
        isOpen={isImportExportOpen}
        onClose={() => setIsImportExportOpen(false)}
        professions={professions}
        onImportSuccess={() => {
          loadQuestions()
        }}
      />

      {/* Предпросмотр вопроса */}
      {previewQuestion && (
        <QuestionPreview
          question={previewQuestion}
          isOpen={!!previewQuestion}
          onClose={() => setPreviewQuestion(null)}
        />
      )}

      {/* Массовое изменение */}
      {isBulkActionsOpen && (
        <BulkActions
          selectedCount={selectedQuestions.length}
          professions={professions}
          onBulkChange={handleBulkChange}
          onCancel={() => setIsBulkActionsOpen(false)}
        />
      )}
    </div>
  )
}
