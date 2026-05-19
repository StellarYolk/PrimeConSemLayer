import { useState, useEffect } from "react"
import { Zap, ZapOff } from "lucide-react"

export default function Header() {
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    fetch("/health")
      .then((r) => r.json())
      .then(() => setConnected(true))
      .catch(() => setConnected(false))
  }, [])

  return (
    <header className="bg-sap-dark border-b border-sap-accent px-6 py-4 flex items-center justify-between">
      <h2 className="text-lg font-semibold text-sap-text">PrimeCon Semantic Layer</h2>
      <div className="flex items-center gap-2">
        {connected ? (
          <>
            <Zap size={16} className="text-sap-success" />
            <span className="text-sm text-sap-success">Backend Connected</span>
          </>
        ) : (
          <>
            <ZapOff size={16} className="text-sap-warning" />
            <span className="text-sm text-sap-warning">Backend Disconnected</span>
          </>
        )}
      </div>
    </header>
  )
}
