interface QuestionCardProps {
  question: {
    id: number
    text: string
    question_type: string
    difficulty: string
    options: string[]
  }
  selectedAnswer: number | null
  onAnswer: (optionIndex: number) => void
}

export function QuestionCard({ question, selectedAnswer, onAnswer }: QuestionCardProps) {
  const difficultyColors: Record<string, string> = {
    easy: 'bg-green-100 text-green-700',
    medium: 'bg-yellow-100 text-yellow-700',
    hard: 'bg-red-100 text-red-700',
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <div className="mb-4 flex items-center gap-2">
        <span className={`px-2 py-1 rounded text-xs ${difficultyColors[question.difficulty]}`}>
          {question.difficulty}
        </span>
        <span className="text-sm text-gray-500">{question.question_type}</span>
      </div>
      <h2 className="text-xl font-semibold text-gray-900 mb-6">{question.text}</h2>
      <div className="space-y-3">
        {question.options.map((option, index) => (
          <button
            key={index}
            onClick={() => onAnswer(index)}
            className={`w-full text-left p-4 rounded border ${
              selectedAnswer === index
                ? 'border-indigo-600 bg-indigo-50'
                : 'border-gray-300 hover:bg-gray-50'
            }`}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  )
}
