import Axios from 'axios'
import {JobDescription, JobResponse, JobStatus, JobStatusServer, InputParameters} from '../types/Api'
import {FormData, FormParamsCombined} from '../types/FormData'

const API_PREFIX = process.env.REACT_APP_API_URL
const formatString = (text: string) => {
  if (text) {
    const formattedText = text.trim().toUpperCase()
    if (formattedText.length > 0) {
      return formattedText
    }
  }
  return null
}

export const formDataToRequest = (formData: FormData) => ({
  config: {
    avoided_motifs: formData.avoidMotifs || [],
    codon_usage_frequency_threshold: Number((formData.codonUsageFrequencyThresholdPct || 0) / 100),
    max_GC_content: Number((formData.gcContentMax || 0) / 100),
    min_GC_content: Number((formData.gcContentMin || 0) / 100),
    GC_window_size: Number(formData.gcWindowSize),
    organism: String(formData.organism),
    number_of_sequences: Number(formData.numberOfSequences),
    entropy_window: Number(formData.entropyWindowSize),
  },
  uridine_depletion: Boolean(formData.uridineDepletion),
  match_codon_pair: Boolean(formData.matchCodonPair),
  precise_MFE_algorithm: Boolean(formData.preciseMFEAlgorithm),
  dinucleotides: Boolean(formData.dinucleotides),
  file_name: formData.fileName || '',
  CAI: Boolean(formData.cAI),

  sequences: {
    five_end_flanking_sequence: formatString(formData.fivePrimeFlankingSequence),
    gene_of_interest: formatString(formData.goiSequence),
    three_end_flanking_sequence: formatString(formData.threePrimeFlankingSequence),
  },
})

export const getInputData = (inputData: InputParameters) => ({
  inputSequenceType: inputData.input_mRNA,
  fivePrimeFlankingSequence: inputData.five_end,
  goiSequence: inputData.input_mRNA,
  threePrimeFlankingSequence: inputData.three_end,
  uridineDepletion: inputData.uridine_depletion,
  preciseMFEAlgorithm: inputData.precise_MFE_algorithm,
  dinucleotides: inputData.dinucleotides,
  matchCodonPair: inputData.codon_pair,
  codonUsage: inputData.usage_threshold,
  taxonomyId: inputData.GC_window_size,
  codonUsageFrequencyThresholdPct: inputData.usage_threshold,
  numberOfSequences: inputData.number_of_sequences,
  gcContentMin: inputData.min_GC_content,
  gcContentMax: inputData.max_GC_content,
  gcWindowSize: inputData.GC_window_size,
  entropyWindowSize: inputData.entropy_window,
  fileName: inputData.filename,
  avoidMotifs: inputData.avoid_motifs,
})

export const dataToFormData = (formData: FormData) => {
  const requestData = formData

  return {
    inputSequenceType: requestData.inputSequenceType,
    fivePrimeFlankingSequence: requestData.fivePrimeFlankingSequence,
    goiSequence: requestData.goiSequence,
    threePrimeFlankingSequence: requestData.threePrimeFlankingSequence,
    useDegeneracyCodon: requestData.useDegeneracyCodon,
    uridineDepletion: requestData.uridineDepletion,
    cAI: requestData.cAI,
    preciseMFEAlgorithm: requestData.preciseMFEAlgorithm,
    dinucleotides: requestData.dinucleotides,
    matchCodonPair: requestData.matchCodonPair,
    codonUsage: requestData.codonUsage,
    taxonomyId: requestData.taxonomyId,
    codonUsageFrequencyThresholdPct: requestData.codonUsageFrequencyThresholdPct,
    numberOfSequences: requestData.numberOfSequences,
    gcContentMin: requestData.gcContentMin,
    gcContentMax: requestData.gcContentMax,
    gcContentGlobal: requestData.gcContentGlobal,
    gcWindowSize: requestData.gcWindowSize,
    entropyWindowSize: requestData.entropyWindowSize,
    fileName: requestData.fileName,
    avoidMotifs: requestData.avoidMotifs,
  }
}

const dataToJobResponse = (data: object): JobResponse => data as JobResponse

export const fetchJobResultData = (jobId: string): Promise<string> =>
  Axios.get(`${API_PREFIX}/status/${jobId}`).then((response) => response.data)

export const fetchJobStatus = (jobId: string): Promise<JobStatusServer> =>
  Axios.get(`${API_PREFIX}/status/${jobId}`).then((response) => response.data as JobStatusServer)

export const submitJob = (endpoint: string, requestData: Partial<FormParamsCombined>): Promise<JobResponse> =>
  Axios.post(`${API_PREFIX}/optimize`, JSON.stringify(requestData), {
    headers: {'Content-Type': 'application/json'},
  }).then((response) => dataToJobResponse(response.data))

const delay = (timeout: number) => new Promise<void>((resolve) => setTimeout(() => resolve(), timeout))

export const pollWhilePending = (jobId: string, pollInterval: number): Promise<JobStatusServer> =>
  fetchJobStatus(jobId).then((jobStatus: JobStatusServer) => {
    if (jobStatus.state === JobStatus.pending) {
      return delay(pollInterval).then(() => pollWhilePending(jobId, pollInterval))
    }
    return jobStatus
  })

const getJobId = (job: JobResponse): string => job.task_id

export const submitRequest = (endpoint: string, requestData: Partial<FormParamsCombined>): Promise<JobDescription> =>
  submitJob(endpoint, requestData).then((jobResponse) => ({
    id: getJobId(jobResponse),
    jobResponse,
  }))
