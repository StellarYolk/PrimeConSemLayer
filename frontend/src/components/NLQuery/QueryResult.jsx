import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

export default function QueryResult({ result }) {
  if (!result) return null

  return (
    <div className="mt-6 space-y-4">
      <div className="bg-sap-card border border-sap-accent rounded-lg p-6">
        <p className="text-sap-text leading-relaxed">{result.answer}</p>
      </div>
      {result.chart && result.chart.data && result.chart.data.length > 0 && (
        <div className="bg-sap-card border border-sap-accent rounded-lg p-6">
          <h3 className="text-sm font-medium text-sap-muted mb-4">{result.chart.title || "Data Visualization"}</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={result.chart.data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={result.chart.x_key} stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip
                contentStyle={{ backgroundColor: "#16213E", border: "1px solid #0F3460", borderRadius: "8px" }}
                labelStyle={{ color: "#E2E8F0" }}
              />
              <Bar dataKey={result.chart.y_key} fill="#0070D2" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
