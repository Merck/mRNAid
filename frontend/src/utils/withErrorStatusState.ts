import * as React from 'react'
import {withState} from 'recompose'
import {JobResponse} from '../types/Api'

/* eslint-disable @typescript-eslint/no-explicit-any */
export type WithErrorStatusState = {
  error: any | undefined
  setError(value: JobResponse | string | undefined): any | undefined
}

export default <P>(component: React.ComponentType<P & WithErrorStatusState>) =>
  withState('error', 'setError', undefined)(component)
