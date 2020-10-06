module.exports = {
  plugins: ['ember'],

  rules: {
    'ember/computed-property-getters': ['error', 'always'],
    'ember/no-proxies': 'error',
    'ember/classic-decorator-hooks': 'error',
    'ember/classic-decorator-no-classic-methods': 'error',
    'ember/avoid-leaking-state-in-ember-objects': 'error'
  }
};
