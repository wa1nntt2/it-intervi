import React, { useState, useEffect } from 'react'
import { Profession, Category } from '../../types'
import { interviewsApi } from '../../services/api'

interface CategoryManagerProps {
  professions: Profession[]
  categories: Category[]
  onCategoriesChange: () => void
}

export function CategoryManager({ professions, categories, onCategoriesChange }: CategoryManagerProps) {
  const [isAdding, setIsAdding] = useState(false)
  const [newCategory, setNewCategory] = useState({
    name: '',
    description: '',
    profession_id: '',
  })
  const [editingCategory, setEditingCategory] = useState<Category | null>(null)

  const handleAddCategory = async () => {
    if (!newCategory.name || !newCategory.profession_id) {
      alert('Введите название и выберите профессию')
      return
    }

    try {
      // Создаём категорию через API (нужно добавить endpoint)
      const response = await fetch('/api/categories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newCategory),
      })

      if (!response.ok) throw new Error('Failed to create category')
      
      onCategoriesChange()
      setIsAdding(false)
      setNewCategory({ name: '', description: '', profession_id: '' })
    } catch (error) {
      console.error('Error creating category:', error)
      alert('Ошибка при создании категории')
    }
  }

  const handleDeleteCategory = async (id: number) => {
    if (!confirm('Удалить эту категорию? Вопросы не будут удалены.')) return

    try {
      const response = await fetch(`/api/categories/${id}`, {
        method: 'DELETE',
      })

      if (!response.ok) throw new Error('Failed to delete category')
      
      onCategoriesChange()
    } catch (error) {
      console.error('Error deleting category:', error)
      alert('Ошибка при удалении категории')
    }
  }

  const handleEditCategory = async () => {
    if (!editingCategory) return

    try {
      const response = await fetch(`/api/categories/${editingCategory.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editingCategory),
      })

      if (!response.ok) throw new Error('Failed to update category')
      
      onCategoriesChange()
      setEditingCategory(null)
    } catch (error) {
      console.error('Error updating category:', error)
      alert('Ошибка при обновлении категории')
    }
  }

  // Группируем категории по профессиям
  const groupedCategories: Record<number, Category[]> = {}
  categories.forEach(cat => {
    if (!groupedCategories[cat.profession_id]) {
      groupedCategories[cat.profession_id] = []
    }
    groupedCategories[cat.profession_id].push(cat)
  })

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
            <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
          </div>
          <div>
            <h2 className="text-lg font-bold text-gray-900">Категории вопросов</h2>
            <p className="text-sm text-gray-500">Управление темами для вопросов</p>
          </div>
        </div>
        <button
          onClick={() => setIsAdding(!isAdding)}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm font-medium transition-colors"
        >
          {isAdding ? '✕ Отмена' : '+ Добавить категорию'}
        </button>
      </div>

      {/* Форма добавления */}
      {isAdding && (
        <div className="bg-gray-50 rounded-xl p-4 mb-6">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Новая категория</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Название *
              </label>
              <input
                type="text"
                value={newCategory.name}
                onChange={(e) => setNewCategory({ ...newCategory, name: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500"
                placeholder="Например: Ansible"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Профессия *
              </label>
              <select
                value={newCategory.profession_id}
                onChange={(e) => setNewCategory({ ...newCategory, profession_id: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">Выберите профессию</option>
                {professions.map((p) => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Описание
              </label>
              <input
                type="text"
                value={newCategory.description}
                onChange={(e) => setNewCategory({ ...newCategory, description: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500"
                placeholder="Краткое описание"
              />
            </div>
          </div>
          <button
            onClick={handleAddCategory}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm font-medium"
          >
            ✓ Создать категорию
          </button>
        </div>
      )}

      {/* Список категорий по профессиям */}
      <div className="space-y-6">
        {professions.map((profession) => {
          const profCategories = groupedCategories[profession.id] || []
          if (profCategories.length === 0 && !isAdding) return null

          return (
            <div key={profession.id}>
              <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <span className="text-lg">{profession.name.split(' ')[0] === 'Frontend' ? '🎨' :
                                        profession.name.split(' ')[0] === 'Backend' ? '⚙️' :
                                        profession.name.split(' ')[0] === 'Fullstack' ? '🚀' : '🔧'}</span>
                {profession.name}
                <span className="text-xs text-gray-400">({profCategories.length})</span>
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {profCategories.map((category) => (
                  <div
                    key={category.id}
                    className="bg-white border border-gray-200 rounded-lg p-3 hover:border-indigo-300 transition-colors group"
                  >
                    {editingCategory?.id === category.id ? (
                      <div className="space-y-2">
                        <input
                          type="text"
                          value={editingCategory.name}
                          onChange={(e) => setEditingCategory({ ...editingCategory, name: e.target.value })}
                          className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                        />
                        <input
                          type="text"
                          value={editingCategory.description || ''}
                          onChange={(e) => setEditingCategory({ ...editingCategory, description: e.target.value })}
                          className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                          placeholder="Описание"
                        />
                        <div className="flex gap-2">
                          <button
                            onClick={handleEditCategory}
                            className="flex-1 px-2 py-1 bg-green-600 text-white rounded text-xs"
                          >
                            Сохранить
                          </button>
                          <button
                            onClick={() => setEditingCategory(null)}
                            className="flex-1 px-2 py-1 bg-gray-300 text-gray-700 rounded text-xs"
                          >
                            Отмена
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div>
                        <div className="flex items-start justify-between mb-2">
                          <h4 className="text-sm font-medium text-gray-900">{category.name}</h4>
                          <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button
                              onClick={() => setEditingCategory(category)}
                              className="p-1 text-indigo-600 hover:bg-indigo-50 rounded"
                              title="Редактировать"
                            >
                              ✏️
                            </button>
                            <button
                              onClick={() => handleDeleteCategory(category.id)}
                              className="p-1 text-red-600 hover:bg-red-50 rounded"
                              title="Удалить"
                            >
                              🗑️
                            </button>
                          </div>
                        </div>
                        {category.description && (
                          <p className="text-xs text-gray-500 line-clamp-2">{category.description}</p>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
              {profCategories.length === 0 && (
                <p className="text-sm text-gray-400 italic">Нет категорий для этой профессии</p>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
