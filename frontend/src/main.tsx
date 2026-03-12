/**
 * Точка входа React приложения.
 * Рендерит корневой компонент App в DOM элемент с id="root".
 */

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// Рендеринг приложения в StrictMode для выявления потенциальных проблем
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
