import { useState } from 'react'

interface OrderingQuestionProps {
  question: {
    id: number
    text: string
    options: string[]
  }
  onOrderChange: (order: number[]) => void
}

export function OrderingQuestion({ question, onOrderChange }: OrderingQuestionProps) {
  const [order, setOrder] = useState<number[]>(question.options.map((_, i) => i))

  const moveItem = (index: number, direction: 'up' | 'down') => {
    const newIndex = direction === 'up' ? index - 1 : index + 1
    if (newIndex < 0 || newIndex >= order.length) return

    const newOrder = [...order]
    ;[newOrder[index], newOrder[newIndex]] = [newOrder[newIndex], newOrder[index]]
    setOrder(newOrder)
    onOrderChange(newOrder)
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">{question.text}</h2>
      <p className="text-gray-600 mb-4">Расположите варианты в правильном порядке:</p>
      <div className="space-y-2">
        {order.map((optionIndex, position) => (
          <div key={optionIndex} className="flex items-center gap-4">
            <span className="text-gray-500 w-6">{position + 1}.</span>
            <div className="flex-1 p-3 bg-gray-50 rounded border">
              {question.options[optionIndex]}
            </div>
            <div className="flex gap-1">
              <button
                onClick={() => moveItem(position, 'up')}
                disabled={position === 0}
                className="px-2 py-1 border rounded hover:bg-gray-100 disabled:opacity-50"
              >
                ↑
              </button>
              <button
                onClick={() => moveItem(position, 'down')}
                disabled={position === order.length - 1}
                className="px-2 py-1 border rounded hover:bg-gray-100 disabled:opacity-50"
              >
                ↓
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
