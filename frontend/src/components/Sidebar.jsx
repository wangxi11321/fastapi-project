import { 
  LayoutDashboard, 
  Users, 
  Scale, 
  FileText, 
  CalendarDays, 
  MessageSquare, 
  Calendar,
  ChevronLeft,
  ChevronRight,
  Brain
} from 'lucide-react'
import { NavLink } from 'react-router-dom'

const menuItems = [
  { path: '/', icon: LayoutDashboard, label: '仪表盘' },
  { path: '/customers', icon: Users, label: '意向客户' },
  { path: '/judge', icon: Brain, label: '客户研判' },
  { path: '/reports', icon: FileText, label: '日报管理' },
  { path: '/leaves', icon: CalendarDays, label: '请假申请' },
  { path: '/feedback', icon: MessageSquare, label: '售后反馈' },
  { path: '/activities', icon: Calendar, label: '活动管理' },
]

function Sidebar({ collapsed }) {
  return (
    <aside className={`${collapsed ? 'w-16' : 'w-64'} bg-sidebar-bg text-white flex flex-col fixed h-full z-10`}>
      <div className={`p-4 border-b border-gray-700 flex items-center ${collapsed ? 'justify-center' : 'gap-3'}`}>
        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
          <Scale className="w-6 h-6 text-white" />
        </div>
        {!collapsed && (
          <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-blue-300 bg-clip-text text-transparent">
            AI智能助手
          </span>
        )}
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={`nav-item flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${collapsed ? 'justify-center px-2' : ''}
                ${({ isActive }) => isActive 
                  ? 'bg-sidebar-active text-blue-400' 
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                }`}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              {!collapsed && <span className="nav-text text-sm font-medium">{item.label}</span>}
            </NavLink>
          )
        })}
      </nav>

      <div className={`p-4 border-t border-gray-700 ${collapsed ? 'flex justify-center' : ''}`}>
        <button
          onClick={() => window.location.reload()}
          className={`flex items-center gap-3 px-4 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-all ${collapsed ? 'px-2 justify-center' : ''}`}
        >
          {collapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
          {!collapsed && <span className="text-sm">收起菜单</span>}
        </button>
      </div>
    </aside>
  )
}

export default Sidebar