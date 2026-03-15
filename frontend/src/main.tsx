/**
 * Точка входа React приложения.
 * Рендерит корневой компонент App в DOM элемент с id="root".
 */

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import { ToastContainer } from './components/ui/Toast.tsx'
import './index.css'

// Инициализация темы при загрузке
const initializeTheme = () => {
  const savedTheme = localStorage.getItem('theme')
  
  // По умолчанию светлая тема, если не сохранено предпочтение
  if (savedTheme === 'dark') {
    document.documentElement.classList.add('dark')
  } else {
    // Явно удаляем класс dark если тема светлая или не сохранена
    document.documentElement.classList.remove('dark')
  }
}

initializeTheme()

// Рендеринг приложения в StrictMode для выявления потенциальных проблем
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
    <ToastContainer />
  </React.StrictMode>,
)
