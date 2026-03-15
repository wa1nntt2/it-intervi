import { useDarkMode } from '../../hooks/useDarkMode'

interface ThemeToggleProps {
  className?: string
}

export function ThemeToggle({ className = '' }: ThemeToggleProps) {
  const { isDark, toggle } = useDarkMode()

  return (
    <button
      onClick={toggle}
      className={`p-2 rounded-lg bg-white/20 backdrop-blur-sm hover:bg-white/30 transition-all ${className}`}
      title={isDark ? 'Светлая тема' : 'Темная тема'}
    >
      {isDark ? (
        <span className="text-xl">☀️</span>
      ) : (
        <span className="text-xl">🌙</span>
      )}
    </button>
  )
}
