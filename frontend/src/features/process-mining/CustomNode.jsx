import { Handle, Position } from "@xyflow/react"

const typeColors = {
  start: { bg: "#10B981", border: "#059669" },
  end: { bg: "#EF4444", border: "#DC2626" },
  activity: { bg: "#0070D2", border: "#0059A3" },
}

export default function CustomNode({ data }) {
  const colors = typeColors[data.node_type] || typeColors.activity

  return (
    <div
      className="rounded-lg shadow-lg min-w-[180px] px-4 py-3"
      style={{ backgroundColor: colors.bg + "20", border: `2px solid ${colors.border}` }}
    >
      <Handle type="target" position={Position.Top} style={{ background: colors.border }} />
      <div className="text-center">
        <p className="text-sm font-semibold text-sap-text">{data.label}</p>
        <p className="text-xs text-sap-muted mt-1">Freq: {data.frequency}</p>
      </div>
      <Handle type="source" position={Position.Bottom} style={{ background: colors.border }} />
    </div>
  )
}
