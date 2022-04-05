import * as React from 'react'
import {formDataToRequest, dataToFormData} from 'src/services/api'
import WorkflowScene, {WorkflowSceneExternalProps} from 'src/components/WorkflowScene'
import {responseToResultData} from 'src/types/ResultData'
import {Workflow} from 'src/utils/workflow'
import {FormData} from 'src/types/FormData'
import routes from 'src/routes'
import Form from '../form'
import Result from '../result'

const demoData: Partial<FormData> = {
  fivePrimeFlankingSequence: '',
  goiSequence: '',
}

type PASOuterProps = WorkflowSceneExternalProps

const Index: React.FC<PASOuterProps> = ({submitRequest, requestJobResult, jobId, jobData, pollInterval}) => (
  <WorkflowScene
    jobId={jobId}
    jobData={jobData}
    defaultFormData={demoData}
    getRoute={routes.mrnaid}
    requestJobResult={(id: string) => requestJobResult(id, pollInterval)}
    responseToFormData={dataToFormData}
    responseToResultData={responseToResultData}
    submitRequest={(formData: FormData) => submitRequest(Workflow.newVal, formDataToRequest, formData)}
    InputForm={({disabled, formData, onSubmit}) => <Form disabled={disabled} data={formData} onSubmit={onSubmit} />}
    ResultsView={({resultData, formData}) => <Result resultData={resultData} jobId={jobId} formData={formData} />}
  />
)
export default Index
