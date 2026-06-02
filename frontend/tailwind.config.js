/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        coffee: {
          50: '#faf8f7',
          100: '#f5f3f0',
          500: '#8B4513',
          600: '#704010',
          700: '#5a340d',
          800: '#44250a',
        },
        primary: '#8B4513',
        secondary: '#704010',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}