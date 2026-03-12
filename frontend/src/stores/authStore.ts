/**
 * Zustand store для управления аутентификацией.
 * Хранит JWT токены, данные пользователя и методы входа/выхода.
 * Использует persist middleware для сохранения состояния в localStorage.
 */

import { create } from 'zustand'
import { persist } from 'zustand/middleware'

/** Данные пользователя */
interface User {
  id: number
  email: string
  is_admin?: boolean  // Флаг администратора
}

/** Состояние store аутентификации */
interface AuthState {
  token: string | null  // JWT access токен
  refreshToken: string | null  // JWT refresh токен
  user: User | null  // Данные текущего пользователя
  isAuthenticated: boolean  // Флаг аутентификации
  login: (token: string, refreshToken: string, user: User) => void  // Вход
  logout: () => void  // Выход
  updateUser: (user: Partial<User>) => void  // Обновление данных пользователя
}

/**
 * Создание store с persist middleware.
 * Данные сохраняются в localStorage под ключом 'auth-storage'.
 */
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,
      
      /**
       * Вход пользователя.
       * @param token - Access токен
       * @param refreshToken - Refresh токен
       * @param user - Данные пользователя
       */
      login: (token, refreshToken, user) =>
        set({ token, refreshToken, user, isAuthenticated: true }),
      
      /**
       * Выход пользователя.
       * Очищает все данные аутентификации.
       */
      logout: () =>
        set({ token: null, refreshToken: null, user: null, isAuthenticated: false }),
      
      /**
       * Обновление данных пользователя.
       * @param userData - Новые данные пользователя
       */
      updateUser: (userData) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...userData } : null
        })),
    }),
    {
      name: 'auth-storage',  // Ключ для localStorage
    }
  )
)
