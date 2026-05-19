import { useState, useEffect } from "react"
import KPIGrid from "../features/dashboards/KPIGrid"
import LoadingSpinner from "../components/shared/LoadingSpinner"
import { dashboardAPI } from "../api/client"

export default function KPIDashboard() {
  const [kpis, setKpis] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    dashboardAPI
      .listKPIs()
      .then((data) => setKpis(data.kpis))
      .catch((err) => console.error("Failed to load KPIs:", err))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-sap-text mb-2">KPI Dashboards</h2>
        <p className="text-sap-muted">Monitor 19 key performance indicators across your SAP processes</p>
      </div>
      {loading ? <LoadingSpinner text="Loading KPIs..." /> : <KPIGrid kpis={kpis} />}
    </div>
  )
}
