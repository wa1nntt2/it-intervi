/**
 * TypeScript типы и интерфейсы для приложения.
 * Определяют структуру данных для API ответов и состояния приложения.
 */

/** Пользователь системы */
export interface User {
  id: number
  email: string
  created_at: string
}

/** Профессия/направление в IT */
export interface Profession {
  id: number
  name: string
  description: string | null
}

/** Вопрос для тестирования */
export interface Question {
  id: number
  text: string
  question_type: 'mcq' | 'ordering'  // MCQ - выбор ответа, Ordering - упорядочивание
  profession_id: number
  difficulty: 'intern' | 'junior' | 'middle'  // Уровень сложности
  options: string[]  // Варианты ответов
  correct_option: number | null  // Индекс правильного ответа (для MCQ)
  correct_order?: number[] | null  // Правильный порядок (для Ordering)
  explanation?: string | null  // Пояснение к ответу
  category_ids?: number[]  // ID категорий вопроса
}

/** Ответ пользователя на вопрос */
export interface Answer {
  id: number
  question_id: number
  selected_option: number | null
  is_correct: boolean
}

/** Сессия тестирования */
export interface Session {
  id: number
  profession_id: number
  question_ids: number[]  // ID вопросов в сессии
  status: 'active' | 'completed' | 'failed'
  score: number  // Количество правильных ответов
  mode?: 'practice' | 'learning' | 'timed' | 'exam'  // Режим сессии
  time_limit?: number | null  // Лимит времени в секундах
  created_at: string
}

/** Ответ API с JWT токенами */
export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

/** Категория вопросов */
export interface Category {
  id: number
  name: string
  description: string | null
  profession_id: number
}

/** Конфигурация категории для собеседования */
export interface CategoryConfig {
  category_id: number
  question_count: number
}

/** Конфигурация собеседования */
export interface InterviewConfig {
  id: number
  name: string
  description: string | null
  profession_id: number
  profession_name: string
  user_id: number | null
  difficulty: 'intern' | 'junior' | 'middle'
  category_configs: CategoryConfig[]
  is_public: boolean
  is_default: boolean
}
