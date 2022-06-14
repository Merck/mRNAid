import {Col, Input, Row, message} from 'antd'
import {WrappedFormUtils} from 'antd/lib/form/Form'
import isEmpty from 'lodash/isEmpty'
import * as React from 'react'

type MinOptMaxInputsProps = Pick<WrappedFormUtils, 'getFieldDecorator' | 'getFieldValue' | 'resetFields'> & {
  fieldPrefix: string
  defaults: {
    min?: number
    max?: number
  }
  disabled: boolean
}
const MinOptMaxInputs = ({
  getFieldDecorator,
  getFieldValue,
  resetFields,
  fieldPrefix,
  defaults = {},
  disabled = false,
}: MinOptMaxInputsProps) => {
  const onBlurReset = (fieldName: string) => () => {
    if (getFieldValue('gcContentMin') >= getFieldValue('gcContentMax')) {
      message.error('gcContentMin should be smaller than gcContentMax ')
    }
    const value = getFieldValue(fieldName)
    if (isEmpty(value) || value < 0 || value > 100) {
      resetFields([fieldName])
    }
  }

  return (
    <Row className="MinOptMaxInputs" gutter={10}>
      <Col span={12}>
        {getFieldDecorator(`${fieldPrefix}Min`, {initialValue: defaults.min})(
          <Input type="number" addonBefore="MIN" onBlur={onBlurReset(`${fieldPrefix}Min`)} disabled={disabled} />,
        )}
      </Col>
      <Col span={12}>
        {getFieldDecorator(`${fieldPrefix}Max`, {initialValue: defaults.max})(
          <Input type="number" addonBefore="MAX" onBlur={onBlurReset(`${fieldPrefix}Max`)} disabled={disabled} />,
        )}
      </Col>
    </Row>
  )
}

export default MinOptMaxInputs
