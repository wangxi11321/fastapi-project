import { useState, useEffect } from 'react'
import { Plus, MessageSquare, Reply, CheckCircle, Clock } from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import { feedbackApi } from '../services/api'

function Feedback() {
  const [feedbacks, setFeedbacks] = useState([])
  const [filterStatus, setFilterStatus] = useState('all')
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [isReplyModalOpen, setIsReplyModalOpen] = useState(false)
  const [selectedFeedback, setSelectedFeedback] = useState(null)
  const [formData, setFormData] = useState({
    student_id: '',
    student_name: '',
    type: '建议',
    content: '',
  })
  const [replyContent, setReplyContent] = useState('')

  useEffect(() => {
    fetchFeedbacks()
  }, [filterStatus])

  const fetchFeedbacks = async () => {
    try {
      const res = await feedbackApi.getAll()
      let filtered = res.data
      if (filterStatus !== 'all') {
        filtered = res.data.filter(f => f.status === filterStatus)
      }
      setFeedbacks(filtered)
    } catch (error) {
      console.error('Failed to fetch feedbacks:', error)
    }
  }

  const handleCreate = async () => {
    try {
      await feedbackApi.create(formData)
      fetchFeedbacks()
      setIsCreateModalOpen(false)
      setFormData({
        student_id: '',
        student_name: '',
        type: '建议',
        content: '',
      })
    } catch (error) {
      console.error('Failed to create feedback:', error)
    }
  }

  const handleReply = async () => {
    try {
      await feedbackApi.update(selectedFeedback.id, {
        status: 'resolved',
        handler_id: 1,
        handler_name: '管理员',
        reply: replyContent,
      })
      fetchFeedbacks()
      setIsReplyModalOpen(false)
      setSelectedFeedback(null)
      setReplyContent('')
    } catch (error) {
      console.error('Failed to reply:', error)
    }
  }

  const statusConfig = {
    pending: { label: '待处理', color: 'bg-yellow-100 text-yellow-700', icon: Clock },
    resolved: { label: '已处理', color: 'bg-green-100 text-green-700', icon: CheckCircle },
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">售后反馈</h1>
          <p className="text-gray-500 mt-1">管理学生售后反馈</p>
        </div>
        <Button onClick={() => setIsCreateModalOpen(true)}>
          <Plus className="w-5 h-5" />
          提交反馈
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
            <option value="pending">待处理</option>
            <option value="resolved">已处理</option>
          </select>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {feedbacks.length > 0 ? (
            feedbacks.map((feedback) => {
              const StatusIcon = statusConfig[feedback.status]?.icon || Clock
              return (
                <div
                  key={feedback.id}
                  className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 transition-colors"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <MessageSquare className="w-5 h-5 text-blue-500" />
                      <span className="font-medium text-gray-900">{feedback.student_name}</span>
                    </div>
                    <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${statusConfig[feedback.status]?.color}`}>
                      <StatusIcon className="w-3 h-3" />
                      {statusConfig[feedback.status]?.label}
                    </span>
                  </div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">{feedback.type}</span>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">{feedback.content}</p>
                  {feedback.reply && (
                    <div className="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                      <p className="text-xs text-blue-500 mb-1">回复</p>
                      <p className="text-sm text-blue-700">{feedback.reply}</p>
                    </div>
                  )}
                  {feedback.status === 'pending' && (
                    <button
                      onClick={() => { setSelectedFeedback(feedback); setIsReplyModalOpen(true) }}
                      className="mt-3 flex items-center gap-2 text-blue-600 hover:text-blue-700 text-sm"
                    >
                      <Reply className="w-4 h-4" />
                      回复
                    </button>
                  )}
                </div>
              )
            })
          ) : (
            <div className="col-span-2 py-12 text-center text-gray-500">
              <MessageSquare className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>暂无反馈数据</p>
            </div>
          )}
        </div>
      </Card>

      {isCreateModalOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-md w-full">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">提交反馈</h3>
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
                <label className="block text-sm font-medium text-gray-700 mb-1">反馈类型</label>
                <select
                  value={formData.type}
                  onChange={(e) => setFormData({...formData, type: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="建议">建议</option>
                  <option value="投诉">投诉</option>
                  <option value="问题">问题</option>
                  <option value="其他">其他</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">反馈内容 *</label>
                <textarea
                  value={formData.content}
                  onChange={(e) => setFormData({...formData, content: e.target.value})}
                  rows={4}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  required
                  placeholder="请描述您的反馈内容"
                />
              </div>
              <div className="flex justify-end gap-3 mt-6">
                <Button variant="secondary" onClick={() => setIsCreateModalOpen(false)}>取消</Button>
                <Button onClick={handleCreate}>提交反馈</Button>
              </div>
            </div>
          </Card>
        </div>
      )}

      {isReplyModalOpen && selectedFeedback && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-md w-full">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">回复反馈</h3>
              <button onClick={() => setIsReplyModalOpen(false)} className="text-gray-400 hover:text-gray-600">
                ✕
              </button>
            </div>
            <div className="space-y-4 mb-6">
              <div>
                <p className="text-sm text-gray-500">学生姓名</p>
                <p className="font-medium">{selectedFeedback.student_name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">反馈类型</p>
                <span className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">{selectedFeedback.type}</span>
              </div>
              <div>
                <p className="text-sm text-gray-500">反馈内容</p>
                <p className="font-medium">{selectedFeedback.content}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">回复内容</label>
                <textarea
                  value={replyContent}
                  onChange={(e) => setReplyContent(e.target.value)}
                  rows={4}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  placeholder="请输入回复内容"
                  required
                />
              </div>
            </div>
            <div className="flex justify-end gap-3">
              <Button variant="secondary" onClick={() => setIsReplyModalOpen(false)}>取消</Button>
              <Button onClick={handleReply}>发送回复</Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  )
}

export default Feedback