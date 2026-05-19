import { useState } from "react"
import KPIChart from "./KPIChart"
import { TrendingUp, TrendingDown, Minus } from "lucide-react"

const statusColors = {
  healthy: "border-sap-success",
  warning: "border-sap-warning",
  critical: "border-sap-danger",
}

const statusBgColors = {
  healthy: "bg-sap-success/10",
  warning: "bg-sap-warning/10",
  critical: "bg-sap-danger/10",
}

export default function KPIGrid({ kpis }) {
  const [selectedKPI, setSelectedKPI] = useState(null)

  if (selectedKPI) {
    const kpi = kpis.find((k) => k.id === selectedKPI)
    return (
      <div>
        <button
          onClick={() => setSelectedKPI(null)}
          className="mb-4 text-sap-blue hover:underline text-sm"
        >
          &larr; Back to all KPIs
        </button>
        {kpi && <KPIChart kpi={kpi} />}
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {kpis.map((kpi) => {
        const trendDirection = kpi.trend.length >= 2
          ? kpi.trend[kpi.trend.length - 1].value > kpi.trend[kpi.trend.length - 2].value
            ? "up"
            : "down"
          : "flat"

        return (
          <button
            key={kpi.id}
            onClick={() => setSelectedKPI(kpi.id)}
            className={`bg-sap-card border-l-4 ${statusColors[kpi.status]} rounded-lg p-5 text-left hover:bg-sap-accent transition-colors`}
          >
            <div className="flex items-start justify-between mb-3">
              <h3 className="text-sm font-medium text-sap-text">{kpi.name}</h3>
              <span className={`px-2 py-0.5 rounded text-xs ${statusBgColors[kpi.status]} text-sap-muted`}>
                {kpi.status}
              </span>
            </div>
            <div className="flex items-end gap-2">
              <span className="text-2xl font-bold text-sap-text">{kpi.value}</span>
              <span className="text-sm text-sap-muted">{kpi.unit}</span>
            </div>
            <div className="mt-2 flex items-center gap-1 text-xs text-sap-muted">
              {trendDirection === "up" ? (
                <TrendingUp size={14} className="text-sap-success" />
              ) : trendDirection === "down" ? (
                <TrendingDown size={14} className="text-sap-danger" />
              ) : (
                <Minus size={14} />
              )}
              <span>Threshold: {kpi.threshold} {kpi.unit}</span>
            </div>
          </button>
        )
      })}
    </div>
  )
}
