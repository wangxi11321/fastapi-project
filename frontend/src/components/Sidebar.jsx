import { 
  LayoutDashboard, 
  Users, 
  Brain, 
  FileText, 
  CalendarDays, 
  MessageSquare, 
  Calendar,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  Plus,
  AlertTriangle,
  BarChart3,
  GraduationCap,
  Settings,
  Shield,
  Activity,
  TrendingUp,
  Zap
} from 'lucide-react'
import { NavLink } from 'react-router-dom'

const menuGroups = [
  {
    title: 'MAIN',
    items: [
      { path: '/', icon: LayoutDashboard, label: '工作台' },
      { path: '/ai-assistant', icon: Sparkles, label: 'AI助手' },
      { path: '/analysis', icon: BarChart3, label: '智能分析' },
    ]
  },
  {
    title: 'CRM',
    items: [
      { path: '/customers', icon: Users, label: '客户管理' },
      { path: '/judge', icon: Brain, label: '客户研判' },
      { path: '/follow-up', icon: MessageSquare, label: '跟进记录' },
    ]
  },
  {
    title: 'STUDENT',
    items: [
      { path: '/students', icon: GraduationCap, label: '学生档案' },
      { path: '/leaves', icon: CalendarDays, label: '请假审批' },
      { path: '/activities', icon: Calendar, label: '活动报名' },
    ]
  },
  {
    title: 'AI ENGINE',
    items: [
      { path: '/risk', icon: AlertTriangle, label: '风险预警' },
      { path: '/emotion', icon: Activity, label: '情绪分析' },
      { path: '/reports', icon: TrendingUp, label: 'AI日报' },
    ]
  },
  {
    title: 'SYSTEM',
    items: [
      { path: '/permissions', icon: Shield, label: '权限管理' },
      { path: '/settings', icon: Settings, label: '系统设置' },
    ]
  }
]

function Sidebar({ collapsed, onToggle }) {
  return (
    <aside className={`${collapsed ? 'w-16' : 'w-64'} bg-[#0F172A] text-white flex flex-col fixed h-full z-10 transition-all duration-300 shadow-2xl`}>
      <div className={`p-4 border-b border-[#1E293B] flex flex-col ${collapsed ? 'items-center' : ''}`}>
        <div className={`flex items-center ${collapsed ? 'justify-center mb-2' : 'gap-3'}`}>
          <div className="w-10 h-10 bg-gradient-to-br from-violet-500 to-cyan-500 rounded-xl flex items-center justify-center shadow-lg shadow-violet-500/20">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          {!collapsed && (
            <div className="flex flex-col">
              <span className="text-lg font-bold bg-gradient-to-r from-violet-400 to-cyan-400 bg-clip-text text-transparent">
                AI Companion
              </span>
              <span className="text-xs text-gray-500">智能留学中台</span>
            </div>
          )}
        </div>
        
        {!collapsed && (
          <button className="mt-4 w-full flex items-center justify-center gap-2 px-3 py-2 bg-gradient-to-r from-violet-600 to-cyan-600 rounded-lg hover:from-violet-500 hover:to-cyan-500 transition-all duration-200 shadow-lg shadow-violet-500/20">
            <Plus className="w-4 h-4" />
            <span className="text-sm font-medium">新建会话</span>
          </button>
        )}
      </div>

      <nav className="flex-1 p-4 space-y-6 overflow-y-auto">
        {menuGroups.map((group) => (
          <div key={group.title} className="space-y-1">
            {!collapsed && (
              <span className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                {group.title}
              </span>
            )}
            {group.items.map((item) => {
              const Icon = item.icon
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={`nav-item flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${collapsed ? 'justify-center px-2' : ''}
                    ${({ isActive }) => isActive 
                      ? 'bg-gradient-to-r from-violet-600/30 to-cyan-600/30 text-violet-300 border-l-2 border-violet-500 shadow-lg shadow-violet-500/10' 
                      : 'text-gray-400 hover:bg-[#1E293B] hover:text-white'
                    }`}
                >
                  <Icon className={`w-5 h-5 flex-shrink-0 transition-all duration-200 ${({ isActive }) => isActive ? 'text-violet-400' : ''}`} />
                  {!collapsed && (
                    <span className={`nav-text text-sm font-medium transition-all duration-200 ${({ isActive }) => isActive ? 'font-semibold text-white' : ''}`}>
                      {item.label}
                    </span>
                  )}
                </NavLink>
              )
            })}
          </div>
        ))}
      </nav>

      <div className={`p-4 border-t border-[#1E293B] ${collapsed ? 'flex flex-col items-center gap-2' : ''}`}>
        {!collapsed && (
          <div className="flex items-center gap-2 mb-3">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-xs text-gray-400">GPT-4 在线</span>
          </div>
        )}
        {collapsed && <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>}
        
        <button
          onClick={onToggle}
          className={`flex items-center gap-3 px-4 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-[#1E293B] transition-all duration-200 ${collapsed ? 'px-2 justify-center' : ''}`}
        >
          {collapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
          {!collapsed && <span className="text-sm">收起菜单</span>}
        </button>
      </div>
    </aside>
  )
}

export default Sidebar
