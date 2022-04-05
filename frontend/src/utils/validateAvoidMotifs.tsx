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
    callback(new Error('Only the following values are allowed: U, C, G, A,T'))
  } else {
    callback()
  }
}

export default {validateAvoidMotifs}
