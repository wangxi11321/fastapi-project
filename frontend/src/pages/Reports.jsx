import { useState, useEffect } from 'react'
import { Plus, Calendar, FileText, Download, RefreshCw } from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import { reportApi } from '../services/api'

function Reports() {
  const [reports, setReports] = useState([])
  const [dailySummary, setDailySummary] = useState('')
  const [weeklySummary, setWeeklySummary] = useState('')
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [formData, setFormData] = useState({
    employee_id: '',
    employee_name: '',
    date: new Date().toISOString().split('T')[0],
    content: '',
    summary: '',
    tasks_done: '',
    tasks_tomorrow: '',
    issues: '',
  })

  useEffect(() => {
    fetchReports()
    fetchDailySummary()
    fetchWeeklySummary()
  }, [])

  const fetchReports = async () => {
    try {
      const res = await reportApi.getAll()
      setReports(res.data)
    } catch (error) {
      console.error('Failed to fetch reports:', error)
    }
  }

  const fetchDailySummary = async () => {
    try {
      const today = new Date().toISOString().split('T')[0]
      const res = await reportApi.getDailySummary(today)
      setDailySummary(res.data.summary)
    } catch (error) {
      console.error('Failed to fetch daily summary:', error)
    }
  }

  const fetchWeeklySummary = async () => {
    try {
      const today = new Date()
      const startDate = new Date(today.setDate(today.getDate() - today.getDay())).toISOString().split('T')[0]
      const endDate = new Date(today.setDate(today.getDate() + 6)).toISOString().split('T')[0]
      const res = await reportApi.getWeeklySummary(startDate, endDate)
      setWeeklySummary(res.data.summary)
    } catch (error) {
      console.error('Failed to fetch weekly summary:', error)
    }
  }

  const handleCreate = async () => {
    try {
      await reportApi.create(formData)
      fetchReports()
      setIsCreateModalOpen(false)
      setFormData({
        employee_id: '',
        employee_name: '',
        date: new Date().toISOString().split('T')[0],
        content: '',
        summary: '',
        tasks_done: '',
        tasks_tomorrow: '',
        issues: '',
      })
    } catch (error) {
      console.error('Failed to create report:', error)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">日报管理</h1>
          <p className="text-gray-500 mt-1">查看和管理员工日报</p>
        </div>
        <Button onClick={() => setIsCreateModalOpen(true)}>
          <Plus className="w-5 h-5" />
          新建日报
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="今日日报汇总" actions={
          <Button variant="secondary" size="sm" onClick={fetchDailySummary}>
            <RefreshCw className="w-4 h-4" />
            刷新
          </Button>
        }>
          <pre className="whitespace-pre-wrap text-sm text-gray-600 bg-gray-50 p-4 rounded-lg max-h-48 overflow-y-auto">
            {dailySummary}
          </pre>
        </Card>

        <Card title="本周周报汇总">
          <pre className="whitespace-pre-wrap text-sm text-gray-600 bg-gray-50 p-4 rounded-lg max-h-48 overflow-y-auto">
            {weeklySummary}
          </pre>
        </Card>
      </div>

      <Card title="日报列表">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">员工</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">日期</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">工作总结</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">今日完成</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">明日计划</th>
              </tr>
            </thead>
            <tbody>
              {reports.length > 0 ? (
                reports.map((report) => (
                  <tr key={report.id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="py-3 px-4 text-sm text-gray-900">{report.employee_name}</td>
                    <td className="py-3 px-4 text-sm text-gray-600">
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-gray-400" />
                        {new Date(report.date).toLocaleDateString('zh-CN')}
                      </div>
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-600 max-w-xs truncate">{report.summary || '-'}</td>
                    <td className="py-3 px-4 text-sm text-gray-600 max-w-xs truncate">{report.tasks_done || '-'}</td>
                    <td className="py-3 px-4 text-sm text-gray-600 max-w-xs truncate">{report.tasks_tomorrow || '-'}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="py-8 text-center text-gray-500">暂无日报数据</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>

      {isCreateModalOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">新建日报</h3>
              <button onClick={() => setIsCreateModalOpen(false)} className="text-gray-400 hover:text-gray-600">
                ✕
              </button>
            </div>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">员工ID *</label>
                  <input
                    type="number"
                    value={formData.employee_id}
                    onChange={(e) => setFormData({...formData, employee_id: parseInt(e.target.value) || ''})}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">员工姓名 *</label>
                  <input
                    type="text"
                    value={formData.employee_name}
                    onChange={(e) => setFormData({...formData, employee_name: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">日期</label>
                  <input
                    type="date"
                    value={formData.date}
                    onChange={(e) => setFormData({...formData, date: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">日报内容 *</label>
                  <textarea
                    value={formData.content}
                    onChange={(e) => setFormData({...formData, content: e.target.value})}
                    rows={4}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                    required
                  />
                </div>
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">工作总结</label>
                  <textarea
                    value={formData.summary}
                    onChange={(e) => setFormData({...formData, summary: e.target.value})}
                    rows={2}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                    placeholder="今日工作小结"
                  />
                </div>
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">今日完成</label>
                  <textarea
                    value={formData.tasks_done}
                    onChange={(e) => setFormData({...formData, tasks_done: e.target.value})}
                    rows={2}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                    placeholder="今日完成的工作"
                  />
                </div>
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">明日计划</label>
                  <textarea
                    value={formData.tasks_tomorrow}
                    onChange={(e) => setFormData({...formData, tasks_tomorrow: e.target.value})}
                    rows={2}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                    placeholder="明日工作计划"
                  />
                </div>
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">问题与建议</label>
                  <textarea
                    value={formData.issues}
                    onChange={(e) => setFormData({...formData, issues: e.target.value})}
                    rows={2}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                    placeholder="工作中遇到的问题或建议"
                  />
                </div>
              </div>
              <div className="flex justify-end gap-3 mt-6">
                <Button variant="secondary" onClick={() => setIsCreateModalOpen(false)}>取消</Button>
                <Button onClick={handleCreate}>提交日报</Button>
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  )
}

export default Reports