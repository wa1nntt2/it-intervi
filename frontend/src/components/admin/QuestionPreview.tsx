import { Question } from '../../types'

interface QuestionPreviewProps {
  question: Question
  isOpen: boolean
  onClose: () => void
}

export function QuestionPreview({ question, isOpen, onClose }: QuestionPreviewProps) {
  if (!isOpen) return null

  const difficultyColors: Record<string, string> = {
    'intern': 'bg-green-500',
    'junior': 'bg-blue-500',
    'middle': 'bg-purple-500'
  }

  const difficultyLabels: Record<string, string> = {
    'intern': '🌱 Intern',
    'junior': '📚 Junior',
    'middle': '💼 Middle'
  }

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-8">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-bold text-white">📋 Предпросмотр вопроса</h3>
            <button onClick={onClose} className="text-white/70 hover:text-white hover:bg-white/20 rounded-lg p-2 transition-colors">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 mb-6">
            <div className="flex flex-wrap gap-2 mb-4">
              <span className={`px-3 py-1 rounded-full text-xs font-bold text-white ${difficultyColors[question.difficulty]}`}>
                {difficultyLabels[question.difficulty]}
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-bold text-white bg-indigo-500">
                {question.question_type === 'mcq' ? '📝 Multiple Choice' : '🔂 Упорядочивание'}
              </span>
            </div>

            <h4 className="text-xl font-bold text-white mb-6 leading-relaxed">{question.text}</h4>

            {question.question_type === 'mcq' ? (
              <div className="space-y-3">
                {question.options.map((option, index) => {
                  const isCorrect = index === question.correct_option
                  return (
                    <div key={index} className={`p-4 rounded-xl border-2 ${isCorrect ? 'bg-green-500/20 border-green-400' : 'bg-white/10 border-white/20'}`}>
                      <div className="flex items-center gap-3">
                        <span className={`w-8 h-8 flex items-center justify-center rounded-full font-bold text-sm ${isCorrect ? 'bg-green-500 text-white' : 'bg-white/20 text-white'}`}>
                          {String.fromCharCode(65 + index)}
                        </span>
                        <span className="flex-1 text-white font-medium">{option}</span>
                        {isCorrect && <span className="text-2xl">✅</span>}
                      </div>
                    </div>
                  )
                })}
              </div>
            ) : (
              <div className="space-y-2">
                <p className="text-white/70 text-sm mb-3">🔂 Расположите в правильном порядке:</p>
                {question.options.map((option, index) => (
                  <div key={index} className="p-3 rounded-xl bg-white/10 border border-white/20 flex items-center gap-3">
                    <span className="w-8 h-8 flex items-center justify-center bg-indigo-500 text-white rounded-full font-bold">{index + 1}</span>
                    <span className="flex-1 text-white">{option}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {question.explanation && (
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6">
              <h5 className="text-sm font-bold text-white/70 uppercase mb-3 flex items-center gap-2">
                <span className="text-xl">💡</span> Пояснение
              </h5>
              <p className="text-white/90 leading-relaxed whitespace-pre-line">{question.explanation}</p>
            </div>
          )}

          <div className="mt-6 flex justify-end">
            <button onClick={onClose} className="px-6 py-3 bg-white text-indigo-600 rounded-xl font-bold hover:bg-yellow-300 transition-all hover:scale-105">
              Закрыть
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
