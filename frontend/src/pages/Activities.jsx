import { useState, useEffect } from 'react'
import { Plus, Calendar, MapPin, Users, CalendarCheck, ExternalLink } from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import { activityApi } from '../services/api'

function Activities() {
  const [activities, setActivities] = useState([])
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [isRegisterModalOpen, setIsRegisterModalOpen] = useState(false)
  const [selectedActivity, setSelectedActivity] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    type: '讲座',
    description: '',
    location: '',
    start_date: '',
    end_date: '',
    capacity: '',
    is_active: true,
  })
  const [registerData, setRegisterData] = useState({
    student_id: '',
    student_name: '',
  })

  useEffect(() => {
    fetchActivities()
  }, [])

  const fetchActivities = async () => {
    try {
      const res = await activityApi.getAll()
      setActivities(res.data)
    } catch (error) {
      console.error('Failed to fetch activities:', error)
    }
  }

  const handleCreate = async () => {
    try {
      await activityApi.create(formData)
      fetchActivities()
      setIsCreateModalOpen(false)
      setFormData({
        name: '',
        type: '讲座',
        description: '',
        location: '',
        start_date: '',
        end_date: '',
        capacity: '',
        is_active: true,
      })
    } catch (error) {
      console.error('Failed to create activity:', error)
    }
  }

  const handleRegister = async () => {
    try {
      await activityApi.register({
        activity_id: selectedActivity.id,
        student_id: registerData.student_id,
        student_name: registerData.student_name,
      })
      fetchActivities()
      setIsRegisterModalOpen(false)
      setSelectedActivity(null)
      setRegisterData({ student_id: '', student_name: '' })
    } catch (error) {
      console.error('Failed to register:', error)
      alert('报名失败，活动已满或不存在')
    }
  }

  const isFull = (activity) => {
    return activity.capacity && activity.registered_count >= activity.capacity
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">活动管理</h1>
          <p className="text-gray-500 mt-1">管理和报名机构活动</p>
        </div>
        <Button onClick={() => setIsCreateModalOpen(true)}>
          <Plus className="w-5 h-5" />
          创建活动
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {activities.length > 0 ? (
          activities.map((activity) => (
            <Card key={activity.id} className="overflow-hidden">
              <div className="h-32 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center relative">
                <Calendar className="w-12 h-12 text-white/30" />
                <div className="absolute bottom-3 left-3 text-white">
                  <p className="text-2xl font-bold">{new Date(activity.start_date).getDate()}</p>
                  <p className="text-sm opacity-80">{new Date(activity.start_date).toLocaleDateString('zh-CN', { month: 'short' })}</p>
                </div>
                {!activity.is_active && (
                  <div className="absolute top-3 right-3 px-2 py-1 bg-black/30 rounded text-xs text-white">已结束</div>
                )}
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-gray-900 mb-2">{activity.name}</h3>
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">{activity.type}</span>
                </div>
                {activity.description && (
                  <p className="text-sm text-gray-600 mb-3 line-clamp-2">{activity.description}</p>
                )}
                <div className="space-y-2 text-sm">
                  {activity.location && (
                    <div className="flex items-center gap-2 text-gray-500">
                      <MapPin className="w-4 h-4" />
                      <span>{activity.location}</span>
                    </div>
                  )}
                  <div className="flex items-center gap-2 text-gray-500">
                    <Users className="w-4 h-4" />
                    <span>已报名 {activity.registered_count} / {activity.capacity || '不限'}</span>
                  </div>
                  {activity.end_date && activity.start_date !== activity.end_date && (
                    <div className="flex items-center gap-2 text-gray-500">
                      <Calendar className="w-4 h-4" />
                      <span>{new Date(activity.start_date).toLocaleDateString('zh-CN')} - {new Date(activity.end_date).toLocaleDateString('zh-CN')}</span>
                    </div>
                  )}
                </div>
                {activity.is_active && !isFull(activity) && (
                  <button
                    onClick={() => { setSelectedActivity(activity); setIsRegisterModalOpen(true) }}
                    className="mt-4 w-full flex items-center justify-center gap-2 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    <CalendarCheck className="w-4 h-4" />
                    立即报名
                  </button>
                )}
                {isFull(activity) && (
                  <div className="mt-4 w-full flex items-center justify-center gap-2 py-2 bg-gray-100 text-gray-500 rounded-lg">
                    <Users className="w-4 h-4" />
                    名额已满
                  </div>
                )}
              </div>
            </Card>
          ))
        ) : (
          <div className="col-span-3 py-12 text-center text-gray-500">
            <Calendar className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p>暂无活动</p>
          </div>
        )}
      </div>

      {isCreateModalOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-lg w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">创建活动</h3>
              <button onClick={() => setIsCreateModalOpen(false)} className="text-gray-400 hover:text-gray-600">
                ✕
              </button>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">活动名称 *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">活动类型</label>
                <select
                  value={formData.type}
                  onChange={(e) => setFormData({...formData, type: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="讲座">讲座</option>
                  <option value="活动">活动</option>
                  <option value="培训">培训</option>
                  <option value="其他">其他</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">活动描述</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  placeholder="请描述活动内容"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">活动地点</label>
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => setFormData({...formData, location: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="如：北京市朝阳区xxx大厦"
                />
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
                  <label className="block text-sm font-medium text-gray-700 mb-1">结束日期</label>
                  <input
                    type="date"
                    value={formData.end_date}
                    onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">活动容量</label>
                <input
                  type="number"
                  value={formData.capacity}
                  onChange={(e) => setFormData({...formData, capacity: parseInt(e.target.value) || ''})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="不填则不限人数"
                />
              </div>
              <div className="flex justify-end gap-3 mt-6">
                <Button variant="secondary" onClick={() => setIsCreateModalOpen(false)}>取消</Button>
                <Button onClick={handleCreate}>创建活动</Button>
              </div>
            </div>
          </Card>
        </div>
      )}

      {isRegisterModalOpen && selectedActivity && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-md w-full">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">报名活动</h3>
              <button onClick={() => setIsRegisterModalOpen(false)} className="text-gray-400 hover:text-gray-600">
                ✕
              </button>
            </div>
            <div className="space-y-4 mb-6">
              <div>
                <p className="text-sm text-gray-500">活动名称</p>
                <p className="font-medium">{selectedActivity.name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">活动时间</p>
                <p className="font-medium">{new Date(selectedActivity.start_date).toLocaleDateString('zh-CN')}</p>
              </div>
              {selectedActivity.location && (
                <div>
                  <p className="text-sm text-gray-500">活动地点</p>
                  <p className="font-medium">{selectedActivity.location}</p>
                </div>
              )}
              <div className="border-t pt-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">学生ID *</label>
                  <input
                    type="number"
                    value={registerData.student_id}
                    onChange={(e) => setRegisterData({...registerData, student_id: parseInt(e.target.value) || ''})}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div className="mt-3">
                  <label className="block text-sm font-medium text-gray-700 mb-1">学生姓名 *</label>
                  <input
                    type="text"
                    value={registerData.student_name}
                    onChange={(e) => setRegisterData({...registerData, student_name: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
              </div>
            </div>
            <div className="flex justify-end gap-3">
              <Button variant="secondary" onClick={() => setIsRegisterModalOpen(false)}>取消</Button>
              <Button onClick={handleRegister}>确认报名</Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  )
}

export default Activities