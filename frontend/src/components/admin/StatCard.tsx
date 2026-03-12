import React from 'react'

interface StatCardProps {
  title: string
  value: string | number
  icon?: React.ReactNode
  trend?: {
    value: number
    isPositive: boolean
  }
  color?: 'indigo' | 'green' | 'yellow' | 'red' | 'blue' | 'purple' | 'pink' | 'cyan'
  subtitle?: string
  progress?: number
}

export function StatCard({ title, value, icon, trend, color = 'indigo', subtitle, progress }: StatCardProps) {
  const colorClasses = {
    indigo: { bg: 'bg-indigo-500', light: 'bg-indigo-100', text: 'text-indigo-600', gradient: 'from-indigo-500 to-indigo-600' },
    green: { bg: 'bg-green-500', light: 'bg-green-100', text: 'text-green-600', gradient: 'from-green-500 to-green-600' },
    yellow: { bg: 'bg-yellow-500', light: 'bg-yellow-100', text: 'text-yellow-600', gradient: 'from-yellow-500 to-yellow-600' },
    red: { bg: 'bg-red-500', light: 'bg-red-100', text: 'text-red-600', gradient: 'from-red-500 to-red-600' },
    blue: { bg: 'bg-blue-500', light: 'bg-blue-100', text: 'text-blue-600', gradient: 'from-blue-500 to-blue-600' },
    purple: { bg: 'bg-purple-500', light: 'bg-purple-100', text: 'text-purple-600', gradient: 'from-purple-500 to-purple-600' },
    pink: { bg: 'bg-pink-500', light: 'bg-pink-100', text: 'text-pink-600', gradient: 'from-pink-500 to-pink-600' },
    cyan: { bg: 'bg-cyan-500', light: 'bg-cyan-100', text: 'text-cyan-600', gradient: 'from-cyan-500 to-cyan-600' },
  }

  const theme = colorClasses[color]

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
      <div className="flex items-start justify-between mb-4">
        <div className={`${theme.light} p-3 rounded-xl`}>
          <div className={theme.text}>{icon}</div>
        </div>
        {trend && (
          <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${
            trend.isPositive ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
          }`}>
            {trend.isPositive ? '↑' : '↓'} {trend.value}%
          </div>
        )}
      </div>
      
      <div>
        <p className="text-gray-500 text-sm font-medium mb-1">{title}</p>
        <div className="flex items-baseline gap-2">
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          {subtitle && <span className="text-sm text-gray-400">{subtitle}</span>}
        </div>
      </div>

      {progress !== undefined && (
        <div className="mt-4">
          <div className="flex justify-between text-xs mb-1">
            <span className="text-gray-500">Прогресс</span>
            <span className="font-medium text-gray-700">{progress}%</span>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-2">
            <div
              className={`h-2 rounded-full bg-gradient-to-r ${theme.gradient} transition-all duration-500`}
              style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
            />
          </div>
        </div>
      )}
    </div>
  )
}
