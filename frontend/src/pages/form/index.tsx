import * as React from 'react'
import {Button, Form, Input, message, Select, InputNumber, Popover, Icon} from 'antd'

import FileUploadInput from 'src/components/FileUploadInput'
import FormSection from 'src/components/FormSection'
import MinOptMaxInputs from 'src/components/MinOptMaxInputs'
import CodonUsage from 'src/components/CodonUsage'
import {FormData} from 'src/types/FormData'
import withForm, {WithFormOuterProps} from 'src/utils/withForm'
import {validateAvoidMotifs} from 'src/utils/validateAvoidMotifs'
import {motifs} from 'src/config/motifs'
import {geneValidationRule} from 'src/config/geneValidationRule'
import './styles.css'

type FormOuterProps = {
  disabled: boolean
}

type FormInnerProps = FormOuterProps & WithFormOuterProps<FormData>
const {Option} = Select
type motifsOptions = React.ReactElement[]

class Index extends React.PureComponent<FormInnerProps, {motifsOption: motifsOptions}> {
  constructor(props: FormInnerProps) {
    super(props)
    const motifsOptions = motifs.map((element: string) => <Option key={element}>{element}</Option>)
    this.state = {motifsOption: motifsOptions}
  }

  handleSubmitForm = (event: React.MouseEvent<HTMLInputElement>) => {
    event.preventDefault()
    const {form, onSubmit} = this.props

    form.validateFields((error: Array<string>, values: FormData) => {
      if (!error) {
        onSubmit(values)
      } else {
        message.error('Validation failed')
      }
    })
  }

  handlePreventSubmitForm = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
  }

  handleResetForm = (event: React.MouseEvent<HTMLInputElement>) => {
    event.preventDefault()
    this.props.form.resetFields()
  }

  onFileUpload = (target: string) => (data: string) => {
    const {setFieldsValue, validateFields} = this.props.form
    setFieldsValue({[target]: data})
    validateFields([target], () => {
      // do nothing
    })
  }
  gcContent = (
    <div>
      <p> This constraint keeps the GC content across the whole sequence in a specified region of values </p>
    </div>
  )
  gcWindowSize = (
    <div>
      This objective tries to keep the GC content as close as possible to the region specified in Global GC content but
      inside the sliding window of the specified size.
    </div>
  )

  entrophyWindowSize = (
    <>
      This parameter is the size of the window in which the minimal free energy (MFE) of the sequence is maximized. This
      window starts at the end of 5’ UTR. Maximization of the MFE in this region allows to keep the structure of the 5’
      end of the sequence as open as possible given other constraints
    </>
  )

  render() {
    const {form, disabled} = this.props
    const {getFieldDecorator, getFieldValue, resetFields} = form

    return (
      <Form layout="vertical" onSubmit={this.handlePreventSubmitForm}>
        <FormSection index={1} title="Sequence">
          <></>
          <Form.Item label="Five Prime Flanking Sequence (5' UTR)" hasFeedback>
            {getFieldDecorator('fivePrimeFlankingSequence', {
              rules: [
                geneValidationRule,
                {
                  required: true,
                  message: 'Five Prime Flanking Sequence is required',
                },
              ],
            })(<Input.TextArea rows={2} />)}
          </Form.Item>
          <></>

          <Form.Item label="Coding Sequence" className="GeneTextArea">
            <FileUploadInput onChange={this.onFileUpload('goiSequence')} />
            {getFieldDecorator('goiSequence', {
              rules: [
                geneValidationRule,
                {
                  required: true,
                  message: 'input RNA Sequence is required',
                },
              ],
            })(<Input.TextArea rows={8} />)}
          </Form.Item>

          <></>
          <Form.Item label="Three Prime Flanking Sequence (3' UTR)" hasFeedback>
            {getFieldDecorator('threePrimeFlankingSequence', {
              rules: [
                geneValidationRule,
                {
                  required: true,
                  message: 'Three Prime Flanking Sequence is required',
                },
              ],
            })(<Input.TextArea rows={2} />)}
          </Form.Item>

          <Form.Item label="Number of Sequences" hasFeedback>
            {getFieldDecorator('numberOfSequences', {
              initialValue: 10,
              rules: [
                {
                  required: true,
                  message: 'Frequency Threshold Percentage is required',
                },
              ],
            })(<InputNumber min={0} max={100} type="number" />)}
          </Form.Item>
        </FormSection>

        <CodonUsage index={2} form={form} />
        <FormSection index={3} title="Avoid Motifs" open={false}>
          <></>
          <Form.Item>
            {getFieldDecorator('avoidMotifs', {
              rules: [{validator: validateAvoidMotifs}],
            })(
              <Select mode="tags" placeholder="None">
                {this.state.motifsOption}
              </Select>,
            )}
          </Form.Item>
        </FormSection>

        <FormSection index={4} title="Parameters" open={false}>
          <></>
          <div className="workflow-cards">
            <Form.Item
              label={
                <>
                  <span>Global GC Content (%) </span>
                  <Popover content={this.gcContent}>
                    <Icon type="question-circle" className="question-circle" />
                  </Popover>
                </>
              }
            >
              <MinOptMaxInputs
                getFieldDecorator={getFieldDecorator}
                getFieldValue={getFieldValue}
                resetFields={resetFields}
                fieldPrefix="gcContent"
                defaults={{min: 30, opt: 40, max: 70}}
                disabled={false}
              />
            </Form.Item>

            <Form.Item
              label={
                <>
                  <span>Window size for local GC content </span>
                  <Popover content={this.gcWindowSize}>
                    <Icon type="question-circle" className="question-circle" />
                  </Popover>
                </>
              }
            >
              {getFieldDecorator('gcWindowSize')(<Input type="number" />)}
            </Form.Item>

            <Form.Item
              label={
                <>
                  <span>Entropy Window Size </span>
                  <Popover content={this.entrophyWindowSize}>
                    <Icon type="question-circle" className="question-circle" />
                  </Popover>
                </>
              }
            >
              {getFieldDecorator('entropyWindowSize')(<Input type="number" />)}
            </Form.Item>

            <Form.Item label="Output file name" hasFeedback>
              {getFieldDecorator('fileName')(<Input />)}
            </Form.Item>
          </div>
        </FormSection>

        <FormSection collapse={false}>
          <Form.Item className="DataInputForm-submitRow">
            <Button.Group>
              <Button type="primary" htmlType="button" icon="save" id="submit_btn" onClick={this.handleSubmitForm}>
                Submit
              </Button>
              <Button type="default" htmlType="reset" icon="reload" disabled={disabled} onClick={this.handleResetForm}>
                Reset
              </Button>
            </Button.Group>
          </Form.Item>
        </FormSection>
      </Form>
    )
  }
}

export default withForm<typeof Index, FormInnerProps>(Index)
