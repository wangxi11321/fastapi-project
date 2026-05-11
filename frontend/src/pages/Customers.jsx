import { useState, useEffect } from 'react'
import { Plus, Search, Edit, Trash2, Eye, Filter } from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import { customerApi } from '../services/api'

function Customers() {
  const [customers, setCustomers] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [selectedCustomer, setSelectedCustomer] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    source: '',
    country: '',
    education: '',
    major: '',
    budget: '',
    target_school: '',
    target_major: '',
    english_level: '',
    tags: '',
    assignee: '',
    status: 'pending',
  })

  useEffect(() => {
    fetchCustomers()
  }, [])

  const fetchCustomers = async () => {
    try {
      const res = await customerApi.getAll()
      setCustomers(res.data)
    } catch (error) {
      console.error('Failed to fetch customers:', error)
    }
  }

  const handleCreate = async () => {
    try {
      await customerApi.create(formData)
      fetchCustomers()
      setIsCreateModalOpen(false)
      setFormData({
        name: '',
        phone: '',
        email: '',
        source: '',
        country: '',
        education: '',
        major: '',
        budget: '',
        target_school: '',
        target_major: '',
        english_level: '',
        tags: '',
        assignee: '',
        status: 'pending',
      })
    } catch (error) {
      console.error('Failed to create customer:', error)
    }
  }

  const handleDelete = async (id) => {
    if (confirm('确定要删除这个客户吗？')) {
      try {
        await customerApi.delete(id)
        fetchCustomers()
      } catch (error) {
        console.error('Failed to delete customer:', error)
      }
    }
  }

  const filteredCustomers = customers.filter(customer => {
    const matchesSearch = customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         customer.phone.includes(searchTerm)
    const matchesFilter = filterStatus === 'all' || 
                         (filterStatus === 'target' ? customer.is_target : !customer.is_target)
    return matchesSearch && matchesFilter
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">意向客户</h1>
          <p className="text-gray-500 mt-1">管理意向客户信息</p>
        </div>
        <Button onClick={() => setIsCreateModalOpen(true)}>
          <Plus className="w-5 h-5" />
          新建客户
        </Button>
      </div>

      <Card>
        <div className="flex items-center gap-4 mb-6">
          <div className="relative flex-1 max-w-md">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="搜索客户姓名或电话..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            />
          </div>
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-gray-500" />
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            >
              <option value="all">全部客户</option>
              <option value="target">目标客户</option>
              <option value="normal">普通客户</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">姓名</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">电话</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">国家</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">学历</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">预算</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">状态</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">操作</th>
              </tr>
            </thead>
            <tbody>
              {filteredCustomers.length > 0 ? (
                filteredCustomers.map((customer) => (
                  <tr key={customer.id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="py-3 px-4 text-sm text-gray-900">{customer.name}</td>
                    <td className="py-3 px-4 text-sm text-gray-600">{customer.phone}</td>
                    <td className="py-3 px-4 text-sm text-gray-600">{customer.country || '-'}</td>
                    <td className="py-3 px-4 text-sm text-gray-600">{customer.education || '-'}</td>
                    <td className="py-3 px-4 text-sm text-gray-600">
                      {customer.budget ? `${customer.budget}万` : '-'}
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        customer.is_target ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
                      }`}>
                        {customer.is_target ? '目标客户' : '普通客户'}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => { setSelectedCustomer(customer); setIsModalOpen(true) }}
                          className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button className="p-2 text-gray-500 hover:text-yellow-600 hover:bg-yellow-50 rounded-lg transition-colors">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(customer.id)}
                          className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-gray-500">暂无客户数据</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>

      {isModalOpen && selectedCustomer && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-2xl w-full max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">客户详情</h3>
              <button onClick={() => setIsModalOpen(false)} className="text-gray-400 hover:text-gray-600">
                ✕
              </button>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500">姓名</p>
                <p className="font-medium">{selectedCustomer.name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">电话</p>
                <p className="font-medium">{selectedCustomer.phone}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">邮箱</p>
                <p className="font-medium">{selectedCustomer.email || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">来源</p>
                <p className="font-medium">{selectedCustomer.source || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">目标国家</p>
                <p className="font-medium">{selectedCustomer.country || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">学历</p>
                <p className="font-medium">{selectedCustomer.education || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">专业</p>
                <p className="font-medium">{selectedCustomer.major || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">预算</p>
                <p className="font-medium">{selectedCustomer.budget ? `${selectedCustomer.budget}万` : '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">目标学校</p>
                <p className="font-medium">{selectedCustomer.target_school || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">目标专业</p>
                <p className="font-medium">{selectedCustomer.target_major || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">英语水平</p>
                <p className="font-medium">{selectedCustomer.english_level || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">标签</p>
                <p className="font-medium">{selectedCustomer.tags || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">状态</p>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  selectedCustomer.is_target ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
                }`}>
                  {selectedCustomer.is_target ? '目标客户' : '普通客户'}
                </span>
              </div>
              <div>
                <p className="text-sm text-gray-500">研判理由</p>
                <p className="font-medium text-sm">{selectedCustomer.judge_reason || '-'}</p>
              </div>
            </div>
          </Card>
        </div>
      )}

      {isCreateModalOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">新建客户</h3>
              <button onClick={() => setIsCreateModalOpen(false)} className="text-gray-400 hover:text-gray-600">
                ✕
              </button>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">姓名 *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">电话 *</label>
                <input
                  type="text"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">来源</label>
                <input
                  type="text"
                  value={formData.source}
                  onChange={(e) => setFormData({...formData, source: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">目标国家</label>
                <input
                  type="text"
                  value={formData.country}
                  onChange={(e) => setFormData({...formData, country: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">学历</label>
                <input
                  type="text"
                  value={formData.education}
                  onChange={(e) => setFormData({...formData, education: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">专业</label>
                <input
                  type="text"
                  value={formData.major}
                  onChange={(e) => setFormData({...formData, major: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">预算(万)</label>
                <input
                  type="number"
                  value={formData.budget}
                  onChange={(e) => setFormData({...formData, budget: parseFloat(e.target.value) || ''})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">目标学校</label>
                <input
                  type="text"
                  value={formData.target_school}
                  onChange={(e) => setFormData({...formData, target_school: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">目标专业</label>
                <input
                  type="text"
                  value={formData.target_major}
                  onChange={(e) => setFormData({...formData, target_major: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">英语水平</label>
                <input
                  type="text"
                  value={formData.english_level}
                  onChange={(e) => setFormData({...formData, english_level: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">负责人</label>
                <input
                  type="text"
                  value={formData.assignee}
                  onChange={(e) => setFormData({...formData, assignee: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
            <div className="flex justify-end gap-3 mt-6">
              <Button variant="secondary" onClick={() => setIsCreateModalOpen(false)}>取消</Button>
              <Button onClick={handleCreate}>创建</Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  )
}

export default Customers