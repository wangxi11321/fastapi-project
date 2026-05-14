import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './pages/Dashboard'
import Customers from './pages/Customers'
import Reports from './pages/Reports'
import LeaveApplications from './pages/LeaveApplications'
import Feedback from './pages/Feedback'
import Activities from './pages/Activities'
import CustomerJudge from './pages/CustomerJudge'

function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50">
      <Sidebar collapsed={sidebarCollapsed} onToggle={() => setSidebarCollapsed(!sidebarCollapsed)} />
      <div className={`flex-1 flex flex-col overflow-hidden transition-all duration-300 ${sidebarCollapsed ? 'ml-16' : 'ml-64'}`}>
        <Header onToggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)} />
        <main className="flex-1 overflow-y-auto p-6 scrollbar-thin">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/ai-assistant" element={<Dashboard />} />
            <Route path="/analysis" element={<Dashboard />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/judge" element={<CustomerJudge />} />
            <Route path="/follow-up" element={<Dashboard />} />
            <Route path="/students" element={<Dashboard />} />
            <Route path="/leaves" element={<LeaveApplications />} />
            <Route path="/activities" element={<Activities />} />
            <Route path="/risk" element={<Dashboard />} />
            <Route path="/emotion" element={<Dashboard />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/permissions" element={<Dashboard />} />
            <Route path="/settings" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}

export default App
