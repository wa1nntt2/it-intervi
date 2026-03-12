import { useState } from 'react'
import { Profession } from '../../types'
import { professionData } from '../../data/professions'

interface ProfessionDropdownProps {
  professions: Profession[]
  questionCounts: Record<number, number>
  selectedProfession: string
  onChange: (value: string) => void
  placeholder?: string
}

export function ProfessionDropdown({
  professions,
  questionCounts,
  selectedProfession,
  onChange,
  placeholder = 'Выберите профессию'
}: ProfessionDropdownProps) {
  const [isOpen, setIsOpen] = useState(false)

  const selectedId = selectedProfession ? parseInt(selectedProfession) : null
  const selectedProf = selectedId ? professionData[selectedId] : null

  return (
    <div className="relative">
      {/* Кнопка dropdown */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-4 py-3 bg-white border border-gray-200 rounded-xl hover:border-indigo-300 focus:ring-2 focus:ring-indigo-500 transition-all"
      >
        <div className="flex items-center gap-3">
          {selectedProf ? (
            <>
              <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${selectedProf.gradient} flex items-center justify-center text-xl shadow-md`}>
                {selectedProf.icon}
              </div>
              <div className="text-left">
                <p className="font-semibold text-gray-900">{selectedProf.name}</p>
                <p className="text-xs text-gray-500">{selectedProf.description}</p>
              </div>
            </>
          ) : (
            <>
              <div className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center text-xl">
                📁
              </div>
              <p className="text-gray-500">{placeholder}</p>
            </>
          )}
        </div>
        <svg
          className={`w-5 h-5 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Выпадающий список */}
      {isOpen && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setIsOpen(false)} />
          <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-xl z-20 max-h-80 overflow-y-auto">
            {/* Опция "Все профессии" */}
            <button
              onClick={() => { onChange(''); setIsOpen(false) }}
              className={`w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors ${
                !selectedProfession ? 'bg-indigo-50' : ''
              }`}
            >
              <div className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center text-xl">
                📚
              </div>
              <div className="flex-1 text-left">
                <p className="font-semibold text-gray-900">Все профессии</p>
                <p className="text-xs text-gray-500">
                  {Object.values(questionCounts).reduce((a, b) => a + b, 0)} вопросов
                </p>
              </div>
            </button>

            {/* Профессии */}
            {professions.map((profession) => {
              const profInfo = professionData[profession.id]
              const count = questionCounts[profession.id] || 0
              const isSelected = selectedProfession === profession.id.toString()

              return (
                <button
                  key={profession.id}
                  onClick={() => { onChange(profession.id.toString()); setIsOpen(false) }}
                  className={`w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors ${
                    isSelected ? 'bg-indigo-50' : ''
                  }`}
                >
                  <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${profInfo?.gradient || 'from-gray-500 to-gray-600'} flex items-center justify-center text-xl shadow-md`}>
                    {profInfo?.icon || '📁'}
                  </div>
                  <div className="flex-1 text-left">
                    <div className="flex items-center justify-between">
                      <p className="font-semibold text-gray-900">{profession.name}</p>
                      <span className="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                        {count} вопр.
                      </span>
                    </div>
                    <p className="text-xs text-gray-500">{profInfo?.description || 'Описание недоступно'}</p>
                    {profInfo?.technologies && (
                      <div className="flex gap-1 mt-1 flex-wrap">
                        {profInfo.technologies.slice(0, 3).map((tech, idx) => (
                          <span key={idx} className="text-xs text-indigo-600 bg-indigo-50 px-1.5 py-0.5 rounded">
                            {tech}
                          </span>
                        ))}
                        {profInfo.technologies.length > 3 && (
                          <span className="text-xs text-gray-400">+{profInfo.technologies.length - 3}</span>
                        )}
                      </div>
                    )}
                  </div>
                </button>
              )
            })}
          </div>
        </>
      )}
    </div>
  )
}
