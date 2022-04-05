module.exports = {
  rules: {
    /*
     * IMPORTANT
     * We found these rules help find bugs
     * and generally there is no reason against them.
     * If you were to disable any of it, think twice.
     */
    /*
     * We need to reset some of eslint rules,
     * because there are in conflict with typescript
     * rules.
     */
    'no-unused-vars': 'off',
    'no-useless-constructor': 'off',
    'react/jsx-closing-bracket-location': 'off',
    'react/jsx-filename-extension': 'off',
    'react/prop-types': 'off',
    semi: 'off',
    'semi-style': ['error', 'last'],
    /*
     * PREFERRED
     * We found these rules to be useful and there is a positive case
     * for using this settings.
     * Your project may have special requirements
     * which justify different settings; YMMV.
     */
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-explicit-any': 'off',
    '@typescript-eslint/no-unused-vars': [
      'error',
      {
        vars: 'all',
        args: 'after-used',
        ignoreRestSiblings: true,
        argsIgnorePattern: '^_',
      },
    ],
    '@typescript-eslint/no-useless-constructor': 'error',
    '@typescript-eslint/semi': ['warn', 'never'], // should be consistent with index.js
    'no-use-before-define': 'off',
    '@typescript-eslint/no-use-before-define': ['error'],
    'no-shadow': 'off',
    '@typescript-eslint/no-shadow': ['error'],
  },
}
