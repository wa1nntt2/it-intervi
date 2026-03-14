import React, { useState } from 'react'
import { Profession } from '../../types'
import { interviewsApi } from '../../services/api'

interface AddCategoryModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
  professions: Profession[]
  professionId?: number
}

export function AddCategoryModal({ isOpen, onClose, onSuccess, professions, professionId }: AddCategoryModalProps) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [selectedProfession, setSelectedProfession] = useState(professionId?.toString() || '')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name || !selectedProfession) {
      alert('Введите название и выберите профессию')
      return
    }

    setLoading(true)
    try {
      await interviewsApi.createCategory({
        name,
        description: description || undefined,
        profession_id: parseInt(selectedProfession),
      })
      onSuccess()
      setName('')
      setDescription('')
      setSelectedProfession('')
      onClose()
    } catch (error: any) {
      alert(error.message || 'Ошибка при создании категории')
    } finally {
      setLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6" onClick={(e) => e.stopPropagation()}>
        <h2 className="text-xl font-bold text-gray-900 mb-4">🏷️ Новая категория</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Название категории *
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-indigo-500"
              placeholder="Например: Ansible, Other, Cloud"
              autoFocus
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Профессия *
            </label>
            <select
              value={selectedProfession}
              onChange={(e) => setSelectedProfession(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">Выберите профессию</option>
              {professions.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Описание (опционально)
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-indigo-500"
              rows={3}
              placeholder="Краткое описание категории..."
            />
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              disabled={loading}
            >
              Отмена
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
            >
              {loading ? 'Создание...' : '✓ Создать'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
