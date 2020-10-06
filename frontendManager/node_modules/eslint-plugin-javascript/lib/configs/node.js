module.exports = {
  root: true,

  parserOptions: {
    ecmaVersion: 2018,
    sourceType: 'module'
  },

  env: {
    es6: true,
    node: true
  },

  plugins: ['node'],

  extends: [
    'plugin:node/recommended',
    require.resolve('./recommended.js'),
    require.resolve('./-private/eslint/node.js'),
    require.resolve('./-private/eslint/strict-mode.js')
  ],

  rules: {
    'node/no-unpublished-require': 'off'
  }
};
