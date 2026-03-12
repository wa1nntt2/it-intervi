import React from 'react'

interface SidebarProps {
  children: React.ReactNode
}

export function Sidebar({ children }: SidebarProps) {
  return (
    <aside className="w-64 bg-white shadow-lg min-h-screen">
      <div className="p-4">{children}</div>
    </aside>
  )
}
