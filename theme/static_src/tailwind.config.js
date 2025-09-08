const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
  content: [
    '../templates/**/*.html', // Django templates in the app
    '../../templates/**/*.html', // Project-level templates
    '../../**/templates/**/*.html', // Any other app templates
  ],
  theme: {
    extend: {
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
