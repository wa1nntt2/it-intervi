/**
 * Zustand store для управления аутентификацией.
 * Хранит JWT токены, данные пользователя и методы входа/выхода.
 *
 * SECURITY UPDATE: Refresh токен теперь хранится в HttpOnly cookie на backend.
 * Access токен хранится в localStorage для сохранения сессии после перезагрузки.
 */

import { create } from 'zustand'
import { persist } from 'zustand/middleware'

/** Данные пользователя */
export interface User {
  id: number
  email: string
  is_admin?: boolean  // Флаг администратора
}

/** Состояние store аутентификации */
interface AuthState {
  token: string | null  // JWT access токен (сохраняется в localStorage)
  user: User | null  // Данные текущего пользователя
  isAuthenticated: boolean  // Флаг аутентификации
  isLoading: boolean  // Флаг загрузки состояния
  login: (token: string, user: User) => void  // Вход
  logout: () => Promise<void>  // Выход (с вызовом API)
  updateUser: (user: Partial<User>) => void  // Обновление данных пользователя
  setAuthenticated: (isAuthenticated: boolean) => void  // Установка состояния
}

/**
 * Создание store с persist middleware.
 * ACCESS токен и user сохраняются в localStorage для сохранения сессии.
 * REFRESH токен хранится в HttpOnly cookie на backend.
 */
export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,  // Не загружаемся, так как данные из localStorage

      /**
       * Вход пользователя.
       * @param token - Access токен
       * @param user - Данные пользователя
       */
      login: (token, user) =>
        set({ token, user, isAuthenticated: true, isLoading: false }),

      /**
       * Выход пользователя.
       * Вызывает API endpoint для очистки cookies и очищает состояние.
       */
      logout: async () => {
        try {
          // Импортируем api для вызова logout endpoint
          const { authApi } = await import('../services/api')
          await authApi.logout()
        } catch (error) {
          console.error('Logout error:', error)
        } finally {
          // Всегда очищаем состояние независимо от результата
          set({ token: null, user: null, isAuthenticated: false, isLoading: false })
        }
      },

      /**
       * Обновление данных пользователя.
       * @param userData - Новые данные пользователя
       */
      updateUser: (userData) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...userData } : null
        })),

      /**
       * Установка состояния аутентификации.
       * Используется при инициализации приложения.
       */
      setAuthenticated: (isAuthenticated) =>
        set({ isAuthenticated, isLoading: false }),
    }),
    {
      name: 'auth-storage',  // Ключ для localStorage
      partialize: (state) => ({
        // Сохраняем только token и user (не сохраняем isLoading)
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
