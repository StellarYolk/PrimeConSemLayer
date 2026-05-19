import axios from "axios"

const API_BASE_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL.replace(/\/$/, "")}/api`
  : "/api"

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

export const queryAPI = {
  processQuery: (query) => api.post("/query/", { query }).then((r) => r.data),
}

export const processMiningAPI = {
  discover: (processType) =>
    api.post("/process-mining/discover", { process_type: processType, sample_data: true }).then((r) => r.data),
  conformance: (processType) =>
    api.post("/process-mining/conformance", { process_type: processType, mode: "conformance", sample_data: true }).then((r) => r.data),
}

export const dashboardAPI = {
  listKPIs: () => api.get("/dashboards/list").then((r) => r.data),
  getKPI: (kpiId) => api.get(`/dashboards/${kpiId}`).then((r) => r.data),
  getKPITrend: (kpiId) => api.get(`/dashboards/${kpiId}/trend`).then((r) => r.data),
}

export const rcaAPI = {
  analyze: (query) => api.post("/rca/analyze", { query }).then((r) => r.data),
  diagnose: (kpiId) => api.post(`/rca/diagnose/${kpiId}`).then((r) => r.data),
}

export default api
