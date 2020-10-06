module.exports = {
  rules: {
    'no-label-var': 'error',
    'no-shadow': 'error',
    'no-undef-init': 'error',
    'no-use-before-define': ['error', { functions: false }],
    'no-delete-var': 'error',
    'no-shadow-restricted-names': 'error',
    'no-undef': 'error',
    'no-unused-vars': 'error',

    'init-declarations': 'off',
    'no-undefined': 'off',
    'no-restricted-globals': 'off'
  }
};
