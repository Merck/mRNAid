import * as React from 'react'
import {Button, Form, Input, message, Select, InputNumber, Popover, Icon, Radio, Switch, Row, Col} from 'antd'

import FileUploadInput from 'src/components/FileUploadInput'
import FormSection from 'src/components/FormSection'
import MinOptMaxInputs from 'src/components/MinOptMaxInputs'
import {FormData} from 'src/types/FormData'
import withForm, {WithFormOuterProps} from 'src/utils/withForm'
import {requiredField, geneField, motifsField, codingSequenceField} from 'src/utils/validators'
import {motifs} from 'src/config/motifs'
import './styles.css'

const exampleForm: Partial<FormData> = {
  fivePrimeFlankingSequence: 'AGAACUAAG',
  goiSequence:
    'CGCUUUGCCAAAGUUGGCCAGAAGCCCACGCAUUAAUUCUAGUGUGUGGGGAUGUGAAGAAUGUCCCGGAAAAGAUGUCCAUUGCGCUGGAGACCCUGGAUUGGCUACGCAUGAUCUCCUUCCCUAGACUUCGGUUCCUUCUAAGAGGUAUACUCCACAGCCCAGUUGGCCCAUAGAGACGCCUACUAACGAAACGGUCACUAUAGACCAAAAACUACGAUGUCCGCGAUGGAGAUACGCUGACUUACUACCCAUUCAUUCCGCGACAGUAGAGAAAAGACGACGGACUAUCAUUCUGAAGAGUCGUUCAAGUAGGAUUCCGGCCGACCUGUACCUAAAUGGCGUCCGUCCGGGUGUCCUUGUAACUGCCUAGAAACAGGAGCAGGACGGGAAGUCCUCGUAGUCCUAUCGUGGUUCUGGCCUCAAAUCCGCCCCGAAGAGUGAGCAACGACUCGUCGUACAUUUAGUCCACGGGAGAUCUGAACAAUCUCGGUGGUCUACCUUGCUUGUUUCGACACUUUCUUCCAUCCGAGCAAAUAUCGGGCUACCCACUUGAGGUAUGAGGGACCC',
  threePrimeFlankingSequence: 'UUGAGUGCAAUUUCCAAUGCAGCCUAC',
  uridineDepletion: true,
  cAI: true,
  preciseMFEAlgorithm: false,
  organism: 'h_sapiens',
  codonUsageFrequencyThresholdPct: 10,
  numberOfSequences: 3,
  gcContentMin: 30,
  gcContentMax: 70,
  gcWindowSize: 100,
  entropyWindowSize: 30,
  avoidMotifs: ['EcoRI'],
}

type FormOuterProps = {
  disabled: boolean
}
type FormInnerProps = FormOuterProps & WithFormOuterProps<FormData>
type MotifsOptions = React.ReactElement[]

type CompState = {
  motifsOption: MotifsOptions
  dinucleotides: boolean
  matchCodonPair: boolean
  cAIOptimization: boolean
}

class Index extends React.PureComponent<FormInnerProps, CompState> {
  constructor(props: FormInnerProps) {
    super(props)
    const motifsOptions = motifs.map((element: string) => <Select.Option key={element}>{element}</Select.Option>)
    this.state = {
      motifsOption: motifsOptions,
      dinucleotides: false,
      matchCodonPair: false,
      cAIOptimization: false,
    }
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

  handleExampleForm = (event: React.MouseEvent<HTMLInputElement>) => {
    event.preventDefault()
    this.props.form.setFieldsValue(exampleForm)
    this.setState({
      dinucleotides: exampleForm.dinucleotides || false,
      matchCodonPair: exampleForm.matchCodonPair || false,
      cAIOptimization: exampleForm.cAI || false,
    })
  }

  handleDinucleotides = (value: boolean) => {
    this.setState({dinucleotides: value})
  }

  handleMatchCodonPair = (value: boolean) => {
    this.setState({matchCodonPair: value})
  }

  handleCAIOptimization = (value: boolean) => {
    this.setState({cAIOptimization: value})
  }

  onFileUpload = (target: string) => (data: string) => {
    const {setFieldsValue, validateFields} = this.props.form
    setFieldsValue({[target]: data})
    validateFields([target], () => {
      // do nothing
    })
  }

  dinucleotides = (
    <div>
      <p>
        This optimization objective tries to adjust the usage of nucleotide pairs in the sequence in a way that the
        frequencies of these pairs are as close as possible to the frequencies in homo sapiens. This frequencies are
        taken from CoCoPUTs database. See the{' '}
        <a
          href="https://www.sciencedirect.com/science/article/pii/S0022283619302281"
          target="_blank"
          rel="noopener noreferrer"
        >
          link.
        </a>{' '}
        If no optimization strategy for codons or nucleotides is chosen, then the default one is used. The default one
        is the optimization of individual codon frequencies to the frequencies in the host (homo sapiens)
      </p>
    </div>
  )
  matchCodonPair = (
    <div>
      <p>
        This optimization objective tries to adjust the usage of codon pairs in the sequence in a way that the
        frequencies of these pairs are as close as possible to the frequencies in homo sapiens. This frequencies are
        taken from CoCoPUTs database. See the{' '}
        <a
          href="https://www.sciencedirect.com/science/article/pii/S0022283619302281"
          target="_blank"
          rel="noopener noreferrer"
        >
          link.
        </a>{' '}
        If no optimization strategy for codons or nucleotides is chosen, then the default one is used. The default one
        is the optimization of individual codon frequencies to the frequencies in the host (homo sapiens)
      </p>
    </div>
  )
  preciseMFEAlgorithm = (
    <div>
      <p>
        {' '}
        By default the optimization algorithm is based on the{' '}
        <a href="https://academic.oup.com/nar/article/41/6/e73/2902446/" target="_blank" rel="noopener noreferrer">
          stem-loop prediction
        </a>{' '}
        algorithm. You can change it to the more precise one used in{' '}
        <a href="https://www.tbi.univie.ac.at/RNA/" target="_blank" rel="noopener noreferrer">
          ViennaRNA package
        </a>
        . Be aware that this algorithm is much more computationally expensive, and the optimization can take quite a
        long time in this case.
      </p>
    </div>
  )
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
    const {form} = this.props
    const {getFieldDecorator, getFieldValue, resetFields} = form

    return (
      <Form layout="vertical" onSubmit={this.handlePreventSubmitForm}>
        <FormSection index={1} title="Sequence">
          <Form.Item label="Five Prime Flanking Sequence (5' UTR)">
            {getFieldDecorator('fivePrimeFlankingSequence', {
              rules: [requiredField, geneField],
            })(<Input.TextArea rows={2} />)}
          </Form.Item>

          <Form.Item label="Coding Sequence" className="GeneTextArea">
            <FileUploadInput onChange={this.onFileUpload('goiSequence')} />
            {getFieldDecorator('goiSequence', {
              rules: [requiredField, geneField, codingSequenceField],
            })(<Input.TextArea rows={8} />)}
          </Form.Item>

          <></>
          <Form.Item label="Three Prime Flanking Sequence (3' UTR)">
            {getFieldDecorator('threePrimeFlankingSequence', {
              rules: [requiredField, geneField],
            })(<Input.TextArea rows={2} />)}
          </Form.Item>
        </FormSection>

        <FormSection index={2} title="Optimization parameters">
          <Form.Item label="Codon Usage" required>
            {getFieldDecorator('organism', {initialValue: 'h_sapiens'})(
              <Radio.Group>
                <Radio.Button value="h_sapiens">Homo Sapiens</Radio.Button>
                <Radio.Button value="m_musculus">Mus musculus</Radio.Button>
              </Radio.Group>,
            )}
          </Form.Item>

          <Form.Item label="Codon Usage Frequency Threshold Percentage">
            {getFieldDecorator('codonUsageFrequencyThresholdPct', {
              initialValue: 10,
              rules: [requiredField],
            })(<InputNumber min={0} max={100} />)}
          </Form.Item>

          <Row gutter={10}>
            <Col>
              <Form.Item label="Uridine depletion">
                {getFieldDecorator('uridineDepletion', {
                  initialValue: false,
                  valuePropName: 'checked',
                })(<Switch />)}
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={10}>
            <Col>
              <Form.Item
                label={
                  <>
                    <span>Match dinucleotides usage </span>
                    <Popover content={this.dinucleotides}>
                      <Icon type="question-circle" className="question-circle" />
                    </Popover>
                  </>
                }
              >
                {getFieldDecorator('dinucleotides', {
                  initialValue: false,
                  valuePropName: 'checked',
                })(
                  <Switch
                    onChange={this.handleDinucleotides}
                    disabled={!!(this.state.matchCodonPair === true || this.state.cAIOptimization === true)}
                  />,
                )}
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={10}>
            <Col>
              <Form.Item
                label={
                  <>
                    <Popover content={this.matchCodonPair}>
                      <span>Match codon pair usuage </span>
                      <Icon type="question-circle" className="question-circle" />
                    </Popover>
                  </>
                }
              >
                {getFieldDecorator('matchCodonPair', {
                  initialValue: false,
                  valuePropName: 'checked',
                })(
                  <Switch
                    onChange={this.handleMatchCodonPair}
                    disabled={!!(this.state.dinucleotides === true || this.state.cAIOptimization === true)}
                  />,
                )}
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={10}>
            <Col>
              <Form.Item label="CAI optimization">
                {getFieldDecorator('cAI', {
                  initialValue: false,
                  valuePropName: 'checked',
                })(
                  <Switch
                    onChange={this.handleCAIOptimization}
                    disabled={!!(this.state.dinucleotides === true || this.state.matchCodonPair === true)}
                  />,
                )}
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={10}>
            <Col>
              <Form.Item
                label={
                  <>
                    <Popover content={this.preciseMFEAlgorithm}>
                      <span>Use more precise MFE estimation </span>

                      <Icon type="question-circle" className="question-circle" />
                    </Popover>
                  </>
                }
              >
                {getFieldDecorator('preciseMFEAlgorithm', {
                  initialValue: false,
                  valuePropName: 'checked',
                })(<Switch />)}
              </Form.Item>
            </Col>
          </Row>

          <Form.Item label="Avoid motifs">
            {getFieldDecorator('avoidMotifs', {
              rules: [motifsField],
            })(
              <Select mode="tags" placeholder="None">
                {this.state.motifsOption}
              </Select>,
            )}
          </Form.Item>

          <Form.Item
            label={
              <>
                <span>Global GC Content (%) </span>
                <Popover content={this.gcContent}>
                  <Icon type="question-circle" className="question-circle" />
                </Popover>
              </>
            }
            required
          >
            <MinOptMaxInputs
              getFieldDecorator={getFieldDecorator}
              getFieldValue={getFieldValue}
              resetFields={resetFields}
              fieldPrefix="gcContent"
              defaults={{min: 30, max: 70}}
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
            {getFieldDecorator('gcWindowSize', {
              initialValue: 100,
              rules: [requiredField],
            })(<InputNumber min={0} />)}
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
            {getFieldDecorator('entropyWindowSize', {
              initialValue: 30,
              rules: [requiredField],
            })(<InputNumber min={0} />)}
          </Form.Item>

          <Form.Item label="Number of Sequences">
            {getFieldDecorator('numberOfSequences', {
              initialValue: 10,
              rules: [requiredField],
            })(<InputNumber min={1} max={100} />)}
          </Form.Item>
        </FormSection>

        <div className="FormActions">
          <div>
            <Button type="default" htmlType="reset" icon="reload" onClick={this.handleResetForm}>
              Reset
            </Button>
            <Button type="default" htmlType="button" icon="form" onClick={this.handleExampleForm}>
              Example
            </Button>
          </div>
          <Button type="primary" htmlType="button" icon="save" id="submit_btn" onClick={this.handleSubmitForm}>
            Submit
          </Button>
        </div>
      </Form>
    )
  }
}

export default withForm<typeof Index, FormInnerProps>(Index)
