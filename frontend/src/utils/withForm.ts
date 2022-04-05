import {ComponentType} from 'react'
import {Form} from 'antd'
import {WrappedFormUtils} from 'antd/lib/form/Form'
import {Matching, GetProps} from 'antd/lib/form/interface'

export type WithFormOuterProps<D> = {
  data: Partial<D>
  onSubmit(data: D): void
  form: WrappedFormUtils
}

function withForm<C extends ComponentType<Matching<T, GetProps<C>>>, T extends WithFormOuterProps<any>>(component: C) {
  return Form.create<T>({
    mapPropsToFields({data}) {
      if (data) {
        return Object.keys(data).reduce(
          (acc, key) => ({
            ...acc,
            [key]: Form.createFormField({value: data[key]}),
          }),
          {},
        )
      }
      return undefined
    },
  })(component)
}

export default withForm
