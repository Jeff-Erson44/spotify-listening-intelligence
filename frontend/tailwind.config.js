/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "./app/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
        gridTemplateColumns: {
        16: 'repeat(16, minmax(0, 1fr))',
      }
    },
  },
  plugins: [],
}