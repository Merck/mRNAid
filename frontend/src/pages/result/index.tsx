import * as React from 'react'
import {PDFDownloadLink} from '@react-pdf/renderer'
import {Button, Tabs, Col, Row} from 'antd'
import {ResultData} from 'src/types/ResultData'
import {FormData} from 'src/types/FormData'
import SaveFile from 'src/components/SaveFile'
import SavePdf from 'src/components/SavePdf'
import ResultPage from './resultPage'
import './styles.css'

const {TabPane} = Tabs

type ResultOuterProps = {
  jobId?: string
  resultData: ResultData
  formData: Partial<FormData>
}

class Result extends React.PureComponent<ResultOuterProps> {
  constructor(props: ResultOuterProps) {
    super(props)
    this.state = {}
  }
  render() {
    const {results, input, inputParameters} = this.props.resultData
    const {formData} = this.props

    return (
      <div className="ant-row">
        {/* <Form> */}
        <div key="unique">
          <Row gutter={24} type="flex" justify="center">
            <Col md={2} sm={4} xs={24} className="p-12">
              <div className="border-all bg-grey">
                <h3>Result</h3>
              </div>
            </Col>
            <Col md={22} sm={20} xs={24} className="p-12">
              <div className="border-all bg-grey">
                <h3> Details</h3>
              </div>
            </Col>
          </Row>
          <Tabs defaultActiveKey="Input" tabPosition="left">
            <TabPane tab="Input" key="Input">
              <ResultPage result={input} title={'Input'} openSection={false} />
            </TabPane>

            {results.map((value, index) => (
              <TabPane tab={`Output ${index + 1}`} key={`key ${Math.random().toString(36).substring(2, 7)}`}>
                <ResultPage
                  result={value}
                  title={`Output ${index + 1}`}
                  openSection={false}
                  key={`key ${Math.random().toString(36).substring(2, 7)}`}
                />
              </TabPane>
            ))}
          </Tabs>
        </div>
        <SaveFile result={results} input={input} type="pas" fileName={inputParameters.filename} formData={formData} />
        <PDFDownloadLink
          document={<SavePdf result={results} inputParameters={inputParameters} />}
          fileName={inputParameters.filename ? inputParameters.filename : 'mRNAid'}
          style={{
            textDecoration: 'none',
            padding: '10px',
            color: '#4a4a4a',
            backgroundColor: '#f2f2f2',
          }}
        >
          {({loading}) => (
            <>
              {loading ? (
                'Loading document'
              ) : (
                <Button type="primary" icon="download" style={{float: 'right', margin: '10px'}}>
                  Download PDF
                </Button>
              )}
            </>
          )}
        </PDFDownloadLink>
      </div>
    )
  }
}
export default Result
