import { useState, useEffect } from 'react'
import { Plus, Calendar, CheckCircle, XCircle, Clock } from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import { leaveApi } from '../services/api'

function LeaveApplications() {
  const [applications, setApplications] = useState([])
  const [filterStatus, setFilterStatus] = useState('all')
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [isApproveModalOpen, setIsApproveModalOpen] = useState(false)
  const [selectedApplication, setSelectedApplication] = useState(null)
  const [formData, setFormData] = useState({
    student_id: '',
    student_name: '',
    leave_type: '事假',
    start_date: '',
    end_date: '',
    reason: '',
  })
  const [approveComment, setApproveComment] = useState('')

  useEffect(() => {
    fetchApplications()
  }, [filterStatus])

  const fetchApplications = async () => {
    try {
      if (filterStatus === 'all') {
        const res = await leaveApi.getAll()
        setApplications(res.data)
      } else {
        const res = await leaveApi.getByStatus(filterStatus)
        setApplications(res.data)
      }
    } catch (error) {
      console.error('Failed to fetch applications:', error)
    }
  }

  const handleCreate = async () => {
    try {
      await leaveApi.create(formData)
      fetchApplications()
      setIsCreateModalOpen(false)
      setFormData({
        student_id: '',
        student_name: '',
        leave_type: '事假',
        start_date: '',
        end_date: '',
        reason: '',
      })
    } catch (error) {
      console.error('Failed to create application:', error)
    }
  }

  const handleApprove = async (status) => {
    try {
      await leaveApi.update(selectedApplication.id, {
        status: status,
        approver_id: 1,
        approver_name: '管理员',
        approve_comment: approveComment,
      })
      fetchApplications()
      setIsApproveModalOpen(false)
      setSelectedApplication(null)
      setApproveComment('')
    } catch (error) {
      console.error('Failed to approve:', error)
    }
  }

  const statusConfig = {
    pending: { label: '待审批', color: 'bg-yellow-100 text-yellow-700', icon: Clock },
    approved: { label: '已批准', color: 'bg-green-100 text-green-700', icon: CheckCircle },
    rejected: { label: '已拒绝', color: 'bg-red-100 text-red-700', icon: XCircle },
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">请假申请</h1>
          <p className="text-gray-500 mt-1">管理学生请假申请</p>
        </div>
        <Button onClick={() => setIsCreateModalOpen(true)}>
          <Plus className="w-5 h-5" />
          提交申请
        </Button>
      </div>

      <Card>
        <div className="flex items-center gap-4 mb-6">
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          >
            <option value="all">全部状态</option>
            <option value="pending">待审批</option>
            <option value="approved">已批准</option>
            <option value="rejected">已拒绝</option>
          </select>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">学生姓名</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">请假类型</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">开始日期</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">结束日期</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">状态</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">操作</th>
              </tr>
            </thead>
            <tbody>
              {applications.length > 0 ? (
                applications.map((app) => {
                  const StatusIcon = statusConfig[app.status]?.icon || Clock
                  return (
                    <tr key={app.id} className="border-b border-gray-50 hover:bg-gray-50">
                      <td className="py-3 px-4 text-sm text-gray-900">{app.student_name}</td>
                      <td className="py-3 px-4 text-sm text-gray-600">{app.leave_type}</td>
                      <td className="py-3 px-4 text-sm text-gray-600">
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4 text-gray-400" />
                          {new Date(app.start_date).toLocaleDateString('zh-CN')}
                        </div>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600">{new Date(app.end_date).toLocaleDateString('zh-CN')}</td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${statusConfig[app.status]?.color}`}>
                          <StatusIcon className="w-3 h-3" />
                          {statusConfig[app.status]?.label}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        {app.status === 'pending' && (
                          <div className="flex items-center gap-2">
                            <button
                              onClick={() => { setSelectedApplication(app); setIsApproveModalOpen(true) }}
                              className="px-3 py-1 text-green-600 bg-green-50 rounded-lg text-sm hover:bg-green-100 transition-colors"
                            >
                              审批
                            </button>
                          </div>
                        )}
                        {app.status !== 'pending' && app.approve_comment && (
                          <span className="text-xs text-gray-500">已处理</span>
                        )}
                      </td>
                    </tr>
                  )
                })
              ) : (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-gray-500">暂无请假申请</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>

      {isCreateModalOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-md w-full">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">提交请假申请</h3>
              <button onClick={() => setIsCreateModalOpen(false)} className="text-gray-400 hover:text-gray-600">
                ✕
              </button>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">学生ID *</label>
                <input
                  type="number"
                  value={formData.student_id}
                  onChange={(e) => setFormData({...formData, student_id: parseInt(e.target.value) || ''})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">学生姓名 *</label>
                <input
                  type="text"
                  value={formData.student_name}
                  onChange={(e) => setFormData({...formData, student_name: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">请假类型</label>
                <select
                  value={formData.leave_type}
                  onChange={(e) => setFormData({...formData, leave_type: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="事假">事假</option>
                  <option value="病假">病假</option>
                  <option value="其他">其他</option>
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">开始日期 *</label>
                  <input
                    type="date"
                    value={formData.start_date}
                    onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">结束日期 *</label>
                  <input
                    type="date"
                    value={formData.end_date}
                    onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">请假原因</label>
                <textarea
                  value={formData.reason}
                  onChange={(e) => setFormData({...formData, reason: e.target.value})}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  placeholder="请说明请假原因"
                />
              </div>
              <div className="flex justify-end gap-3 mt-6">
                <Button variant="secondary" onClick={() => setIsCreateModalOpen(false)}>取消</Button>
                <Button onClick={handleCreate}>提交申请</Button>
              </div>
            </div>
          </Card>
        </div>
      )}

      {isApproveModalOpen && selectedApplication && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-md w-full">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">审批请假申请</h3>
              <button onClick={() => setIsApproveModalOpen(false)} className="text-gray-400 hover:text-gray-600">
                ✕
              </button>
            </div>
            <div className="space-y-4 mb-6">
              <div>
                <p className="text-sm text-gray-500">学生姓名</p>
                <p className="font-medium">{selectedApplication.student_name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">请假类型</p>
                <p className="font-medium">{selectedApplication.leave_type}</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">开始日期</p>
                  <p className="font-medium">{new Date(selectedApplication.start_date).toLocaleDateString('zh-CN')}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">结束日期</p>
                  <p className="font-medium">{new Date(selectedApplication.end_date).toLocaleDateString('zh-CN')}</p>
                </div>
              </div>
              {selectedApplication.reason && (
                <div>
                  <p className="text-sm text-gray-500">请假原因</p>
                  <p className="font-medium">{selectedApplication.reason}</p>
                </div>
              )}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">审批意见</label>
                <textarea
                  value={approveComment}
                  onChange={(e) => setApproveComment(e.target.value)}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  placeholder="请输入审批意见（可选）"
                />
              </div>
            </div>
            <div className="flex justify-end gap-3">
              <Button variant="secondary" onClick={() => setIsApproveModalOpen(false)}>取消</Button>
              <Button variant="danger" onClick={() => handleApprove('rejected')}>拒绝</Button>
              <Button onClick={() => handleApprove('approved')}>批准</Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  )
}

export default LeaveApplications