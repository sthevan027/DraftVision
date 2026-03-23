/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#7C3AED',
        accent: '#22C55E',
        surface: '#1F2937',
        background: '#0F172A',
      },
    },
  },
  plugins: [],
};
