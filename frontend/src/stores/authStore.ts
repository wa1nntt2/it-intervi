/**
 * Zustand store для управления аутентификацией.
 *
 * SECURITY: Access токен хранится в sessionStorage (очищается при закрытии вкладки).
 * Refresh токен хранится в HttpOnly cookie на backend.
 * При перезагрузке страницы сессия восстанавливается из sessionStorage + refresh через cookie.
 */

import { create } from 'zustand'
import { authApi } from '../services/api'

/** Данные пользователя */
export interface User {
  id: number
  email: string
  is_admin?: boolean
}

/** Состояние store аутентификации */
interface AuthState {
  token: string | null
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  isRefreshing: boolean
  error: string | null
  login: (token: string, user: User) => void
  logout: () => Promise<void>
  updateUser: (user: Partial<User>) => void
  setAuthenticated: (isAuthenticated: boolean) => void
  initializeSession: () => Promise<void>
  clearError: () => void
}

// Ключи для sessionStorage
const TOKEN_KEY = 'auth_token'
const USER_KEY = 'auth_user'

/**
 * Восстановление данных из sessionStorage
 */
const restoreFromSession = (): { token: string | null, user: User | null } => {
  if (typeof window === 'undefined') return { token: null, user: null }
  
  try {
    const token = sessionStorage.getItem(TOKEN_KEY)
    const userStr = sessionStorage.getItem(USER_KEY)
    const user = userStr ? JSON.parse(userStr) : null
    
    return { token, user }
  } catch {
    return { token: null, user: null }
  }
}

/**
 * Сохранение данных в sessionStorage
 */
const saveToSession = (token: string | null, user: User | null) => {
  if (typeof window === 'undefined') return
  
  if (token) {
    sessionStorage.setItem(TOKEN_KEY, token)
  } else {
    sessionStorage.removeItem(TOKEN_KEY)
  }
  
  if (user) {
    sessionStorage.setItem(USER_KEY, JSON.stringify(user))
  } else {
    sessionStorage.removeItem(USER_KEY)
  }
}

/**
 * Очистка sessionStorage
 */
const clearSession = () => {
  if (typeof window === 'undefined') return
  sessionStorage.removeItem(TOKEN_KEY)
  sessionStorage.removeItem(USER_KEY)
}

// Восстанавливаем сессию при создании store
const { token: savedToken, user: savedUser } = restoreFromSession()

/**
 * Создание store с восстановлением сессии из sessionStorage.
 * Refresh токен хранится в HttpOnly cookie на backend.
 */
export const useAuthStore = create<AuthState>()((set, get) => ({
  token: savedToken,
  user: savedUser,
  isAuthenticated: !!savedToken && !!savedUser,
  isLoading: true,  // Начинаем с загрузки для проверки сессии
  isRefreshing: false,
  error: null,

  /**
   * Вход пользователя.
   */
  login: (token, user) => {
    saveToSession(token, user)
    set({ token, user, isAuthenticated: true, isLoading: false, error: null })
  },

  /**
   * Выход пользователя.
   * Вызывает API endpoint для очистки cookies.
   */
  logout: async () => {
    try {
      await authApi.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      clearSession()
      set({ token: null, user: null, isAuthenticated: false, isLoading: false, error: null })
    }
  },

  /**
   * Обновление данных пользователя.
   */
  updateUser: (userData) => {
    set((state) => {
      const newUser = state.user ? { ...state.user, ...userData } : null
      saveToSession(state.token, newUser)
      return { user: newUser }
    })
  },

  /**
   * Установка состояния аутентификации.
   */
  setAuthenticated: (isAuthenticated) =>
    set({ isAuthenticated, isLoading: false }),

  /**
   * Инициализация сессии при загрузке приложения.
   * Проверяет сохраненную сессию и при необходимости refresh'ит токен.
   */
  initializeSession: async () => {
    console.log('[authStore] initializeSession called')
    const { token: savedToken, user: savedUser } = restoreFromSession()
    console.log('[authStore] Restored from session:', { hasToken: !!savedToken, hasUser: !!savedUser })

    // Если нет сохраненных данных - просто завершаем инициализацию
    if (!savedToken || !savedUser) {
      console.log('[authStore] No saved session, setting isLoading=false')
      set({
        token: null,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null
      })
      return
    }

    // Если есть сохраненные данные, пробуем получить актуальные
    try {
      console.log('[authStore] Trying to get current user with saved token')
      const user = await authApi.getCurrentUser()
      console.log('[authStore] Got user:', user)
      set({
        token: savedToken,
        user,
        isAuthenticated: true,
        isLoading: false,
        error: null
      })
    } catch (error) {
      // Токен истек или ошибка сети - очищаем сессию
      console.log('[authStore] Failed to get user, clearing session:', error)
      clearSession()
      set({
        token: null,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null
      })
    }
  },

  /**
   * Очистка ошибки.
   */
  clearError: () => set({ error: null }),
}))
