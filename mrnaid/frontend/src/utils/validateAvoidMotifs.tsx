import {motifs} from '../config/motifs'

export const validateAvoidMotifs = (rule: string, values: string[], callback: (e?: Error) => void) => {
  if (!values) {
    callback()
    return
  }

  // Allowed custom values
  const customMotifsRegex = /^[UCAGTucagt]+$/
  // Exclude motifs selection list
  const customInputs = values.filter((value: string) => !motifs.includes(value))
  const invalidInputs = customInputs.filter((value: string) => !value.match(customMotifsRegex))
  if (invalidInputs.length !== 0) {
    callback(new Error('Only A, C, G ,T and U are allowed'))
  } else {
    callback()
  }
}

export default {validateAvoidMotifs}
