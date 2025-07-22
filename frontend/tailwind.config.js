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
      },colors: {
        black: '#000000',
        'black-50': 'rgba(0,0,0,0.5)',
        'gray-666': '#666666',
        'gray-11': 'rgba(210, 206, 206, 0.11)',
        'gray-dark': '#171717',
        'purple-accent': '#9C79D4',
        'gris': 'rgba(229, 229, 229, 0.50)',
        white: '#FFFFFF',
        'white-soft': '#FFFEFE',
        joie: "#FDD835",
        detente: "#A3D5FF",
        enthousiasme: "#FFB74D",
        motivation: "#FF7043",
        envieDeDanser: "#4DB6AC",
        excitation: "#D81B90",
        tristesse: "#7986CB",
        colere: "#EF5350",
        melancolie: "#B39DDB",
        nostalgie: "#F3C6F1",
        neutre: "#B0BEC5",
        confiance: "#81C784"
      } 
    },
  },
  plugins: [],
}