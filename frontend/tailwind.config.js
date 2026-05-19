/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        sap: {
          blue: "#0070D2",
          dark: "#1A1A2E",
          darker: "#0F0F1A",
          card: "#16213E",
          accent: "#0F3460",
          success: "#10B981",
          warning: "#F59E0B",
          danger: "#EF4444",
          text: "#E2E8F0",
          muted: "#94A3B8",
        },
      },
    },
  },
  plugins: [],
}
