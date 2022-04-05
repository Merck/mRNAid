import * as React from 'react'
import {Form, InputNumber, Radio, Row, Col, Switch, Icon, Popover} from 'antd'
import {WrappedFormUtils} from 'antd/lib/form/Form'
import FormSection from '../FormSection'
import './styles.css'

type codonUsageProps = {
  index: number
  form: WrappedFormUtils
}

type customProps = {
  dinucleotides: boolean
  matchCodonPair: boolean
  cAIOptimization: boolean
}

export default class CodonUsage extends React.Component<codonUsageProps, customProps> {
  constructor(props: codonUsageProps) {
    super(props)
    this.state = {
      dinucleotides: false,
      matchCodonPair: false,
      cAIOptimization: false,
    }
  }

  shouldComponentUpdate() {
    return true
  }

  codonUsageDataLoad: Array<{name: string}> = []

  handleDinucleotides = (event: unknown) => {
    if (event) {
      this.setState({dinucleotides: true})
    } else {
      this.setState({dinucleotides: false})
    }
  }

  handleMatchCodonPair = (event: unknown) => {
    if (event) {
      this.setState({matchCodonPair: true})
    } else {
      this.setState({matchCodonPair: false})
    }
  }

  handleCAIOptimization = (event: unknown) => {
    if (event) {
      this.setState({cAIOptimization: true})
    } else {
      this.setState({cAIOptimization: false})
    }
  }

  content = (
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

  render() {
    const {getFieldDecorator} = this.props.form

    return (
      <FormSection index={this.props.index} title="Codon Usage">
        <Form.Item label="Codon Usage">
          {getFieldDecorator('organism', {initialValue: 'h_sapiens'})(
            <Radio.Group>
              <Radio.Button value="h_sapiens">Homo Sapiens</Radio.Button>
              <Radio.Button value="m_musculus">Mus musculus</Radio.Button>
            </Radio.Group>,
          )}
        </Form.Item>
        <></>

        <Form.Item label="Codon Usage Frequency Threshold Percentage">
          {getFieldDecorator('codonUsageFrequencyThresholdPct', {
            initialValue: 10,
            rules: [
              {
                required: true,
                message: 'Frequency Threshold Percentage is required',
              },
            ],
          })(<InputNumber min={0} max={100} type="number" />)}
        </Form.Item>
        <></>
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
        <></>

        <Row gutter={10}>
          <Col>
            <Form.Item
              label={
                <>
                  <span>Match dinucleotides usage </span>
                  <Popover content={this.content}>
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
        <></>
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
      </FormSection>
    )
  }
}
