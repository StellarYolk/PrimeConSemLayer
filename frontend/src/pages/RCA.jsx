import { useState } from "react"
import QueryInput from "../components/NLQuery/QueryInput"
import LoadingSpinner from "../components/shared/LoadingSpinner"
import { rcaAPI } from "../api/client"
import { AlertCircle, AlertTriangle, CheckCircle, Info } from "lucide-react"

const severityIcons = {
  critical: <AlertCircle className="text-sap-danger" size={20} />,
  high: <AlertTriangle className="text-sap-warning" size={20} />,
  medium: <Info className="text-sap-blue" size={20} />,
  info: <CheckCircle className="text-sap-success" size={20} />,
}

export default function RCA() {
  const [rcaResult, setRcaResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleQuery = async (query) => {
    setLoading(true)
    try {
      const data = await rcaAPI.analyze(query)
      setRcaResult(data)
    } catch (err) {
      setRcaResult({ summary: "Failed to perform RCA. Specify a valid KPI name." })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-sap-text mb-2">Root Cause Analysis</h2>
        <p className="text-sap-muted">Identify root causes of KPI deviations and process anomalies</p>
      </div>
      <QueryInput onSubmit={handleQuery} loading={loading} />
      {loading && <LoadingSpinner text="Analyzing root causes..." />}
      {rcaResult && (
        <div className="mt-6 space-y-4">
          <div className="bg-sap-card border border-sap-accent rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-sap-text">{rcaResult.kpi_name}</h3>
              <span
                className={`px-3 py-1 rounded-full text-sm ${
                  rcaResult.status === "critical"
                    ? "bg-red-900/30 text-red-400"
                    : rcaResult.status === "warning"
                      ? "bg-yellow-900/30 text-yellow-400"
                      : "bg-green-900/30 text-green-400"
                }`}
              >
                {rcaResult.status}
              </span>
            </div>
            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="bg-sap-dark rounded-lg p-3">
                <p className="text-xs text-sap-muted">Current Value</p>
                <p className="text-xl font-bold text-sap-text">{rcaResult.current_value}</p>
              </div>
              <div className="bg-sap-dark rounded-lg p-3">
                <p className="text-xs text-sap-muted">Threshold</p>
                <p className="text-xl font-bold text-sap-text">{rcaResult.threshold}</p>
              </div>
              <div className="bg-sap-dark rounded-lg p-3">
                <p className="text-xs text-sap-muted">Factors Found</p>
                <p className="text-xl font-bold text-sap-text">{rcaResult.steps?.length || 0}</p>
              </div>
            </div>
            <p className="text-sap-text text-sm">{rcaResult.summary}</p>
          </div>
          {rcaResult.steps && (
            <div className="space-y-3">
              {rcaResult.steps.map((step) => (
                <div key={step.step_number} className="bg-sap-card border border-sap-accent rounded-lg p-5">
                  <div className="flex items-start gap-3">
                    <div className="mt-0.5">{severityIcons[step.severity]}</div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xs font-mono text-sap-muted">Step {step.step_number}</span>
                        <h4 className="font-semibold text-sap-text">{step.title}</h4>
                      </div>
                      <p className="text-sm text-sap-text mb-2">{step.description}</p>
                      <p className="text-sm text-sap-muted italic">{step.finding}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
