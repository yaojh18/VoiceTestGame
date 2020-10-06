module.exports = {
  plugins: ['ember'],

  rules: {
    'ember/no-arrow-function-computed-properties': 'error',
    'ember/no-deeply-nested-dependent-keys-with-each': 'error',
    'ember/no-ember-super-in-es-classes': 'error',
    'ember/no-incorrect-calls-with-inline-anonymous-functions': 'error',
    'ember/no-invalid-debug-function-arguments': 'error',
    'ember/require-computed-property-dependencies': 'error',
    'ember/require-return-from-computed': 'error',
    'ember/jquery-ember-run': 'error',
    'ember/no-attrs-snapshot': 'error',
    'ember/no-duplicate-dependent-keys': 'error',
    'ember/no-ember-testing-in-module-scope': 'error',
    'ember/no-side-effects': 'error',
    'ember/require-super-in-init': 'error',
    'ember/routes-segments-snake-case': 'error',
    'ember/no-capital-letters-in-routes': 'error',
    'ember/no-invalid-dependent-keys': 'error',
    'ember/no-incorrect-computed-macros': 'error',
    'ember/no-attrs-in-components': 'error'
  }
};
