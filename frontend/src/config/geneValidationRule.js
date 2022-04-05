export const geneValidationRule = {
  type: 'string',
  pattern: /^[ACGTUacgtu]+$/,
  message: 'Only A, C, G ,T and U are allowed',
}
