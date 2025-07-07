/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"SFPro"', 'sans-serif'],
      },
      fontSize: {
        header1: ['96px', { lineHeight: '96px', fontWeight: '500' }],
        header2: ['40px', { lineHeight: '48px', fontWeight: '400' }],
        body: ['16px', { lineHeight: '24px', fontWeight: '400' }],
        caption: ['12px', { lineHeight: '16px', fontWeight: '300' }],
      },
    },
  },
  plugins: [],
}