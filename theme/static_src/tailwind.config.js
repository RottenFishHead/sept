const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
  content: [
    '../templates/**/*.html', // Django templates in the app
    '../../templates/**/*.html', // Project-level templates
    '../../**/templates/**/*.html', // Any other app templates
  ],
  theme: {
    extend: {
      keyframes: {
        gradient: { '0%, 100%': { backgroundPosition: '0% 50%' }, '50%': { backgroundPosition: '100% 50%' } }
  },
        animation: { gradient: 'gradient 8s ease infinite' },
      colors: {
        primary: '#5d8eb9',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
