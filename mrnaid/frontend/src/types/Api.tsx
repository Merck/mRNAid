/* eslint-disable camelcase */
export type JobResponse = {
  task_id: string
}

export enum JobStatus {
  pending = 'PENDING',
  success = 'SUCCESS',
  failure = 'FAILURE',
}
export type JobStatusServer = {
  state: string
  JobStatus: JobStatus
  data: ResponseData
}

export type JobDescription = {
  id: string
  jobResponse: JobResponse
}

export type RequestConfig = {
  avoided_motifs: string[]
  codon_usage_frequency_threshold: number
  max_GC_content: number
  min_GC_content: number
  GC_window_size: number
  organism: string
  number_of_sequences: number
  entropy_window: number
}

export type InputAndResultData = {
  seqID: number
  RNASeq: string
  DNASeq: string
  A_ratio: string
  TU_ratio: string
  G_ratio: string
  C_ratio: string
  AT_ratio: string
  GC_ratio: string
  MFE: string
  MFE_5: string
  score: string
  RNA_structure: string
  CAI: string
}

export type InputParameters = {
  filename: string
  five_end: string
  three_end: string
  input_mRNA: string
  organism: string
  optimization_criterion: string
  usage_threshold: string
  uridine_depletion: string
  avoid_motifs: string
  min_GC_content: string
  max_GC_content: string
  GC_window_size: string
  entropy_window: string
  number_of_sequences: number
  precise_MFE_algorithm: boolean
}

export type RequestData = {
  sequences: {
    five_end_flanking_sequence: string
    gene_of_interest: string
    three_end_flanking_sequence: string
  }
  uridine_depletion: boolean
  precise_MFE_algorithm: boolean
  file_name: string
  config: RequestConfig
}

export type ResponseData = {
  input: InputAndResultData
  optimized: InputAndResultData[]
  input_parameters: InputParameters
}
