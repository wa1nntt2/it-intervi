import { useEffect } from 'react'
import { useToastStore, Toast } from '../../stores/toastStore'

const toastIcons: Record<string, string> = {
  success: '✓',
  error: '✕',
  info: 'ℹ',
  warning: '⚠',
}

const toastColors: Record<string, string> = {
  success: 'bg-green-500',
  error: 'bg-red-500',
  info: 'bg-blue-500',
  warning: 'bg-yellow-500',
}

export function ToastContainer() {
  const { toasts, removeToast } = useToastStore()

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 max-w-sm">
      {toasts.map((toastItem) => (
        <ToastItem key={toastItem.id} toast={toastItem} onClose={() => removeToast(toastItem.id)} />
      ))}
    </div>
  )
}

function ToastItem({ toast, onClose }: { toast: Toast; onClose: () => void }) {
  useEffect(() => {
    if (toast.duration && toast.duration > 0) {
      const timer = setTimeout(onClose, toast.duration)
      return () => clearTimeout(timer)
    }
  }, [toast.duration, onClose])

  const colorClass = toastColors[toast.type] || toastColors.info

  return (
    <div
      className={`${colorClass} text-white px-4 py-3 rounded-lg shadow-lg flex items-center justify-between gap-3 animate-slide-in`}
      role="alert"
    >
      <div className="flex items-center gap-2">
        <span className="text-xl font-bold">{toastIcons[toast.type]}</span>
        <span className="text-sm font-medium">{toast.message}</span>
      </div>
      <button
        onClick={onClose}
        className="text-white/80 hover:text-white transition-colors text-lg leading-none"
        aria-label="Закрыть уведомление"
      >
        ×
      </button>
    </div>
  )
}
