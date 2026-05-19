import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Legend } from "recharts"

export default function KPIChart({ kpi }) {
  return (
    <div className="bg-sap-card border border-sap-accent rounded-lg p-6">
      <div className="mb-6">
        <h3 className="text-xl font-bold text-sap-text">{kpi.name}</h3>
        <div className="flex items-center gap-4 mt-2">
          <div>
            <span className="text-xs text-sap-muted">Current</span>
            <p className="text-2xl font-bold text-sap-text">{kpi.value} {kpi.unit}</p>
          </div>
          <div>
            <span className="text-xs text-sap-muted">Threshold</span>
            <p className="text-2xl font-bold text-sap-muted">{kpi.threshold} {kpi.unit}</p>
          </div>
          <span
            className={`px-3 py-1 rounded-full text-sm ${
              kpi.status === "critical"
                ? "bg-red-900/30 text-red-400"
                : kpi.status === "warning"
                  ? "bg-yellow-900/30 text-yellow-400"
                  : "bg-green-900/30 text-green-400"
            }`}
          >
            {kpi.status}
          </span>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={kpi.trend}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="date" stroke="#94A3B8" />
          <YAxis stroke="#94A3B8" />
          <Tooltip
            contentStyle={{ backgroundColor: "#16213E", border: "1px solid #0F3460", borderRadius: "8px" }}
            labelStyle={{ color: "#E2E8F0" }}
          />
          <ReferenceLine y={kpi.threshold} stroke="#EF4444" strokeDasharray="5 5" label="Threshold" />
          <Line type="monotone" dataKey="value" stroke="#0070D2" strokeWidth={2} dot={{ fill: "#0070D2" }} name="Value" />
          <Legend />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
