import * as React from 'react'
import {Button} from 'antd'
import './styles.css'
/* eslint-disable @typescript-eslint/no-var-requires */
const Fornac = require('fornac')
const saveSvgAsPng = require('save-svg-as-png')

const imageOptions = {
  scale: 5,
  encoderOptions: 1,
  backgroundColor: 'white',
}

type visualizationProps = {
  structure: string
  name: number
  sequence: string
  title: string
}

class Visualization extends React.PureComponent<visualizationProps> {
  componentDidMount() {
    const {name} = this.props
    const container = new Fornac.FornaContainer(`#rna_ss_${name}`, {
      applyForce: true,
      allowPanningAndZooming: true,
      initialSize: [500, 475],
    })

    const options = {
      structure: this.props.structure,
      sequence: this.props.sequence,
    }

    container.addRNA(options.structure, options)
    container.setSize()
  }

  handleSVG = (name: number, title: string) => () => {
    const newId = `rna_ss_${name}`
    const imageName = title
    saveSvgAsPng.saveSvgAsPng(document.getElementById(newId)?.querySelector('#plotting-area'), imageName, imageOptions)
  }

  render() {
    const {name, title} = this.props

    return (
      <>
        <div id={`rna_ss_${name}`} />
        <Button
          className="no-print"
          type="primary"
          icon="download"
          onClick={this.handleSVG(name, title)}
          style={{float: 'right', margin: '10px'}}
        >
          Download Image
        </Button>
      </>
    )
  }
}

export default Visualization
