export interface ProfessionInfo {
  id: number
  name: string
  description: string
  icon: string
  gradient: string
  technologies: string[]
}

export const professionData: Record<number, ProfessionInfo> = {
  1: {
    id: 1,
    name: 'Frontend',
    description: 'Разработка пользовательских интерфейсов',
    icon: '🎨',
    gradient: 'from-pink-500 to-rose-500',
    technologies: ['React', 'Vue', 'Angular', 'TypeScript']
  },
  2: {
    id: 2,
    name: 'Backend',
    description: 'Серверная логика и базы данных',
    icon: '⚙️',
    gradient: 'from-blue-500 to-cyan-500',
    technologies: ['Python', 'Java', 'Go', 'Node.js']
  },
  3: {
    id: 3,
    name: 'Fullstack',
    description: 'Универсальный разработчик',
    icon: '🚀',
    gradient: 'from-purple-500 to-indigo-500',
    technologies: ['React', 'Node.js', 'Python', 'SQL']
  },
  4: {
    id: 4,
    name: 'DevOps',
    description: 'Инфраструктура и автоматизация',
    icon: '☁️',
    gradient: 'from-orange-500 to-amber-500',
    technologies: ['Docker', 'Kubernetes', 'AWS', 'CI/CD']
  }
}

export const getProfessionIcon = (id: number): string => {
  return professionData[id]?.icon || '📁'
}

export const getProfessionGradient = (id: number): string => {
  return professionData[id]?.gradient || 'from-gray-500 to-gray-600'
}
