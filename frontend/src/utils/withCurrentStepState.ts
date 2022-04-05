import * as React from 'react'
import {withState} from 'recompose'

export enum WorkflowStep {
  InputParameters,
  InProgress,
  Results,
}

export type WithCurrentStepState = {
  currentStep: WorkflowStep | undefined
  setCurrentStep(value: WorkflowStep | undefined): WorkflowStep | undefined
}

export default <P>(component: React.ComponentType<P & WithCurrentStepState>) =>
  withState<P, WorkflowStep | undefined, 'currentStep', 'setCurrentStep'>(
    'currentStep',
    'setCurrentStep',
    undefined,
  )(component)
