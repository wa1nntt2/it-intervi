import { Profession } from '../../types'

interface BulkActionsProps {
  selectedCount: number
  professions: Profession[]
  onBulkChange: (updates: { profession_id?: number; difficulty?: string }) => void
  onCancel: () => void
}

export function BulkActions({ selectedCount, professions, onBulkChange, onCancel }: BulkActionsProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const form = e.target as HTMLFormElement
    const formData = new FormData(form)
    const updates: { profession_id?: number; difficulty?: string } = {}
    
    if (formData.get('profession_id')) {
      updates.profession_id = parseInt(formData.get('profession_id') as string)
    }
    if (formData.get('difficulty')) {
      updates.difficulty = formData.get('difficulty') as string
    }
    
    onBulkChange(updates)
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6">
        <div className="text-center mb-6">
          <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-3xl">⚡</span>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">Массовое изменение</h3>
          <p className="text-gray-600">
            Изменить <span className="font-bold text-indigo-600">{selectedCount}</span> вопросов
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Профессия (необязательно)
            </label>
            <select name="profession_id" className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500">
              <option value="">Не менять</option>
              {professions.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Сложность (необязательно)
            </label>
            <select name="difficulty" className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500">
              <option value="">Не менять</option>
              <option value="intern">🌱 Intern</option>
              <option value="junior">📚 Junior</option>
              <option value="middle">💼 Middle</option>
            </select>
          </div>

          <div className="flex gap-3 pt-4">
            <button type="button" onClick={onCancel} className="flex-1 px-4 py-3 border border-gray-300 rounded-xl font-semibold text-gray-700 hover:bg-gray-50 transition-colors">
              Отмена
            </button>
            <button type="submit" className="flex-1 px-4 py-3 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition-colors">
              Применить
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
