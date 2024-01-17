import {compose} from 'recompose'
// eslint-disable-next-line import/named
import {withRouter, RouteComponentProps} from 'react-router-dom'

import withErrorStatusState, {WithErrorStatusState} from 'src/utils/withErrorStatusState'
import withCurrentStepState, {WithCurrentStepState} from 'src/utils/withCurrentStepState'
import {WithJobStore, Job} from 'src/utils/withJobStore'
import {JobDescription, ResponseData} from 'src/types/Api'
import {ResultData} from 'src/types/ResultData'
import {FormData} from 'src/types/FormData'
import WorkflowScene from './WorkflowScene'

type WorkflowSceneInnerProps<FormData, ResultData> = WorkflowSceneOuterProps<FormData, ResultData> &
  RouteComponentProps<Record<string, string>> &
  WithCurrentStepState &
  WithErrorStatusState

export type WorkflowSceneExternalProps = {
  jobId?: string
  jobData?: Job
  pollInterval: number
} & Pick<WithJobStore, 'submitRequest' | 'requestJobResult'>

type WorkflowSceneOuterProps<FormData, ResultData> = Pick<WorkflowSceneExternalProps, 'jobId' | 'jobData'> & {
  defaultFormData: Partial<FormData>
  getRoute(jobId?: string): string

  requestJobResult(id: string): Promise<void>

  responseToFormData(data: FormData): Partial<FormData>
  responseToResultData(data: ResponseData): ResultData

  submitRequest(formData: FormData): Promise<JobDescription>
  InputForm(props: {
    disabled: boolean
    formData: Partial<FormData>
    onSubmit(formData: Partial<FormData>): void
  }): JSX.Element
  ResultsView(props: {resultData: ResultData; formData: Partial<FormData>}): JSX.Element
}

export default compose<WorkflowSceneInnerProps<FormData, ResultData>, WorkflowSceneOuterProps<FormData, ResultData>>(
  withRouter,
  withCurrentStepState,
  withErrorStatusState,
)(WorkflowScene)
