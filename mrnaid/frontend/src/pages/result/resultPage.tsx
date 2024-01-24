import * as React from 'react'
import {Row, Col} from 'antd'
import LazyLoad from 'react-lazyload'
import Visualization from 'src/components/Visualization'
import PlotGraph from 'src/components/PlotGraph'
import {InputAndResultData} from 'src/types/Api'

type ResultPageProps = {
  result: InputAndResultData
  title: string
  openSection: boolean
}

class ResultPage extends React.PureComponent<ResultPageProps> {
  constructor(props: ResultPageProps) {
    super(props)
    this.state = {}
  }
  render() {
    const {result, title} = this.props

    return (
      <Row gutter={24} type="flex" justify="center">
        <Col md={12} sm={12} xs={24}>
          <div className="bg-grey">
            <h3>SECONDARY STRUCTURE</h3>
            <LazyLoad height={200} offset={100}>
              <Visualization
                structure={result.RNA_structure}
                sequence={result.RNASeq}
                name={result.seqID}
                title={title}
              />
            </LazyLoad>
          </div>
        </Col>
        <Col md={12} sm={12} xs={24}>
          <div className="bg-grey">
            <h3>DNA SEQUENCE</h3>
            <span className="break-word"> {result.DNASeq}</span>
          </div>
        </Col>
        <Col md={12} sm={12} xs={24}>
          <Row gutter={24} type="flex" className="bg-grey" style={{padding: '10px'}}>
            <h3>MFE DISTRIBUITION</h3>
            <PlotGraph value={result.RNA_structure} />
          </Row>
          <Row gutter={24}>
            <div className="bg-grey">
              <h3>Parameters</h3>
              <Row gutter={24} type="flex" justify="center">
                <Col md={12} sm={12} xs={24}>
                  A ratio: {result.A_ratio}
                </Col>
                <Col md={12} sm={12} xs={24}>
                  AT ratio: {result.AT_ratio}
                </Col>
              </Row>
              <Row gutter={24} type="flex" justify="center">
                <Col md={12} sm={12} xs={24}>
                  T/U ratio: {result.TU_ratio}
                </Col>
                <Col md={12} sm={12} xs={24}>
                  GC ratio: {result.GC_ratio}
                </Col>
              </Row>
              <Row gutter={24} type="flex" justify="center">
                <Col md={12} sm={12} xs={24}>
                  G ratio: {result.G_ratio}
                </Col>
                <Col md={12} sm={12} xs={24}>
                  MFE: {result.MFE}
                </Col>
              </Row>
              <Row gutter={24} type="flex">
                <Col md={12} sm={12} xs={24}>
                  5_MFE: {result.MFE_5}
                </Col>
                <Col md={12} sm={12} xs={24}>
                  C ratio: {result.C_ratio}
                </Col>
              </Row>
              <Row gutter={24} type="flex">
                <Col md={12} sm={12} xs={24}>
                  CAI: {result.CAI}
                </Col>
              </Row>
            </div>
          </Row>
        </Col>
        <Col md={12} sm={12} xs={24}>
          <div className="bg-grey">
            <h3>RNA SEQUENCE</h3>
            <span className="break-word"> {result.RNASeq}</span>
          </div>
        </Col>
      </Row>
    )
  }
}
export default ResultPage
