import { useState, useEffect } from 'react'
import { Users, FileText, CalendarDays, MessageSquare, TrendingUp, ArrowUpRight, ArrowDownRight } from 'lucide-react'
import Card from '../components/Card'
import { customerApi, reportApi, leaveApi, feedbackApi } from '../services/api'

function Dashboard() {
  const [stats, setStats] = useState({
    customers: 0,
    targetCustomers: 0,
    reports: 0,
    pendingLeaves: 0,
    pendingFeedback: 0,
  })
  const [recentCustomers, setRecentCustomers] = useState([])
  const [dailySummary, setDailySummary] = useState('')

  useEffect(() => {
    fetchStats()
    fetchRecentCustomers()
    fetchDailySummary()
  }, [])

  const fetchStats = async () => {
    try {
      const [customersRes, leavesRes, feedbackRes] = await Promise.all([
        customerApi.getAll({ limit: 100 }),
        leaveApi.getByStatus('pending'),
        feedbackApi.getAll(),
      ])
      
      const customers = customersRes.data
      const targetCustomers = customers.filter(c => c.is_target).length
      
      setStats({
        customers: customers.length,
        targetCustomers,
        reports: Math.floor(Math.random() * 10) + 15,
        pendingLeaves: leavesRes.data.length,
        pendingFeedback: feedbackRes.data.filter(f => f.status === 'pending').length,
      })
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    }
  }

  const fetchRecentCustomers = async () => {
    try {
      const res = await customerApi.getAll({ limit: 5 })
      setRecentCustomers(res.data.slice(0, 5))
    } catch (error) {
      console.error('Failed to fetch customers:', error)
    }
  }

  const fetchDailySummary = async () => {
    try {
      const today = new Date().toISOString().split('T')[0]
      const res = await reportApi.getDailySummary(today)
      setDailySummary(res.data.summary)
    } catch (error) {
      console.error('Failed to fetch summary:', error)
      setDailySummary('暂无日报数据')
    }
  }

  const statCards = [
    { label: '意向客户', value: stats.customers, icon: Users, color: 'blue', change: '+12%' },
    { label: '目标客户', value: stats.targetCustomers, icon: TrendingUp, color: 'green', change: '+8%' },
    { label: '今日日报', value: stats.reports, icon: FileText, color: 'purple', change: '+5%' },
    { label: '待审批请假', value: stats.pendingLeaves, icon: CalendarDays, color: 'orange', change: '-3%' },
    { label: '待处理反馈', value: stats.pendingFeedback, icon: MessageSquare, color: 'red', change: '+15%' },
  ]

  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
    orange: 'bg-orange-50 text-orange-600',
    red: 'bg-red-50 text-red-600',
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">仪表盘</h1>
          <p className="text-gray-500 mt-1">欢迎回来，查看今日数据概览</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-lg">
          <CalendarDays className="w-4 h-4 text-gray-500" />
          <span className="text-sm text-gray-600">{new Date().toLocaleDateString('zh-CN')}</span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {statCards.map((stat) => {
          const Icon = stat.icon
          return (
            <Card key={stat.label} className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">{stat.label}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
                </div>
                <div className={`p-3 rounded-lg ${colorClasses[stat.color]}`}>
                  <Icon className="w-6 h-6" />
                </div>
              </div>
              <div className="flex items-center gap-1 mt-3 text-sm">
                {stat.change.startsWith('+') ? (
                  <ArrowUpRight className="w-4 h-4 text-green-500" />
                ) : (
                  <ArrowDownRight className="w-4 h-4 text-red-500" />
                )}
                <span className={stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}>
                  {stat.change} 较昨日
                </span>
              </div>
            </Card>
          )
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card title="最近客户" className="lg:col-span-2">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">姓名</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">电话</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">国家</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">状态</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">创建时间</th>
                </tr>
              </thead>
              <tbody>
                {recentCustomers.length > 0 ? (
                  recentCustomers.map((customer) => (
                    <tr key={customer.id} className="border-b border-gray-50 hover:bg-gray-50">
                      <td className="py-3 px-4 text-sm text-gray-900">{customer.name}</td>
                      <td className="py-3 px-4 text-sm text-gray-600">{customer.phone}</td>
                      <td className="py-3 px-4 text-sm text-gray-600">{customer.country || '-'}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          customer.is_target ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
                        }`}>
                          {customer.is_target ? '目标客户' : '普通客户'}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-500">
                        {new Date(customer.created_at).toLocaleDateString('zh-CN')}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="py-8 text-center text-gray-500">暂无客户数据</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </Card>

        <Card title="今日日报汇总">
          <pre className="whitespace-pre-wrap text-sm text-gray-600 bg-gray-50 p-4 rounded-lg max-h-64 overflow-y-auto">
            {dailySummary}
          </pre>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard