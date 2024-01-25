import {RequestData} from './Api'

export type FormData = {
  inputSequenceType: string
  fivePrimeFlankingSequence: string
  goiSequence: string
  threePrimeFlankingSequence: string
  useDegeneracyCodon: boolean
  uridineDepletion: boolean
  preciseMFEAlgorithm: boolean
  codonUsage: string
  taxonomyId: string
  codonUsageFrequencyThresholdPct: number
  optimizationCriterion: string
  numberOfSequences: number
  gcContentMin: number
  gcContentMax: number
  gcContentGlobal: number
  gcWindowSize: number
  entropyWindowSize: number
  avoidMotifs: string[]
  organism: string
}

export type FormParamsCombined = RequestData & FormData
