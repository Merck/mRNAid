import * as React from 'react'
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from 'recharts'
import './styles.css'

type PlotGraphProps = {
  value: string
}

type PlotGraphItem = {
  name: number
  mfe: number
}
type PLotGraphState = {
  refinedData: PlotGraphItem[]
}
class PlotGraph extends React.PureComponent<PlotGraphProps, PLotGraphState> {
  constructor(props: PlotGraphProps) {
    super(props)
    const structure = this.props.value
    const newArrayStruct = Array.from(structure)
    const countArray: number[] = []
    let counts = 0
    newArrayStruct.forEach((result) => {
      let ct = 0

      if (result === '(') {
        ct = 1
      } else if (result === ')') {
        ct = -1
      }
      const newCount = counts + ct
      countArray.push(newCount)
      counts = newCount
    })
    const objArray: PlotGraphItem[] = countArray.map((newVal, index) => ({
      name: index,
      mfe: newVal,
    }))
    this.state = {refinedData: objArray}
  }

  render() {
    return (
      <LineChart
        width={500}
        height={300}
        data={this.state.refinedData}
        margin={{top: 5, right: 30, left: 20, bottom: 5}}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="mfe" stroke="#8884d8" activeDot={{r: 8}} />
      </LineChart>
    )
  }
}

export default PlotGraph
