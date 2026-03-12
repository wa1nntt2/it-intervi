import { Profession } from '../../types'

interface ProfessionDistributionProps {
  professions: Profession[]
  questions: any[]
}

const colors = [
  'from-indigo-500 to-indigo-600',
  'from-purple-500 to-purple-600',
  'from-pink-500 to-pink-600',
  'from-blue-500 to-blue-600',
  'from-cyan-500 to-cyan-600',
  'from-teal-500 to-teal-600',
  'from-green-500 to-green-600',
  'from-yellow-500 to-yellow-600',
]

export function ProfessionDistribution({ professions, questions }: ProfessionDistributionProps) {
  const professionStats = professions.map((p, index) => {
    const count = questions.filter((q) => q.profession_id === p.id).length
    const total = questions.length
    const percent = total > 0 ? Math.round((count / total) * 100) : 0
    return {
      ...p,
      count,
      percent,
      color: colors[index % colors.length],
    }
  }).sort((a, b) => b.count - a.count)

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">📚 Распределение по профессиям</h3>
      
      <div className="space-y-3">
        {professionStats.map((prof) => (
          <div key={prof.id} className="group">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-700 font-medium">{prof.name}</span>
              <span className="text-gray-500">{prof.count} ({prof.percent}%)</span>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-2.5">
              <div
                className={`h-2.5 rounded-full bg-gradient-to-r ${prof.color} transition-all duration-500 group-hover:opacity-80`}
                style={{ width: `${prof.percent}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 pt-4 border-t border-gray-100">
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Всего профессий</span>
          <span className="text-xl font-bold text-gray-900">{professions.length}</span>
        </div>
      </div>
    </div>
  )
}
