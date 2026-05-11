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
      <Sidebar collapsed={sidebarCollapsed} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header onToggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)} />
        <main className="flex-1 overflow-y-auto p-6 scrollbar-thin">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/judge" element={<CustomerJudge />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/leaves" element={<LeaveApplications />} />
            <Route path="/feedback" element={<Feedback />} />
            <Route path="/activities" element={<Activities />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}

export default App