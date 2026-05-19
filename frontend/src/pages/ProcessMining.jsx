import { useState } from "react"
import ProcessFlow from "../features/process-mining/ProcessFlow"
import LoadingSpinner from "../components/shared/LoadingSpinner"
import { processMiningAPI } from "../api/client"

const processTypes = [
  { value: "procure-to-pay", label: "Procure-to-Pay" },
  { value: "order-to-cash", label: "Order-to-Cash" },
  { value: "record-to-report", label: "Record-to-Report" },
]

export default function ProcessMining() {
  const [processType, setProcessType] = useState("order-to-cash")
  const [flowData, setFlowData] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleDiscover = async () => {
    setLoading(true)
    try {
      const data = await processMiningAPI.discover(processType)
      setFlowData(data)
    } catch (err) {
      console.error("Process mining error:", err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-sap-text mb-2">Process Mining</h2>
        <p className="text-sap-muted">Discover and analyze SAP process flows</p>
      </div>
      <div className="flex gap-4 mb-6">
        <select
          value={processType}
          onChange={(e) => setProcessType(e.target.value)}
          className="bg-sap-card border border-sap-accent rounded-lg px-4 py-2 text-sap-text focus:outline-none focus:border-sap-blue"
        >
          {processTypes.map((pt) => (
            <option key={pt.value} value={pt.value}>
              {pt.label}
            </option>
          ))}
        </select>
        <button
          onClick={handleDiscover}
          disabled={loading}
          className="bg-sap-blue hover:bg-blue-600 disabled:opacity-50 text-white px-6 py-2 rounded-lg transition-colors"
        >
          Discover Process
        </button>
      </div>
      {loading && <LoadingSpinner text="Discovering process flow..." />}
      {flowData && <ProcessFlow nodes={flowData.nodes} edges={flowData.edges} metrics={flowData.metrics} />}
    </div>
  )
}
