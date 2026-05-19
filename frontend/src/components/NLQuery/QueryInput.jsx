import { useState } from "react"
import { Send } from "lucide-react"

export default function QueryInput({ onSubmit, loading }) {
  const [query, setQuery] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim() && !loading) {
      onSubmit(query.trim())
      setQuery("")
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask about your SAP data... (e.g., 'Show me sales orders' or 'Why did cycle time increase?')"
        className="flex-1 bg-sap-card border border-sap-accent rounded-lg px-4 py-3 text-sap-text placeholder-sap-muted focus:outline-none focus:border-sap-blue"
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading || !query.trim()}
        className="bg-sap-blue hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg flex items-center gap-2 transition-colors"
      >
        <Send size={18} />
        <span>Ask</span>
      </button>
    </form>
  )
}
