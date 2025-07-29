/** @type {import('stylelint').Config} */
export default {
  extends: [
    "stylelint-config-standard",
    "stylelint-config-recommended",
    "stylelint-config-alphabetical-order",
  ],
  rules: {
    "block-no-empty": true,
    "selector-class-pattern": ["^([a-z][a-z0-9]*)(_[a-z0-9]+)*$", {"disableFix": true}],
  },
};
