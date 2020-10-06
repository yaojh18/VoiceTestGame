module.exports = {
  root: true,

  parserOptions: {
    ecmaVersion: 2018
  },

  env: {
    es6: true,
    browser: true
  },

  extends: [
    require.resolve('./recommended.js')
  ]
};
