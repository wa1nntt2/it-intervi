import { useEffect, useState } from 'react'

/**
 * Хук для управления темной темой.
 * Сохраняет предпочтение в localStorage.
 */
export function useDarkMode() {
  const [isDark, setIsDark] = useState(() => {
    // Проверяем localStorage или системные настройки
    if (typeof window === 'undefined') return false
    
    const saved = localStorage.getItem('theme')
    if (saved) {
      return saved === 'dark'
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  })

  useEffect(() => {
    const root = window.document.documentElement
    
    console.log('useDarkMode: isDark =', isDark, 'Adding class:', isDark)
    
    if (isDark) {
      root.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      root.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }, [isDark])

  const toggle = () => {
    console.log('useDarkMode: toggle called')
    setIsDark(prev => !prev)
  }

  return { isDark, toggle }
}
