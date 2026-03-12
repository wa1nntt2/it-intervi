interface DifficultyDistributionProps {
  intern: number
  junior: number
  middle: number
}

export function DifficultyDistribution({ intern, junior, middle }: DifficultyDistributionProps) {
  const total = intern + junior + middle
  const internPercent = total > 0 ? Math.round((intern / total) * 100) : 0
  const juniorPercent = total > 0 ? Math.round((junior / total) * 100) : 0
  const middlePercent = total > 0 ? Math.round((middle / total) * 100) : 0

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">📊 Распределение по сложности</h3>

      <div className="space-y-4">
        {/* Intern */}
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-green-500"></span>
              <span className="text-gray-600">Intern</span>
            </span>
            <span className="font-medium text-gray-900">{intern} ({internPercent}%)</span>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-3">
            <div
              className="h-3 rounded-full bg-gradient-to-r from-green-400 to-green-500 transition-all duration-500"
              style={{ width: `${internPercent}%` }}
            />
          </div>
        </div>

        {/* Junior */}
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-blue-500"></span>
              <span className="text-gray-600">Junior</span>
            </span>
            <span className="font-medium text-gray-900">{junior} ({juniorPercent}%)</span>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-3">
            <div
              className="h-3 rounded-full bg-gradient-to-r from-blue-400 to-blue-500 transition-all duration-500"
              style={{ width: `${juniorPercent}%` }}
            />
          </div>
        </div>

        {/* Middle */}
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-purple-500"></span>
              <span className="text-gray-600">Middle</span>
            </span>
            <span className="font-medium text-gray-900">{middle} ({middlePercent}%)</span>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-3">
            <div
              className="h-3 rounded-full bg-gradient-to-r from-purple-400 to-purple-500 transition-all duration-500"
              style={{ width: `${middlePercent}%` }}
            />
          </div>
        </div>
      </div>

      {/* Итого */}
      <div className="mt-6 pt-4 border-t border-gray-100">
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Всего вопросов</span>
          <span className="text-xl font-bold text-gray-900">{total}</span>
        </div>
      </div>
    </div>
  )
}
