import { Routes, Route } from "react-router-dom"
import Layout from "./components/Layout/Layout"
import Dashboard from "./pages/Dashboard"
import ProcessMining from "./pages/ProcessMining"
import KPIDashboard from "./pages/KPIDashboard"
import RCA from "./pages/RCA"

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="process-mining" element={<ProcessMining />} />
        <Route path="dashboards" element={<KPIDashboard />} />
        <Route path="rca" element={<RCA />} />
      </Route>
    </Routes>
  )
}

export default App
