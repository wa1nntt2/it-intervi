import React from 'react'

interface QuestionFormProps {
  onSubmit: (data: any) => void
  professions: any[]
}

export function QuestionForm({ onSubmit, professions }: QuestionFormProps) {
  const [formData, setFormData] = React.useState({
    text: '',
    question_type: 'mcq' as 'mcq' | 'ordering',
    profession_id: '',
    difficulty: 'medium' as 'easy' | 'medium' | 'hard',
    options: ['', '', '', ''],
    correct_option: 0,
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-gray-700 mb-2">Текст вопроса</label>
        <input
          type="text"
          value={formData.text}
          onChange={(e) => setFormData({ ...formData, text: e.target.value })}
          className="w-full border border-gray-300 rounded px-3 py-2"
          required
        />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-gray-700 mb-2">Тип</label>
          <select
            value={formData.question_type}
            onChange={(e) => setFormData({ ...formData, question_type: e.target.value as 'mcq' | 'ordering' })}
            className="w-full border border-gray-300 rounded px-3 py-2"
          >
            <option value="mcq">Один вариант</option>
            <option value="ordering">Порядок</option>
          </select>
        </div>
        <div>
          <label className="block text-gray-700 mb-2">Сложность</label>
          <select
            value={formData.difficulty}
            onChange={(e) => setFormData({ ...formData, difficulty: e.target.value as 'easy' | 'medium' | 'hard' })}
            className="w-full border border-gray-300 rounded px-3 py-2"
          >
            <option value="easy">Легкий</option>
            <option value="medium">Средний</option>
            <option value="hard">Сложный</option>
          </select>
        </div>
      </div>
      <div>
        <label className="block text-gray-700 mb-2">Профессия</label>
        <select
          value={formData.profession_id}
          onChange={(e) => setFormData({ ...formData, profession_id: e.target.value })}
          className="w-full border border-gray-300 rounded px-3 py-2"
          required
        >
          <option value="">Выберите профессию</option>
          {professions.map((p) => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
      </div>
      <button type="submit" className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700">
        Создать вопрос
      </button>
    </form>
  )
}
