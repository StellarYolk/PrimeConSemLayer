export default function LoadingSpinner({ text = "Loading..." }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 gap-4">
      <div className="w-10 h-10 border-4 border-sap-accent border-t-sap-blue rounded-full animate-spin" />
      <p className="text-sap-muted text-sm">{text}</p>
    </div>
  )
}
