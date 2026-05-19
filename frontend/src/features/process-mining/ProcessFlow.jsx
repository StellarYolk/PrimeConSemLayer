import { useCallback } from "react"
import { ReactFlow, Controls, Background, MiniMap, addEdge } from "@xyflow/react"
import "@xyflow/react/dist/style.css"
import CustomNode from "./CustomNode"

const nodeTypes = { custom: CustomNode }

export default function ProcessFlow({ nodes, edges, metrics }) {
  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [],
  )

  const centeredNodes = nodes.map((node) => ({
    ...node,
    position: {
      x: node.position.x + 400,
      y: node.position.y + 100,
    },
  }))

  return (
    <div className="bg-sap-card border border-sap-accent rounded-lg overflow-hidden">
      {metrics && (
        <div className="p-4 border-b border-sap-accent flex gap-6">
          <div>
            <span className="text-xs text-sap-muted">Cases</span>
            <p className="text-lg font-bold text-sap-text">{metrics.num_cases}</p>
          </div>
          <div>
            <span className="text-xs text-sap-muted">Events</span>
            <p className="text-lg font-bold text-sap-text">{metrics.num_events}</p>
          </div>
          <div>
            <span className="text-xs text-sap-muted">Activities</span>
            <p className="text-lg font-bold text-sap-text">{metrics.num_activities}</p>
          </div>
        </div>
      )}
      <div style={{ height: "600px" }}>
        <ReactFlow
          nodes={centeredNodes}
          edges={edges}
          nodeTypes={nodeTypes}
          onConnect={onConnect}
          fitView
        >
          <Controls />
          <MiniMap />
          <Background color="#334155" gap={16} />
        </ReactFlow>
      </div>
    </div>
  )
}
