import {ResponseData, InputAndResultData, InputParameters} from './Api'

export const responseToResultData = (response: ResponseData): ResultData => ({
  results: response.optimized,
  input: response.input,
  inputParameters: response.input_parameters,
})

export type ResultData = {
  results: InputAndResultData[]
  input: InputAndResultData
  inputParameters: InputParameters
}

export type Result = {
  seqId: string
  RNASeq: string
}
