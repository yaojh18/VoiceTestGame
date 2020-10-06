const { getPackageRules, getPluginRules } = require('./utils/rules');

it('does not use eslint deprecated rules', () => {
  const eslintRules = getPluginRules('eslint');
  const rules = getPackageRules('eslint');

  const deprecatedRules = eslintRules.filter((rule) => rule.deprecated && rules.includes(rule.name));

  expect(deprecatedRules.length).toBe(0);
});

it('specifies all eslint rules', () => {
  const eslintRules = getPluginRules('eslint').filter((rule) => !rule.deprecated);
  const rules = getPackageRules('eslint');

  expect(rules.map((rule) => rule.name).sort()).toEqual(eslintRules.map((rule) => rule.name).sort());
});

it('specifies all ember rules', () => {
  const emberRules = getPluginRules('eslint-plugin-ember');
  const rules = getPackageRules('ember').map((rule) => {
    rule.name = rule.name.replace('ember/', '');

    return rule;
  });

  expect(rules.map((rule) => rule.name).sort()).toEqual(emberRules.map((rule) => rule.name).sort());
});
