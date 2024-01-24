import {Alert, Col, Row, message} from 'antd'
import isNil from 'lodash/isNil'
import * as React from 'react'
import {compose} from 'recompose'
// eslint-disable-next-line import/named
import {RouteComponentProps, withRouter} from 'react-router-dom'

import withCurrentStepState, {WithCurrentStepState, WorkflowStep} from 'src/utils/withCurrentStepState'
import withErrorStatusState, {WithErrorStatusState} from 'src/utils/withErrorStatusState'
import {hasDataLoaded, Job, WithJobStore} from 'src/utils/withJobStore'
import {JobStatus, JobDescription, ResponseData} from 'src/types/Api'
import {getInputData} from 'src/services/api'
import WorkflowSteps from '../WorkflowSteps'
import './styles.css'

export type WorkflowSceneExternalProps = {
  jobId?: string
  jobData?: Job
  pollInterval: number
} & Pick<WithJobStore, 'submitRequest' | 'requestJobResult'>

type WorkflowSceneOuterProps<FormData, ResultData> = Pick<WorkflowSceneExternalProps, 'jobId' | 'jobData'> & {
  defaultFormData: Partial<FormData>
  getRoute(jobId?: string): string

  requestJobResult(id: string): Promise<void>

  responseToFormData(data: any): FormData
  responseToResultData(data: ResponseData): ResultData

  submitRequest(formData: FormData): Promise<JobDescription>
  InputForm(props: {
    disabled: boolean
    formData: Partial<FormData>
    onSubmit(formData: Partial<FormData>): void
  }): JSX.Element
  ResultsView(props: {resultData: ResultData; formData: Partial<FormData>}): JSX.Element
}

type WorkflowSceneInnerProps<FormData, ResultData> = WorkflowSceneOuterProps<FormData, ResultData> &
  RouteComponentProps<Record<string, string>> &
  WithCurrentStepState &
  WithErrorStatusState

class WorkflowScene<FormData, ResultData> extends React.PureComponent<WorkflowSceneInnerProps<FormData, ResultData>> {
  componentDidMount() {
    const {jobId, jobData} = this.props
    this.setCurrentStepOnProps()

    if (!isNil(jobId) && !hasDataLoaded(jobData)) {
      this.requestJobResultWithErrorHandler(jobId)
    }
  }

  componentDidUpdate(prevProps: WorkflowSceneInnerProps<FormData, ResultData>) {
    const {jobId, jobData} = this.props
    this.setCurrentStepOnProps()
    if (prevProps.jobId !== jobId && !isNil(jobId) && !hasDataLoaded(jobData)) {
      this.requestJobResultWithErrorHandler(jobId)
    }
  }

  setCurrentStepOnProps = () => {
    const {setCurrentStep, currentStep, jobId, jobData} = this.props
    if (isNil(currentStep)) {
      if (!isNil(jobId)) {
        if (jobId && jobData?.polling === true) {
          setCurrentStep(WorkflowStep.InProgress)
        } else {
          setCurrentStep(WorkflowStep.Results)
        }
      } else {
        setCurrentStep(WorkflowStep.InputParameters)
      }
    }
  }

  requestJobResultWithErrorHandler = (jobId: string) => {
    const {requestJobResult, setError} = this.props

    return requestJobResult(jobId).catch((err) => {
      setError('Error occured while requesting job result. Please contact support.')
      message.error(err)
    })
  }

  handleOnSubmit = (formData: FormData) => {
    const {setError, submitRequest, history, getRoute} = this.props
    window.scrollTo(0, 0)
    return submitRequest(formData)
      .then((jobDescription) => (
        <>{jobDescription.id ? history.push(getRoute(jobDescription.id)) : message.error(jobDescription.jobResponse)}</>
      ))

      .catch((err) => {
        setError(err)
        message.error(err)
      })
  }

  getFormData = () => {
    const {responseToFormData, jobData} = this.props

    const formData = jobData ? jobData.formData : undefined
    const responseData = jobData ? jobData.responseData : undefined
    if (formData) {
      return formData
    }
    if (responseData) {
      const inputData = getInputData(responseData.input_parameters)
      return responseToFormData(inputData)
    }

    return undefined
  }

  getResultData = () => {
    const {responseToResultData, jobData} = this.props
    const responseData = jobData ? jobData.responseData : undefined
    return responseData ? responseToResultData(responseData) : undefined
  }

  render() {
    const {defaultFormData, jobId, jobData, currentStep, setCurrentStep, error, InputForm, ResultsView} = this.props
    const jobStatus = jobData ? jobData.status?.JobStatus : undefined
    const jobError = jobData ? jobData.error : undefined
    const formData = jobStatus !== JobStatus.failure ? this.getFormData() : undefined

    const resultData = this.getResultData()
    const hasId = !isNil(jobId)
    const loading = hasId && !hasDataLoaded(jobData)
    const finished = hasId && !isNil(resultData)
    const failure = error || jobError
    const displayedFormData = jobData ? (formData as Partial<FormData>) : defaultFormData

    const makeOnWorkflowStepsClick = (step: WorkflowStep) => (hasId ? () => setCurrentStep(step) : undefined)

    return (
      <>
        <WorkflowSteps
          loading={loading}
          finished={finished}
          currentStep={currentStep}
          failure={failure}
          makeOnClick={makeOnWorkflowStepsClick}
        />
        {error && (
          <Alert
            type="error"
            showIcon
            message="Submit Error"
            description={`Error occured while submiting job: \n${error}`}
          />
        )}

        {jobError && (
          <Alert
            type="error"
            showIcon
            message="Job Error"
            description={`Error occured while processing job: \n${jobError}`}
          />
        )}
        {currentStep === WorkflowStep.InputParameters && displayedFormData && (
          <Row>
            <Col xs={{span: 18, offset: 3}} lg={{span: 16, offset: 4}} xxl={{span: 12, offset: 6}}>
              <InputForm onSubmit={this.handleOnSubmit} disabled={hasId} formData={displayedFormData} />
            </Col>
          </Row>
        )}

        {currentStep === WorkflowStep.InProgress && (
          <div className="InProgress">Computation is in progress. Please wait.</div>
        )}

        {currentStep === WorkflowStep.Results && resultData && (
          <ResultsView resultData={resultData} formData={displayedFormData} />
        )}
      </>
    )
  }
}
export default <FormData, ResultData>(props: WorkflowSceneOuterProps<FormData, ResultData>) => {
  const EnhancedWorkflowScene = compose<
    WorkflowSceneInnerProps<FormData, ResultData>,
    WorkflowSceneOuterProps<FormData, ResultData>
  >(
    withRouter,
    withErrorStatusState,
    withCurrentStepState,
  )(WorkflowScene)

  return <EnhancedWorkflowScene {...props} />
}
