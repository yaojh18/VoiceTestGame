const glob = require('glob');
const path = require('path');

function getPluginRules(name) {
  const packageDir = path.dirname(require.resolve(`${name}/package.json`));
  const rulesPaths = glob.sync(`${packageDir}/lib/rules/*.js`, {});

  return rulesPaths.map((filePath) => {
    const rule = require(filePath);
    const regexp = `^${packageDir}/lib/rules/(?<ruleName>.+).js`;
    const { ruleName } = filePath.match(regexp).groups;

    if (ruleName === 'index') return null;

    return { name: ruleName, deprecated: rule.meta && rule.meta.deprecated };
  }).filter((a) => a);
}

function getPackageRules(name) {
  const pluginRulesFilesPaths = glob.sync(`lib/configs/-private/${name}/*.js`, {});

  return pluginRulesFilesPaths.map((filePath) => {
    const ruleFiles = require(`../../${filePath}`);

    return Object.keys(ruleFiles.rules).map((rule) => ({ name: rule }));
  }).flat();
}

module.exports = {
  getPackageRules,
  getPluginRules
};
