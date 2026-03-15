/**
 * Схемы валидации Zod для форм приложения.
 * Используются для валидации данных на frontend перед отправкой на сервер.
 */

import { z } from 'zod'

/**
 * Схема валидации пароля:
 * - Минимум 8 символов
 * - Хотя бы одна заглавная буква
 * - Хотя бы одна строчная буква
 * - Хотя бы одна цифра
 */
const passwordSchema = z
  .string()
  .min(8, 'Пароль должен содержать минимум 8 символов')
  .regex(/[A-Z]/, 'Пароль должен содержать хотя бы одну заглавную букву')
  .regex(/[a-z]/, 'Пароль должен содержать хотя бы одну строчную букву')
  .regex(/\d/, 'Пароль должен содержать хотя бы одну цифру')

/**
 * Схема для формы входа.
 */
export const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'Email обязателен')
    .email('Некорректный формат email'),
  password: z.string().min(1, 'Пароль обязателен'),
})

/**
 * Схема для формы регистрации.
 */
export const registerSchema = z.object({
  email: z
    .string()
    .min(1, 'Email обязателен')
    .email('Некорректный формат email'),
  password: passwordSchema,
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Пароли не совпадают',
  path: ['confirmPassword'],
})

/**
 * Схема для формы вопроса (MCQ).
 */
export const questionMcqSchema = z.object({
  text: z.string().min(10, 'Вопрос должен содержать минимум 10 символов'),
  question_type: z.literal('mcq'),
  profession_id: z.number().int().positive('Выберите профессию'),
  difficulty: z.enum(['intern', 'junior', 'middle']),
  options: z
    .array(z.string().min(1, 'Вариант не может быть пустым'))
    .min(2, 'Минимум 2 варианта ответа')
    .max(10, 'Максимум 10 вариантов ответа'),
  correct_option: z.number().int().min(0, 'Выберите правильный ответ'),
  explanation: z.string().optional(),
  category_ids: z.array(z.number()).optional(),
})

/**
 * Схема для формы вопроса (Ordering).
 */
export const questionOrderingSchema = z.object({
  text: z.string().min(10, 'Вопрос должен содержать минимум 10 символов'),
  question_type: z.literal('ordering'),
  profession_id: z.number().int().positive('Выберите профессию'),
  difficulty: z.enum(['intern', 'junior', 'middle']),
  options: z
    .array(z.string().min(1, 'Вариант не может быть пустым'))
    .min(3, 'Минимум 3 варианта для упорядочивания')
    .max(10, 'Максимум 10 вариантов'),
  correct_order: z
    .array(z.number())
    .min(3, 'Минимум 3 элемента в правильном порядке'),
  explanation: z.string().optional(),
  category_ids: z.array(z.number()).optional(),
})

/**
 * Объединенная схема для вопроса (любой тип).
 */
export const questionSchema = z.union([
  questionMcqSchema,
  questionOrderingSchema,
])

/**
 * Схема для формы профиля.
 */
export const profileSchema = z.object({
  currentPassword: z.string().optional(),
  newPassword: passwordSchema.optional(),
  confirmPassword: z.string().optional(),
}).refine((data) => {
  // Если меняем пароль, проверяем совпадение
  if (data.newPassword || data.confirmPassword) {
    return data.newPassword === data.confirmPassword
  }
  return true
}, {
  message: 'Пароли не совпадают',
  path: ['confirmPassword'],
})

/**
 * Схема для формы категории.
 */
export const categorySchema = z.object({
  name: z.string().min(2, 'Название должно содержать минимум 2 символа').max(100),
  description: z.string().max(500, 'Описание не должно превышать 500 символов').optional(),
  profession_id: z.number().int().positive('Выберите профессию'),
})

/**
 * Схема для формы конфигурации собеседования.
 */
export const interviewConfigSchema = z.object({
  name: z.string().min(3, 'Название должно содержать минимум 3 символа').max(100),
  description: z.string().max(500).optional(),
  profession_id: z.number().int().positive('Выберите профессию'),
  difficulty: z.enum(['intern', 'junior', 'middle']),
  category_configs: z
    .array(z.object({
      category_id: z.number(),
      question_count: z.number().int().positive().max(50),
    }))
    .min(1, 'Добавьте хотя бы одну категорию'),
  is_public: z.boolean().optional(),
})

/**
 * Типы для форм, выведенные из схем.
 */
export type LoginFormData = z.infer<typeof loginSchema>
export type RegisterFormData = z.infer<typeof registerSchema>
export type QuestionMcqFormData = z.infer<typeof questionMcqSchema>
export type QuestionOrderingFormData = z.infer<typeof questionOrderingSchema>
export type QuestionFormData = z.infer<typeof questionSchema>
export type ProfileFormData = z.infer<typeof profileSchema>
export type CategoryFormData = z.infer<typeof categorySchema>
export type InterviewConfigFormData = z.infer<typeof interviewConfigSchema>
