import { useState } from "react"
import QueryInput from "../components/NLQuery/QueryInput"
import QueryResult from "../components/NLQuery/QueryResult"
import LoadingSpinner from "../components/shared/LoadingSpinner"
import { queryAPI } from "../api/client"

export default function Dashboard() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleQuery = async (query) => {
    setLoading(true)
    try {
      const data = await queryAPI.processQuery(query)
      setResult(data)
    } catch (err) {
      setResult({ answer: "Failed to process query. Ensure backend is running." })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-sap-text mb-2">Natural Language Query</h2>
        <p className="text-sap-muted">Ask questions about your SAP data in plain English</p>
      </div>
      <QueryInput onSubmit={handleQuery} loading={loading} />
      {loading && <LoadingSpinner text="Processing your query..." />}
      <QueryResult result={result} />
    </div>
  )
}
