module.exports = {
  rules: {
    /*
     * IMPORTANT
     * We found these rules help find bugs
     * and generally there is no reason against them.
     * If you were to disable any of it, think twice.
     */
    'array-callback-return': 'error',
    // Emulates C-like scope for var. Has no effect on let / const
    'block-scoped-var': 'error',
    eqeqeq: ['error', 'always', {null: 'ignore'}],
    'for-direction': 'error',
    'guard-for-in': 'warn',
    'handle-callback-err': ['error', '^(err|error)$'],
    'linebreak-style': ['warn', 'unix'],
    'no-array-constructor': 'error',
    'no-buffer-constructor': 'error',
    'no-caller': 'error',
    'no-case-declarations': 'error',
    'no-class-assign': 'error',
    'no-cond-assign': ['error', 'always'],
    'no-const-assign': 'error',
    'no-constant-condition': ['error', {checkLoops: false}],
    'no-control-regex': 'error',
    'no-debugger': 'error',
    'no-delete-var': 'error',
    'no-dupe-args': 'error',
    'no-dupe-keys': 'error',
    'no-duplicate-case': 'error',
    /*
     * Empty block statements, while not technically errors,
     * usually occur due to refactoring that wasn’t completed.
     * Empty block with comment (such as ignored catch) is possible.
     */
    'no-empty': 'error',
    'no-empty-character-class': 'error',
    'no-empty-function': 'error',
    'no-empty-pattern': 'error',
    'no-eval': 'error',
    'no-extra-semi': 'warn',
    'no-ex-assign': 'error',
    'no-extend-native': 'error',
    'no-floating-decimal': 'error',
    'no-func-assign': 'error',
    'no-global-assign': 'error',
    'no-implied-eval': 'error',
    'no-inner-declarations': ['error', 'functions'],
    'no-invalid-regexp': 'error',
    'no-irregular-whitespace': 'error',
    /*
     * The __iterator__ property was a SpiderMonkey extension.
     * This property is now obsolete, so it should not be used.
     */
    'no-iterator': 'error',
    'no-label-var': 'error',
    'no-lonely-if': 'warn',
    'no-lone-blocks': 'error',
    'no-mixed-operators': 'warn',
    'no-mixed-spaces-and-tabs': 'error',
    'no-multi-spaces': 'warn',
    /*
     * It’s possible to create functions in JavaScript using
     * the Function constructor. Disallows this.
     */
    'no-new-func': 'error',
    // Forces Object literals
    'no-new-object': 'error',
    'no-new-require': 'error',
    'no-new-wrappers': 'error',
    'no-obj-calls': 'error',
    'no-octal': 'error',
    'no-octal-escape': 'error',
    'no-param-reassign': ['error', {props: false}],
    'no-plusplus': 'off',
    'no-proto': 'error',
    'no-redeclare': 'error',
    'no-regex-spaces': 'error',
    'no-return-assign': 'error',
    'no-self-assign': ['error', {props: false}],
    'no-self-compare': 'error',
    'no-sequences': 'error',
    /*
     * Shadowing is the process by which a local variable
     * shares the same name as a variable in its containing scope.
     * This can cause confusion and it's impossible to access
     * the outer variable.
     */
    'no-shadow': 'error',
    'no-shadow-restricted-names': 'error',
    'no-sparse-arrays': 'error',
    'no-template-curly-in-string': 'error',
    'no-this-before-super': 'error',
    'no-throw-literal': 'error',
    'no-trailing-spaces': 'warn',
    'no-undef': 'error',
    'no-undef-init': 'error',
    'no-unexpected-multiline': 'warn',
    'no-unreachable': 'error',
    'no-unsafe-finally': 'error',
    'no-unsafe-negation': 'error',
    'no-unused-expressions': ['warn', {allowShortCircuit: true}],
    'no-unused-labels': 'error',
    'no-useless-call': 'error',
    'no-useless-computed-key': 'error',
    'no-useless-concat': 'warn',
    'no-useless-constructor': 'error',
    'no-useless-escape': 'error',
    'no-whitespace-before-property': 'error',
    'no-with': 'error',
    'unicode-bom': ['error', 'never'],
    strict: 'error',
    'use-isnan': 'error',
    'valid-typeof': 'error',
    'wrap-iife': ['error', 'any'],

    /*
     * PREFERRED
     * We found these rules to be useful and there is a positive case
     * for using this settings.
     * Your project may have special requirements
     * which justify different settings; YMMV.
     */
    // Require return statements to either always or never specify values.
    'consistent-return': 'error',
    'constructor-super': 'error',
    curly: ['error', 'multi-line'],
    // Require Default Case in Switch Statements
    'default-case': 'warn',
    'eol-last': 'error',
    'global-require': 'warn',
    'new-cap': ['error', {newIsCap: true, capIsNew: false}],
    'new-parens': 'error',
    'no-alert': 'warn',
    'no-bitwise': 'warn',
    'no-console': 'warn',
    'no-continue': 'warn',
    'no-extra-bind': 'error',
    'no-extra-boolean-cast': 'error',
    'no-extra-parens': ['error', 'functions'],
    'no-fallthrough': 'error',
    'no-labels': ['error', {allowLoop: false, allowSwitch: false}],
    'no-extra-label': 'error',
    /*
     * Writing functions within loops tends to result in errors
     * due to the way the function creates a closure around the loop.
     */
    'no-loop-func': 'warn',
    'no-multi-str': 'warn',
    // Nested ternaries are difficult to read
    'no-nested-ternary': 'warn',
    // Disallow new For Side Effects
    'no-new': 'error',
    'no-path-concat': 'error',
    'no-prototype-builtins': 'warn',
    'no-unmodified-loop-condition': 'error',
    'no-unneeded-ternary': ['error', {defaultAssignment: false}],
    'no-unused-vars': ['error', {vars: 'all', args: 'after-used'}],
    'no-use-before-define': 'warn',
    'no-void': 'error',
    'object-property-newline': ['warn', {allowMultiplePropertiesPerLine: true}],

    /*
     * CONSISTENCY
     * These rules are in the sake of consistency.
     * Either settings is fine, depending on your team preference.
     * Feel free to adjust settings as you like - just do not disable them.
     */
    'accessor-pairs': 'warn',
    'block-spacing': ['warn', 'always'],
    'brace-style': ['warn', '1tbs', {allowSingleLine: true}],
    camelcase: ['warn', {properties: 'never'}],
    'comma-dangle': ['warn', 'always-multiline'],
    'comma-spacing': ['warn', {before: false, after: true}],
    'comma-style': ['warn', 'last'],
    'computed-property-spacing': ['warn', 'never'],
    'dot-location': ['warn', 'property'],
    'dot-notation': 'warn',
    'func-call-spacing': ['warn', 'never'],
    'func-names': 'warn',
    indent: ['warn', 2, {VariableDeclarator: 2, SwitchCase: 1}],
    'jsx-quotes': ['warn', 'prefer-double'],
    'key-spacing': ['warn', {beforeColon: false, afterColon: true}],
    'keyword-spacing': ['warn', {before: true, after: true}],
    'max-len': ['warn', {code: 100, ignoreComments: true}],
    'newline-per-chained-call': ['warn', {ignoreChainWithDepth: 2}],
    'no-else-return': 'warn',
    'no-multiple-empty-lines': ['warn', {max: 1}],
    'no-tabs': 'warn',
    'object-curly-spacing': 'warn',
    'one-var': ['warn', 'never'],
    'one-var-declaration-per-line': 'warn',
    'operator-linebreak': ['warn', 'after', {overrides: {'?': 'before', ':': 'before'}}],
    'padded-blocks': ['warn', 'never'],
    quotes: ['warn', 'single', {avoidEscape: true, allowTemplateLiterals: true}],
    'quote-props': ['warn', 'consistent-as-needed'],
    semi: ['warn', 'never'],
    'semi-style': ['warn', 'first'],
    'semi-spacing': ['warn', {before: false, after: true}],
    'space-before-blocks': ['warn', 'always'],
    'space-before-function-paren': ['warn', 'never'],
    'space-in-parens': ['warn', 'never'],
    'space-infix-ops': 'warn',
    'space-unary-ops': ['warn', {words: true, nonwords: false}],
    'spaced-comment': [
      'warn',
      'always',
      {
        line: {markers: ['*package', '!', ',']},
        block: {balanced: true, markers: ['*package', '!', ','], exceptions: ['*']},
      },
    ],
    'switch-colon-spacing': 'warn',
    'vars-on-top': 'warn',
    yoda: ['warn', 'never'],
  },
}
