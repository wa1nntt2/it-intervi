import { useState } from 'react'
import { questionsApi } from '../../services/api'
import { Profession } from '../../types'

interface ImportExportModalProps {
  isOpen: boolean
  onClose: () => void
  professions: Profession[]
  onImportSuccess: () => void
}

interface Template {
  id: number
  name: string
  description: string
  template: any
}

export function ImportExportModal({ isOpen, onClose, professions, onImportSuccess }: ImportExportModalProps) {
  const [activeTab, setActiveTab] = useState<'export' | 'import' | 'templates'>('export')
  const [selectedProfession, setSelectedProfession] = useState<string>('')
  const [importFile, setImportFile] = useState<File | null>(null)
  const [importResult, setImportResult] = useState<any>(null)
  const [templates, setTemplates] = useState<Template[]>([])
  const [loading, setLoading] = useState(false)

  const handleExportJSON = async () => {
    try {
      const data = await questionsApi.exportJSON(selectedProfession ? parseInt(selectedProfession) : undefined)
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `questions_${new Date().toISOString().split('T')[0]}.json`
      link.click()
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Export failed:', error)
    }
  }

  const handleExportCSV = async () => {
    try {
      const data = await questionsApi.exportCSV(selectedProfession ? parseInt(selectedProfession) : undefined)
      const blob = new Blob([data], { type: 'text/csv;charset=utf-8;' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `questions_${new Date().toISOString().split('T')[0]}.csv`
      link.click()
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Export failed:', error)
    }
  }

  const handleImportJSON = async () => {
    if (!importFile) return
    setLoading(true)
    try {
      const result = await questionsApi.importJSON(importFile)
      setImportResult(result)
      onImportSuccess()
    } catch (error) {
      console.error('Import failed:', error)
      setImportResult({ error: 'Ошибка импорта' })
    } finally {
      setLoading(false)
    }
  }

  const handleImportCSV = async () => {
    if (!importFile) return
    setLoading(true)
    try {
      const result = await questionsApi.importCSV(importFile)
      setImportResult(result)
      onImportSuccess()
    } catch (error) {
      console.error('Import failed:', error)
      setImportResult({ error: 'Ошибка импорта' })
    } finally {
      setLoading(false)
    }
  }

  const handleLoadTemplates = async () => {
    try {
      const data = await questionsApi.getTemplates()
      setTemplates(data)
    } catch (error) {
      console.error('Failed to load templates:', error)
    }
  }

  const handleUseTemplate = (template: any) => {
    window.dispatchEvent(new CustomEvent('useTemplate', { detail: template }))
    onClose()
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black bg-opacity-50" onClick={onClose} />
      <div className="relative bg-white rounded-2xl shadow-xl max-w-3xl w-full max-h-[80vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b">
          <h3 className="text-xl font-bold text-gray-900">📦 Импорт / Экспорт</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-2xl">×</button>
        </div>

        <div className="flex border-b">
          <button
            onClick={() => { setActiveTab('export'); setImportResult(null) }}
            className={`flex-1 px-6 py-3 font-medium transition-colors ${
              activeTab === 'export'
                ? 'text-indigo-600 border-b-2 border-indigo-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            📤 Экспорт
          </button>
          <button
            onClick={() => { setActiveTab('import'); setImportResult(null) }}
            className={`flex-1 px-6 py-3 font-medium transition-colors ${
              activeTab === 'import'
                ? 'text-indigo-600 border-b-2 border-indigo-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            📥 Импорт
          </button>
          <button
            onClick={() => { setActiveTab('templates'); setImportResult(null); handleLoadTemplates() }}
            className={`flex-1 px-6 py-3 font-medium transition-colors ${
              activeTab === 'templates'
                ? 'text-indigo-600 border-b-2 border-indigo-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            📋 Шаблоны
          </button>
        </div>

        <div className="p-6">
          {activeTab === 'export' && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Фильтр по профессии
                </label>
                <select
                  value={selectedProfession}
                  onChange={(e) => setSelectedProfession(e.target.value)}
                  className="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">Все профессии</option>
                  {professions.map((p) => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={handleExportJSON}
                  className="flex flex-col items-center gap-2 p-6 border-2 border-indigo-200 rounded-xl hover:bg-indigo-50 transition-colors"
                >
                  <span className="text-4xl">📄</span>
                  <span className="font-medium text-indigo-700">JSON</span>
                  <span className="text-xs text-gray-500">Для импорта в систему</span>
                </button>
                <button
                  onClick={handleExportCSV}
                  className="flex flex-col items-center gap-2 p-6 border-2 border-green-200 rounded-xl hover:bg-green-50 transition-colors"
                >
                  <span className="text-4xl">📊</span>
                  <span className="font-medium text-green-700">CSV</span>
                  <span className="text-xs text-gray-500">Для Excel/Google Sheets</span>
                </button>
              </div>
            </div>
          )}

          {activeTab === 'import' && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Выберите файл
                </label>
                <div className="flex gap-4 mb-4">
                  <input
                    type="file"
                    accept=".json,.csv"
                    onChange={(e) => setImportFile(e.target.files?.[0] || null)}
                    className="flex-1 px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                {importFile && (
                  <p className="text-sm text-gray-600">
                    Выбран файл: <span className="font-medium">{importFile.name}</span>
                  </p>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={handleImportJSON}
                  disabled={!importFile || !importFile.name.endsWith('.json') || loading}
                  className="px-6 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? '⏳ Загрузка...' : '📄 Импорт JSON'}
                </button>
                <button
                  onClick={handleImportCSV}
                  disabled={!importFile || !importFile.name.endsWith('.csv') || loading}
                  className="px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? '⏳ Загрузка...' : '📊 Импорт CSV'}
                </button>
              </div>

              {importResult && (
                <div className={`p-4 rounded-xl ${importResult.error ? 'bg-red-50' : 'bg-green-50'}`}>
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">{importResult.error ? '❌' : '✅'}</span>
                    <div className="flex-1">
                      <p className={`font-medium ${importResult.error ? 'text-red-800' : 'text-green-800'}`}>
                        {importResult.message || importResult.error}
                      </p>
                      {!importResult.error && (
                        <p className="text-sm text-green-600 mt-1">
                          Создано: {importResult.created} | Ошибок: {importResult.errors}
                        </p>
                      )}
                      {importResult.error_details && importResult.error_details.length > 0 && (
                        <details className="mt-2">
                          <summary className="text-sm text-red-600 cursor-pointer">Ошибки ({importResult.errors})</summary>
                          <ul className="mt-2 text-sm text-red-700 space-y-1 max-h-40 overflow-y-auto">
                            {importResult.error_details.map((err: any, idx: number) => (
                              <li key={idx}>#{idx + 1}: {err.error}</li>
                            ))}
                          </ul>
                        </details>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'templates' && (
            <div className="space-y-4">
              {templates.length === 0 ? (
                <p className="text-center text-gray-500 py-8">Загрузка шаблонов...</p>
              ) : (
                templates.map((template) => (
                  <div
                    key={template.id}
                    className="p-4 border border-gray-200 rounded-xl hover:border-indigo-300 hover:bg-indigo-50 transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="font-semibold text-gray-900">{template.name}</h4>
                        <p className="text-sm text-gray-500 mt-1">{template.description}</p>
                      </div>
                      <button
                        onClick={() => handleUseTemplate(template.template)}
                        className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm font-medium"
                      >
                        Использовать
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
