import * as React from 'react'
import {Card, Avatar} from 'antd'
import './styles.css'

type FormSectionTitleProps = {
  index: number
  title: string
}

const FormSectionTitle: React.FC<FormSectionTitleProps> = ({index, title}) => (
  <div className="FormSectionTitle">
    <Avatar>{index}</Avatar>
    <h1>{title}</h1>
  </div>
)

type FormSectionProps = {
  index: number
  title: string
  children: React.ReactNode
}

const FormSection: React.FC<FormSectionProps> = ({index, title, children}) => (
  <Card className="FormSection" title={<FormSectionTitle index={index} title={title} />}>
    {children}
  </Card>
)

export default FormSection
