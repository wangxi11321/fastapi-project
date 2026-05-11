import { useState } from 'react'
import { Brain, FileText, CheckCircle, XCircle, Tag } from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import { judgeApi, customerApi } from '../services/api'

function CustomerJudge() {
  const [customerInfo, setCustomerInfo] = useState('')
  const [judgeResult, setJudgeResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)

  const handleJudge = async () => {
    if (!customerInfo.trim()) {
      alert('请输入客户信息')
      return
    }
    
    setIsLoading(true)
    try {
      const res = await judgeApi.judge({ customer_info: customerInfo })
      setJudgeResult(res.data)
      setSaveSuccess(false)
    } catch (error) {
      console.error('Failed to judge customer:', error)
      alert('研判失败，请重试')
    } finally {
      setIsLoading(false)
    }
  }

  const handleJudgeAndSave = async () => {
    if (!customerInfo.trim()) {
      alert('请输入客户信息')
      return
    }
    
    setIsLoading(true)
    try {
      const res = await judgeApi.judgeAndSave({ customer_info: customerInfo })
      setJudgeResult(res.data.judge_result)
      setSaveSuccess(true)
      setTimeout(() => setSaveSuccess(false), 3000)
    } catch (error) {
      console.error('Failed to judge and save:', error)
      alert('保存失败，请重试')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">客户研判</h1>
          <p className="text-gray-500 mt-1">输入客户信息，系统自动判断是否符合目标客户画像</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="客户信息输入">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <FileText className="w-4 h-4 inline mr-2" />
                客户信息
              </label>
              <textarea
                value={customerInfo}
                onChange={(e) => setCustomerInfo(e.target.value)}
                placeholder="请输入客户信息，例如：
姓名：张三，电话：13800138000，本科学历，计算机专业，目标国家美国，预算50万，雅思6.5，意向学校哈佛大学..."
                className="w-full h-48 px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              />
            </div>
            <div className="flex gap-3">
              <Button onClick={handleJudge} disabled={isLoading} className="flex-1">
                <Brain className="w-5 h-5" />
                {isLoading ? '研判中...' : '开始研判'}
              </Button>
              <Button variant="success" onClick={handleJudgeAndSave} disabled={isLoading} className="flex-1">
                <CheckCircle className="w-5 h-5" />
                {isLoading ? '保存中...' : '研判并保存'}
              </Button>
            </div>
            {saveSuccess && (
              <div className="p-3 bg-green-100 text-green-700 rounded-lg flex items-center gap-2">
                <CheckCircle className="w-5 h-5" />
                客户信息已成功保存！
              </div>
            )}
          </div>
        </Card>

        <Card title="研判结果">
          {judgeResult ? (
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                {judgeResult.is_target ? (
                  <>
                    <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                      <CheckCircle className="w-6 h-6 text-green-600" />
                    </div>
                    <div>
                      <p className="text-lg font-bold text-green-600">目标客户</p>
                      <p className="text-sm text-gray-500">符合目标客户画像</p>
                    </div>
                  </>
                ) : (
                  <>
                    <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                      <XCircle className="w-6 h-6 text-red-600" />
                    </div>
                    <div>
                      <p className="text-lg font-bold text-red-600">非目标客户</p>
                      <p className="text-sm text-gray-500">暂不符合目标客户画像</p>
                    </div>
                  </>
                )}
              </div>

              <div className="p-4 bg-gray-50 rounded-lg">
                <p className="text-sm font-medium text-gray-700 mb-2">研判理由</p>
                <p className="text-sm text-gray-600">{judgeResult.reason}</p>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">
                  <Tag className="w-4 h-4 inline mr-2" />
                  标签
                </p>
                <div className="flex flex-wrap gap-2">
                  {judgeResult.tags.split(',').map((tag, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>

              {judgeResult.extracted_info && (
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-2">提取的客户信息</p>
                  <div className="grid grid-cols-2 gap-2">
                    {judgeResult.extracted_info.name && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">姓名</span>
                        <span className="text-gray-900">{judgeResult.extracted_info.name}</span>
                      </div>
                    )}
                    {judgeResult.extracted_info.phone && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">电话</span>
                        <span className="text-gray-900">{judgeResult.extracted_info.phone}</span>
                      </div>
                    )}
                    {judgeResult.extracted_info.email && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">邮箱</span>
                        <span className="text-gray-900">{judgeResult.extracted_info.email}</span>
                      </div>
                    )}
                    {judgeResult.extracted_info.country && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">目标国家</span>
                        <span className="text-gray-900">{judgeResult.extracted_info.country}</span>
                      </div>
                    )}
                    {judgeResult.extracted_info.education && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">学历</span>
                        <span className="text-gray-900">{judgeResult.extracted_info.education}</span>
                      </div>
                    )}
                    {judgeResult.extracted_info.budget && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">预算</span>
                        <span className="text-gray-900">{judgeResult.extracted_info.budget}万</span>
                      </div>
                    )}
                    {judgeResult.extracted_info.english_level && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">英语水平</span>
                        <span className="text-gray-900">{judgeResult.extracted_info.english_level}</span>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-64 text-gray-400">
              <Brain className="w-16 h-16 mb-4 opacity-50" />
              <p>请输入客户信息并点击研判</p>
              <p className="text-sm mt-2">系统将自动分析客户是否符合目标画像</p>
            </div>
          )}
        </Card>
      </div>

      <Card title="研判规则说明">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 bg-blue-50 rounded-lg">
            <h4 className="font-medium text-blue-800 mb-2">学历要求</h4>
            <p className="text-sm text-blue-600">本科及以上学历</p>
          </div>
          <div className="p-4 bg-green-50 rounded-lg">
            <h4 className="font-medium text-green-800 mb-2">预算要求</h4>
            <p className="text-sm text-green-600">30万以上</p>
          </div>
          <div className="p-4 bg-purple-50 rounded-lg">
            <h4 className="font-medium text-purple-800 mb-2">英语水平</h4>
            <p className="text-sm text-purple-600">雅思6.5/托福90+</p>
          </div>
          <div className="p-4 bg-orange-50 rounded-lg">
            <h4 className="font-medium text-orange-800 mb-2">目标国家</h4>
            <p className="text-sm text-orange-600">美、英、加、澳、新</p>
          </div>
        </div>
      </Card>
    </div>
  )
}

export default CustomerJudge