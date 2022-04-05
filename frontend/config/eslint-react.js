module.exports = {
  rules: {
    /*
     * IMPORTANT
     * We found these rules help find bugs
     * and generally there is no reason against them.
     * If you were to disable any of it, think twice.
     */
    'react/no-deprecated': 'warn',
    // Updating the state after a component mount will trigger a second render() call
    // and can lead to property/layout thrashing
    'react/no-did-mount-set-state': 'warn',
    'react/no-did-update-set-state': 'warn',
    'react/no-direct-mutation-state': 'error',
    'react/no-is-mounted': 'error',
    'react/no-render-return-value': 'error',
    'react/no-string-refs': 'error',
    'react/no-unescaped-entities': 'error',
    'react/no-unknown-property': 'error',
    'react/no-unused-prop-types': 'off', // too many false positives
    'react/require-render-return': 'error',
    'react/style-prop-object': 'warn',
    'react/jsx-key': 'warn',
    'react/jsx-no-comment-textnodes': 'warn',
    'react/jsx-no-duplicate-props': [
      'error',
      {
        ignoreCase: true,
      },
    ],
    'react/jsx-no-target-blank': 'error',
    'react/jsx-no-undef': 'error',
    'react/jsx-pascal-case': 'error',
    'react/jsx-uses-react': 'warn',
    'react/jsx-uses-vars': 'warn',
    'react/jsx-wrap-multilines': 'warn',
    'react/no-typos': 'error',
    'react/default-props-match-prop-types': 'warn',
    'react/no-children-prop': 'warn',
    /*
     * PREFERRED
     * We found these rules to be useful and there is a positive case
     * for using this settings.
     * Your project may have special requirements
     * which justify different settings; YMMV.
     */
    'react/prop-types': 'warn',
    'react/react-in-jsx-scope': 'off',
    'react/sort-comp': 'warn',
    'react/jsx-boolean-value': 'warn',
    'react/jsx-no-bind': 'off', // not useful in function components
    'react/void-dom-elements-no-children': 'warn',
    'react/no-danger-with-children': 'warn',
    'react/no-unused-state': 'warn',
    'react/forbid-foreign-prop-types': 'warn',
    'react/no-redundant-should-component-update': 'warn',
    'react/require-default-props': 'warn',
    'react/no-array-index-key': 'warn',
    /*
     * CONSISTENCY
     * These rules are in the sake of consistency.
     * Either settings is fine, depending on your team preference.
     * Feel free to adjust settings as you like - just do not disable them.
     */
    'react/display-name': 'off',
    'react/prefer-es6-class': ['error', 'always'],
    'react/prefer-stateless-function': 'warn',
    'react/require-optimization': 'warn',
    'react/self-closing-comp': 'warn',
    'react/sort-prop-types': [
      'warn',
      {
        callbacksLast: true,
        requiredFirst: true,
      },
    ],
    'react/jsx-closing-bracket-location': [
      'warn',
      {
        nonEmpty: 'after-props',
        selfClosing: 'props-aligned',
      },
    ],
    'react/jsx-curly-spacing': ['warn', 'never'],
    'react/jsx-equals-spacing': ['warn', 'never'],
    'react/jsx-filename-extension': [
      'warn',
      {
        extensions: ['.js', '.jsx', '.tsx'],
      },
    ],
    'react/jsx-first-prop-new-line': ['warn', 'multiline-multiprop'],
    'react/jsx-handler-names': 'warn',
    'react/jsx-indent': ['warn', 2],
    'react/jsx-indent-props': ['warn', 2],
    'react/jsx-max-props-per-line': [
      'warn',
      {
        maximum: 3,
      },
    ],
    'react/jsx-no-literals': 'off',
    'react/jsx-sort-props': 'off',
    'react/jsx-tag-spacing': 'warn',
    'react/forbid-elements': 'off',
    'react/jsx-closing-tag-location': 'warn',
    'react/boolean-prop-naming': 'off',
  },
  extends: ['plugin:react-hooks/recommended', 'plugin:jsx-a11y/recommended'],
}
