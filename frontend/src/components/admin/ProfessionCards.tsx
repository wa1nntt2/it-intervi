import { Profession } from '../../types'
import { professionData } from '../../data/professions'

interface ProfessionCardsProps {
  professions: Profession[]
  questionCounts: Record<number, number>
  selectedProfession: string
  onChange: (value: string) => void
}

export function ProfessionCards({
  professions,
  questionCounts,
  selectedProfession,
  onChange
}: ProfessionCardsProps) {
  const totalQuestions = Object.values(questionCounts).reduce((a, b) => a + b, 0)

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Карточка "Все профессии" */}
      <button
        onClick={() => onChange('')}
        className={`group relative p-6 rounded-2xl border-2 transition-all duration-300 hover:shadow-lg ${
          selectedProfession === ''
            ? 'border-indigo-500 bg-indigo-50 shadow-md'
            : 'border-gray-200 bg-white hover:border-indigo-300'
        }`}
      >
        <div className="flex flex-col items-center text-center">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center text-3xl mb-3 group-hover:scale-110 transition-transform">
            📚
          </div>
          <h3 className="font-bold text-gray-900 mb-1">Все профессии</h3>
          <p className="text-2xl font-bold text-indigo-600">{totalQuestions}</p>
          <p className="text-xs text-gray-500 mt-1">вопросов всего</p>
        </div>
        {selectedProfession === '' && (
          <div className="absolute top-3 right-3 w-6 h-6 bg-indigo-500 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          </div>
        )}
      </button>

      {/* Карточки профессий */}
      {professions.map((profession) => {
        const profInfo = professionData[profession.id]
        const count = questionCounts[profession.id] || 0
        const isSelected = selectedProfession === profession.id.toString()
        const gradient = profInfo?.gradient || 'from-gray-500 to-gray-600'

        return (
          <button
            key={profession.id}
            onClick={() => onChange(profession.id.toString())}
            className={`group relative p-6 rounded-2xl border-2 transition-all duration-300 hover:shadow-lg ${
              isSelected
                ? 'border-indigo-500 bg-indigo-50 shadow-md'
                : 'border-gray-200 bg-white hover:border-indigo-300'
            }`}
          >
            <div className="flex flex-col items-center text-center">
              {/* Иконка с градиентом */}
              <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${gradient} flex items-center justify-center text-3xl mb-3 group-hover:scale-110 group-hover:shadow-lg transition-all duration-300`}>
                {profInfo?.icon || '📁'}
              </div>

              {/* Название */}
              <h3 className="font-bold text-gray-900 mb-1">{profession.name}</h3>

              {/* Описание */}
              <p className="text-xs text-gray-500 mb-3 line-clamp-2">
                {profInfo?.description || 'Описание недоступно'}
              </p>

              {/* Количество вопросов */}
              <div className="mt-auto">
                <p className="text-2xl font-bold text-indigo-600">{count}</p>
                <p className="text-xs text-gray-500">вопросов</p>
              </div>

              {/* Технологии */}
              {profInfo?.technologies && (
                <div className="flex gap-1 mt-3 flex-wrap justify-center">
                  {profInfo.technologies.slice(0, 2).map((tech, idx) => (
                    <span
                      key={idx}
                      className="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded-full"
                    >
                      {tech}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Индикатор выбора */}
            {isSelected && (
              <div className="absolute top-3 right-3 w-6 h-6 bg-indigo-500 rounded-full flex items-center justify-center shadow-md">
                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
            )}

            {/* Hover эффект */}
            <div className={`absolute inset-0 rounded-2xl bg-gradient-to-br ${gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-300`} />
          </button>
        )
      })}
    </div>
  )
}
