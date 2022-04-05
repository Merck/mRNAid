import {Avatar, Col, Collapse, Row} from 'antd'
import isNil from 'lodash/isNil'
import * as React from 'react'
import './styles.css'

const {Panel} = Collapse

type FormSectionProps = {
  index?: number
  title?: string

  children: React.ReactNode
  collapse?: boolean
  open?: boolean
}

type FormSectionTitleProps = {
  index?: number
  title?: string
  children?: React.ReactNode
}

const FormSectionTitle: React.FC<FormSectionTitleProps> = ({index, title, children}) => (
  <Row className="FormSection">
    <Col span={1} className="FormSection-number--col">
      {!isNil(index) && <Avatar>{index}</Avatar>}
    </Col>
    <Col span={22}>
      {!isNil(title) && <h1>{title}</h1>}
      {children}
    </Col>
  </Row>
)

const FormSection: React.FC<FormSectionProps> = ({index, title, children, collapse = true, open = true}) => (
  <>
    {collapse && (
      <Collapse defaultActiveKey={open ? ['1'] : undefined}>
        <Panel header={<FormSectionTitle index={index} title={title} />} key="1" forceRender>
          {children}
        </Panel>
      </Collapse>
    )}
    {!collapse && (
      <div className="FormSectionNotCollapsing">
        <FormSectionTitle index={index} title={title}>
          {' '}
          {children}{' '}
        </FormSectionTitle>
      </div>
    )}
  </>
)

export default FormSection
