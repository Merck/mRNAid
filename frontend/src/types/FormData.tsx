import {RequestData} from './Api'

export type FormData = {
  inputSequenceType: string
  fivePrimeFlankingSequence: string
  goiSequence: string
  threePrimeFlankingSequence: string
  useDegeneracyCodon: boolean
  uridineDepletion: boolean
  cAI: boolean
  preciseMFEAlgorithm: boolean
  dinucleotides: boolean
  matchCodonPair: boolean
  codonUsage: string
  taxonomyId: string
  codonUsageFrequencyThresholdPct: number
  numberOfSequences: number
  gcContentMin: number
  gcContentMax: number
  gcContentGlobal: number
  gcWindowSize: number
  entropyWindowSize: number
  fileName: string
  avoidMotifs: string[]
  organism: string
}

export type FormParamsCombined = RequestData & FormData
