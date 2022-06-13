export const validateCodingSequence = (
  rule: string,
  values: string[],
  callback: (e?: Error) => void,
) => {
  if (values.length % 3 !== 0 ) {
    callback(new Error('The length must be a multiple of three'))
  } else {
    callback()
  }
}
export default {validateCodingSequence}