import {Icon, Steps} from 'antd'
import * as React from 'react'
import {WorkflowStep} from 'src/utils/withCurrentStepState'

type WorkflowStepsProps = {
  loading: boolean
  finished: boolean
  failure: boolean
  currentStep: WorkflowStep | undefined
  makeOnClick(step: WorkflowStep): (() => void) | undefined
}

const WorkflowSteps: React.FC<WorkflowStepsProps> = ({loading, finished, failure, currentStep, makeOnClick}) => {
  const getIcon = (step: WorkflowStep) => {
    if (finished) {
      return <Icon type="check" />
    } else if (currentStep === WorkflowStep.Results) {
      return <Icon type="check" />
    }
    return currentStep === step && loading && <Icon type="loading" />
  }

  const stepStyle = {
    marginBottom: 20,
    marginTop: 10,
    paddingLeft: 10,
    paddingRight: 10,
  }

  const clickableStyle = {cursor: 'pointer'}

  const onInputClick = makeOnClick(WorkflowStep.InputParameters)
  const onResultsClick = makeOnClick(WorkflowStep.Results)

  return (
    <Steps current={currentStep} status={failure ? 'error' : undefined} style={stepStyle}>
      <Steps.Step
        title="Input Parameters"
        icon={getIcon(WorkflowStep.InputParameters)}
        style={onInputClick && clickableStyle}
        onClick={currentStep !== WorkflowStep.InProgress ? onInputClick : undefined}
      />
      <Steps.Step title="In Progress" icon={getIcon(WorkflowStep.InProgress)} />
      <Steps.Step
        title="Results"
        icon={getIcon(WorkflowStep.Results)}
        style={onResultsClick && clickableStyle}
        onClick={currentStep !== WorkflowStep.InProgress ? onResultsClick : undefined}
      />
    </Steps>
  )
}

export default WorkflowSteps
