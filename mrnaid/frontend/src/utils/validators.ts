import {type ValidationRule} from 'antd/lib/form'
import {validateAvoidMotifs} from './validateAvoidMotifs'
import {validateCodingSequence} from './validateCodingSequence'

export const requiredField: ValidationRule = {
  required: true,
  message: 'Field is required',
}

export const geneField: ValidationRule = {
  type: 'string',
  pattern: /^[ACGTUacgtu]+$/,
  message: 'Only A, C, G ,T and U are allowed',
}

export const motifsField: ValidationRule = {
  validator: validateAvoidMotifs,
}

export const codingSequenceField: ValidationRule = {
  validator: validateCodingSequence,
}
