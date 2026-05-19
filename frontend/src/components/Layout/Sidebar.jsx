import { NavLink } from "react-router-dom"
import { LayoutDashboard, GitBranch, BarChart3, Search } from "lucide-react"

const navItems = [
  { to: "/", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/process-mining", icon: GitBranch, label: "Process Mining" },
  { to: "/dashboards", icon: BarChart3, label: "KPI Dashboards" },
  { to: "/rca", icon: Search, label: "Root Cause Analysis" },
]

export default function Sidebar() {
  return (
    <aside className="w-64 bg-sap-dark border-r border-sap-accent flex flex-col">
      <div className="p-6 border-b border-sap-accent">
        <h1 className="text-xl font-bold text-sap-blue">PrimeCon</h1>
        <p className="text-xs text-sap-muted mt-1">Semantic Layer</p>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? "bg-sap-blue text-white"
                  : "text-sap-text hover:bg-sap-accent"
              }`
            }
          >
            <Icon size={18} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
