module.exports = {
  rules: {
    /*
     * IMPORTANT
     * We found these rules help find bugs
     * and generally there is no reason against them.
     * If you were to disable any of it, think twice.
     */
    'prefer-promise-reject-errors': 'warn',
    'no-compare-neg-zero': 'error',
    'no-dupe-class-members': 'error',
    'import/no-duplicates': 'error',
    'import/named': 'error',
    'import/no-cycle': ['error', {maxDepth: 1}], // maxDepth for performance
    // Symbol is not intended to be used with the new operator,
    // but to be called as a function.
    'no-new-symbol': 'error',
    'no-return-await': 'error',
    'no-useless-rename': 'error',

    /*
     * PREFERRED
     * We found these rules to be useful and there is a positive case
     * for using this settings.
     * Your project may have special requirements
     * which justify different settings; YMMV.
     */
    'arrow-body-style': ['warn', 'as-needed'],
    'arrow-parens': ['warn', 'always'],
    'no-confusing-arrow': 'warn',
    'no-multi-assign': 'warn',
    'no-var': 'warn',
    'nonblock-statement-body-position': 'warn',
    'object-shorthand': 'warn',
    'prefer-const': 'warn',
    'prefer-template': 'warn',
    'require-await': 'warn',
    'require-yield': 'warn',
    'symbol-description': 'warn',

    /*
     * CONSISTENCY
     * These rules are in the sake of consistency.
     * Either settings is fine, depending on your team preference.
     * Feel free to adjust settings as you like - just do not disable them.
     */
    'array-bracket-spacing': ['warn', 'never'],
    'arrow-spacing': ['warn', {before: true, after: true}],
    'generator-star-spacing': 'warn',
    'prefer-arrow-callback': 'warn',
    'prefer-destructuring': 'warn',
    'rest-spread-spacing': ['warn', 'never'],
    'template-curly-spacing': ['warn', 'never'],
    'template-tag-spacing': 'warn',
    'yield-star-spacing': ['error', 'after'],
  },
}
