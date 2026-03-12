/**
 * API клиент для взаимодействия с backend.
 * Использует Axios для HTTP запросов с автоматической обработкой JWT токенов.
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from '../stores/authStore'

const API_BASE = '/api'

// Создание экземпляра axios с базовой конфигурацией
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Флаг для предотвращения множественных запросов на refresh
let isRefreshing = false
// Очередь запросов, ожидающих refresh токена
let failedQueue: Array<{
  resolve: (value: unknown) => void
  reject: (reason?: unknown) => void
}> = []

/**
 * Обработка очереди запросов после refresh токена.
 * @param error - Ошибка (если была) или null
 * @param token - Новый токен (если успешен) или null
 */
const processQueue = (error: Error | null, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

/**
 * Interceptor для добавления JWT токена в заголовок Authorization.
 * Выполняется перед каждым запросом.
 */
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

/**
 * Interceptor для обработки ответов API.
 * Автоматически refresh'ит токен при получении 401 ошибки.
 */
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean
    }

    // Если ошибка 401 и запрос еще не был повторен
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Если уже идет refresh, добавляем запрос в очередь
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return api(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      const refreshToken = useAuthStore.getState().refreshToken

      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE}/auth/refresh`, {
            refresh_token: refreshToken,
          })

          const { access_token, refresh_token: newRefreshToken } = response.data

          // Обновляем токены в store
          useAuthStore.getState().login(access_token, newRefreshToken, useAuthStore.getState().user!)

          // Обрабатываем очередь запросов
          processQueue(null, access_token)

          // Повторяем оригинальный запрос
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return api(originalRequest)
        } catch (refreshError) {
          // Если refresh не удался, logout
          processQueue(refreshError as Error, null)
          useAuthStore.getState().logout()
          window.location.href = '/login'
          return Promise.reject(refreshError)
        } finally {
          isRefreshing = false
        }
      } else {
        // Нет refresh токена - logout
        useAuthStore.getState().logout()
        window.location.href = '/login'
        return Promise.reject(error)
      }
    }

    return Promise.reject(error)
  }
)

/**
 * API методы для аутентификации.
 */
export const authApi = {
  /** Войти пользователя */
  login: async (email: string, password: string) => {
    const params = new URLSearchParams()
    params.append('username', email)
    params.append('password', password)
    const response = await api.post('/auth/login', params.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    return response.data
  },
  /** Зарегистрировать нового пользователя */
  register: async (email: string, password: string) => {
    const response = await api.post('/auth/register', { email, password })
    return response.data
  },
  /** Получить данные текущего пользователя */
  getCurrentUser: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },
  /** Обновить данные текущего пользователя */
  updateCurrentUser: async (data: { password?: string; is_admin?: boolean }) => {
    const response = await api.put('/auth/me', data)
    return response.data
  },
  /** Обновить токены */
  refreshTokens: async (refreshToken: string) => {
    const response = await api.post('/auth/refresh', { refresh_token: refreshToken })
    return response.data
  },
}

/**
 * API методы для работы с профессиями.
 */
export const professionsApi = {
  /** Получить все профессии */
  getAll: async () => {
    const response = await api.get('/professions/')
    return response.data
  },
  /** Получить профессию по ID */
  getById: async (id: number) => {
    const response = await api.get(`/professions/${id}`)
    return response.data
  },
}

/**
 * API методы для работы с вопросами.
 */
export const questionsApi = {
  /** Получить все вопросы или по профессии */
  getAll: async (professionId?: number) => {
    const params = professionId ? { profession_id: professionId } : {}
    const response = await api.get('/questions/', { params })
    return response.data
  },
  /** Получить вопрос по ID */
  getById: async (id: number) => {
    const response = await api.get(`/questions/${id}`)
    return response.data
  },
  /** Создать новый вопрос */
  create: async (data: {
    text: string
    question_type: 'mcq' | 'ordering'
    profession_id: number
    difficulty: 'easy' | 'medium' | 'hard'
    options: string[]
    correct_option: number | null
    correct_order?: number[]
  }) => {
    const response = await api.post('/questions/', data)
    return response.data
  },
  /** Обновить вопрос */
  update: async (id: number, data: {
    text?: string
    question_type?: 'mcq' | 'ordering'
    profession_id?: number
    difficulty?: 'easy' | 'medium' | 'hard'
    options?: string[]
    correct_option?: number | null
    correct_order?: number[]
  }) => {
    const response = await api.put(`/questions/${id}`, data)
    return response.data
  },
  /** Удалить вопрос */
  delete: async (id: number) => {
    const response = await api.delete(`/questions/${id}`)
    return response.data
  },
  /** Дублировать вопрос */
  duplicate: async (id: number) => {
    const response = await api.post(`/questions/${id}/duplicate`)
    return response.data
  },
  /** Получить шаблоны вопросов */
  getTemplates: async () => {
    const response = await api.get('/questions/templates')
    return response.data
  },
  /** Экспорт вопросов в JSON */
  exportJSON: async (professionId?: number) => {
    const params = professionId ? { profession_id: professionId } : {}
    const response = await api.get('/questions/export/json', { params })
    return response.data
  },
  /** Экспорт вопросов в CSV */
  exportCSV: async (professionId?: number) => {
    const params = professionId ? { profession_id: professionId } : {}
    const response = await api.get('/questions/export/csv', { params, responseType: 'text' })
    return response.data
  },
  /** Импорт вопросов из JSON */
  importJSON: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/questions/import/json', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },
  /** Импорт вопросов из CSV */
  importCSV: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/questions/import/csv', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },
  /** Массовое обновление вопросов */
  bulkUpdate: async (questionIds: number[], updates: { profession_id?: number; difficulty?: string }) => {
    const response = await api.post('/questions/bulk-update', { question_ids: questionIds, ...updates })
    return response.data
  },
  /** Отправить ответ на вопрос */
  submitAnswer: async (questionId: number, selectedOption: number) => {
    const response = await api.post(`/questions/${questionId}/answers`, {
      selected_option: selectedOption,
    })
    return response.data
  },
}

/**
 * API методы для работы с сессиями.
 */
export const sessionsApi = {
  /** Создать новую сессию */
  create: async (professionId: number, difficulty: string = 'junior') => {
    const response = await api.post('/sessions/', { profession_id: professionId, difficulty })
    return response.data
  },
  /** Получить сессию по ID */
  getById: async (id: number) => {
    const response = await api.get(`/sessions/${id}`)
    return response.data
  },
  /** Получить все сессии с фильтрами */
  getAll: async (filters?: {
    status?: string
    profession_id?: number
    user_id?: number
    date_from?: string
    date_to?: string
  }) => {
    const params = new URLSearchParams()
    if (filters?.status) params.append('status', filters.status)
    if (filters?.profession_id) params.append('profession_id', filters.profession_id.toString())
    if (filters?.user_id) params.append('user_id', filters.user_id.toString())
    if (filters?.date_from) params.append('date_from', filters.date_from)
    if (filters?.date_to) params.append('date_to', filters.date_to)
    const response = await api.get(`/sessions/?${params.toString()}`)
    return response.data
  },
  /** Получить статистику по сессиям */
  getStats: async () => {
    const response = await api.get('/sessions/stats')
    return response.data
  },
  /** Завершить сессию */
  complete: async (id: number, score: number) => {
    const response = await api.post(`/sessions/${id}/complete`, { score })
    return response.data
  },
  /** Удалить сессию */
  delete: async (id: number) => {
    const response = await api.delete(`/sessions/${id}`)
    return response.data
  },
}

/**
 * API методы для работы с прогрессом пользователя.
 */
export const progressApi = {
  /** Получить прогресс текущего пользователя */
  getMyProgress: async () => {
    const response = await api.get('/progress/me')
    return response.data
  },
  /** Добавить XP за сессию */
  addXp: async (xp_amount: number, correct_answers: number, total_questions: number) => {
    const response = await api.post('/progress/add-xp', { xp_amount, correct_answers, total_questions })
    return response.data
  },
  /** Получить все достижения */
  getAllAchievements: async () => {
    const response = await api.get('/progress/achievements')
    return response.data
  },
}
