import React, { useState, useEffect } from 'react'
import { Question, Profession } from '../../types'

interface QuestionEditorProps {
  question?: Question | null
  professions: Profession[]
  onSubmit: (data: QuestionFormData) => void
  onCancel: () => void
}

interface QuestionFormData {
  text: string
  question_type: 'mcq' | 'ordering'
  profession_id: string
  difficulty: 'intern' | 'junior' | 'middle'
  options: string[]
  correct_option: number | null
  correct_order: number[] | null
}

export function QuestionEditor({ question, professions, onSubmit, onCancel }: QuestionEditorProps) {
  const [formData, setFormData] = useState<QuestionFormData>({
    text: '',
    question_type: 'mcq',
    profession_id: '',
    difficulty: 'junior',
    options: ['', '', '', ''],
    correct_option: null,
    correct_order: null,
  })

  useEffect(() => {
    if (question) {
      setFormData({
        text: question.text,
        question_type: question.question_type,
        profession_id: question.profession_id.toString(),
        difficulty: question.difficulty,
        options: question.options,
        correct_option: question.correct_option,
        correct_order: (question as any).correct_order || null,
      })
    }
  }, [question])

  // Обработка использования шаблона
  useEffect(() => {
    const handleUseTemplate = (event: CustomEvent) => {
      const template = event.detail
      setFormData({
        text: template.text || '',
        question_type: template.question_type || 'mcq',
        profession_id: '',
        difficulty: template.difficulty || 'junior',
        options: template.options || ['', '', '', ''],
        correct_option: template.correct_option ?? 0,
        correct_order: template.correct_order || null,
      })
    }

    window.addEventListener('useTemplate', handleUseTemplate as EventListener)
    return () => window.removeEventListener('useTemplate', handleUseTemplate as EventListener)
  }, [])

  const handleOptionChange = (index: number, value: string) => {
    const newOptions = [...formData.options]
    newOptions[index] = value
    setFormData({ ...formData, options: newOptions })
  }

  const handleAddOption = () => {
    setFormData({ ...formData, options: [...formData.options, ''] })
  }

  const handleRemoveOption = (index: number) => {
    if (formData.options.length <= 2) return
    const newOptions = formData.options.filter((_, i) => i !== index)
    setFormData({ 
      ...formData, 
      options: newOptions,
      correct_option: formData.correct_option !== null && formData.correct_option >= index 
        ? Math.max(0, formData.correct_option - 1)
        : formData.correct_option
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Текст вопроса */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Текст вопроса <span className="text-red-500">*</span>
        </label>
        <textarea
          value={formData.text}
          onChange={(e) => setFormData({ ...formData, text: e.target.value })}
          className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          rows={3}
          required
          placeholder="Введите текст вопроса..."
        />
      </div>

      {/* Тип и сложность */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Тип вопроса <span className="text-red-500">*</span>
          </label>
          <select
            value={formData.question_type}
            onChange={(e) => setFormData({ ...formData, question_type: e.target.value as 'mcq' | 'ordering' })}
            className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-indigo-500"
          >
            <option value="mcq">Multiple Choice (MCQ)</option>
            <option value="ordering">Упорядочивание</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Сложность <span className="text-red-500">*</span>
          </label>
          <select
            value={formData.difficulty}
            onChange={(e) => setFormData({ ...formData, difficulty: e.target.value as 'intern' | 'junior' | 'middle' })}
            className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-indigo-500"
          >
            <option value="intern">🌱 Intern</option>
            <option value="junior">📚 Junior</option>
            <option value="middle">💼 Middle</option>
          </select>
        </div>
      </div>

      {/* Профессия */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Профессия <span className="text-red-500">*</span>
        </label>
        <select
          value={formData.profession_id}
          onChange={(e) => setFormData({ ...formData, profession_id: e.target.value })}
          className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-indigo-500"
          required
        >
          <option value="">Выберите профессию</option>
          {professions.map((p) => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
      </div>

      {/* Варианты ответов */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          {formData.question_type === 'mcq' ? 'Варианты ответов' : 'Элементы для упорядочивания'}
          <span className="text-red-500">*</span>
        </label>
        <div className="space-y-3">
          {formData.options.map((option, index) => (
            <div key={index} className="flex items-center gap-3">
              {formData.question_type === 'mcq' && (
                <input
                  type="radio"
                  name="correct_option"
                  checked={formData.correct_option === index}
                  onChange={() => setFormData({ ...formData, correct_option: index })}
                  className="w-4 h-4 text-indigo-600"
                />
              )}
              <span className="text-gray-500 w-6">{index + 1}.</span>
              <input
                type="text"
                value={option}
                onChange={(e) => handleOptionChange(index, e.target.value)}
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500"
                placeholder={formData.question_type === 'mcq' ? `Вариант ${index + 1}` : `Элемент ${index + 1}`}
                required
              />
              <button
                type="button"
                onClick={() => handleRemoveOption(index)}
                className="text-red-500 hover:text-red-700 p-2"
                disabled={formData.options.length <= 2}
              >
                🗑️
              </button>
            </div>
          ))}
        </div>
        <button
          type="button"
          onClick={handleAddOption}
          className="mt-3 text-indigo-600 hover:text-indigo-800 text-sm font-medium"
        >
          + Добавить вариант
        </button>
        {formData.question_type === 'mcq' && (
          <p className="mt-2 text-sm text-gray-500">
            💡 Выберите правильный ответ, нажав на радио-кнопку слева
          </p>
        )}
        {formData.question_type === 'ordering' && (
          <p className="mt-2 text-sm text-gray-500">
            💡 Для вопросов на упорядочивание правильный порядок задается последовательностью элементов
          </p>
        )}
      </div>

      {/* Кнопки действий */}
      <div className="flex justify-end gap-3 pt-6 border-t">
        <button
          type="button"
          onClick={onCancel}
          className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
        >
          Отмена
        </button>
        <button
          type="submit"
          className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
        >
          {question ? 'Сохранить изменения' : 'Создать вопрос'}
        </button>
      </div>
    </form>
  )
}
