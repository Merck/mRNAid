import {ComponentType} from 'react'
import isNil from 'lodash/isNil'
import {compose, withHandlers, withStateHandlers} from 'recompose'
import {fetchJobStatus, pollWhilePending, submitRequest} from '../services/api'
import {JobDescription, JobStatus, ResponseData, JobStatusServer, RequestData} from '../types/Api'
import {FormParamsCombined} from '../types/FormData'
import {Workflow} from './workflow'

export type Job = {
  formData?: Partial<FormData>
  responseData?: ResponseData
  status?: JobStatusServer
  polling?: boolean
  error?: Record<string, unknown>
}

type WithJobState = {
  jobState: {
    [id: string]: Job
  }
}

type WithJobStateUpdaters = {
  setJob(id: string, job: Job): WithJobState
  updateJob(id: string, jobUpdate: Partial<Job>): WithJobState
}

const withJobState = withStateHandlers<WithJobState, WithJobStateUpdaters>(
  {jobState: {}},
  {
    setJob:
      ({jobState}) =>
      (id: string, job: Job) => ({
        jobState: {
          ...jobState,
          [id]: job,
        },
      }),
    updateJob:
      ({jobState}) =>
      (id: string, job: Job) => ({
        jobState: {
          ...jobState,
          [id]: {
            ...jobState[id],
            ...job,
          },
        },
      }),
  },
)

type WithJobGetter = {
  getJob(id: string | undefined): Job | undefined
}

const withJobGetter = withHandlers<WithJobState, WithJobGetter>({
  getJob:
    ({jobState}) =>
    (id: string) =>
      jobState[id],
})

export const hasDataLoaded = (job: Job | undefined) =>
  !isNil(job) && job.status?.JobStatus !== JobStatus.pending && (!isNil(job.responseData) || !isNil(job.error))
/* eslint-disable @typescript-eslint/no-explicit-any */
type WithJobHandlers = {
  submitRequest(
    workflow: Workflow,
    formDataToRequestData: (formData: FormParamsCombined) => RequestData,
    formData: any,
  ): Promise<JobDescription>
  requestJobResult(id: string, pollInterval: number): Promise<void>
}
/* eslint-enable @typescript-eslint/no-explicit-any */

const withJobHandlers = withHandlers<WithJobGetter & WithJobStateUpdaters, WithJobHandlers>({
  submitRequest:
    ({setJob}) =>
    (workflow: Workflow, formDataToRequestData: (formData: FormParamsCombined) => RequestData, formData) =>
      submitRequest(workflow.toString(), formDataToRequestData(formData)).then((jobDescription) => {
        setJob(jobDescription.id, {formData})
        return jobDescription
      }),
  requestJobResult:
    ({getJob, updateJob}) =>
    (id: string, pollInterval: number) => {
      const job = getJob(id)
      const isPolling = job ? job.polling : false

      if (isPolling || hasDataLoaded(job)) {
        return Promise.resolve()
      }

      updateJob(id, {polling: true})
      return fetchJobStatus(id)
        .then((status) => {
          updateJob(id, {status, polling: true})
          return status.state === JobStatus.pending ? pollWhilePending(id, pollInterval) : Promise.resolve(status)
        })
        .then((status) => {
          if (status.state === JobStatus.success) {
            updateJob(id, {
              status,
              responseData: status.data,
              polling: false,
            })
          }
        })
    },
})

export type WithJobStore = WithJobState & WithJobGetter & WithJobHandlers

export default <P>(component: ComponentType<P & WithJobStore>) =>
  compose<P & WithJobStore, P>(withJobState, withJobGetter, withJobHandlers)(component)
