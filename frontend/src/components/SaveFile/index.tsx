import {Button, message} from 'antd'
import * as React from 'react'
import * as Excel from 'exceljs'
import * as FileSaver from 'file-saver'

import {InputAndResultData} from 'src/types/Api'
import {FormData} from 'src/types/FormData'

type AnyFormData = Partial<FormData>
type SaveFileProps = {
  result: InputAndResultData[]
  input: InputAndResultData
  fileName: string
  formData: AnyFormData
  type: string
}
type Table = {
  [key: string]: Array<string>
}
type DataKey = keyof InputAndResultData

const tableHeaders = {
  pas: [
    'Seq Id',
    'DNA Sequence',
    'A Ratio',
    'T/U Ratio',
    'G Ratio',
    'C Ratio',
    'AT Ratio',
    'GC Ratio',
    'MFE',
    '5_MFE',
    'Score',
    'CAI',
  ],
}

const createPASTable = (result: InputAndResultData[], inputData: InputAndResultData, fileName: string): Table => {
  const table: Record<string, any> = {}
  const type = 'pas'
  // Create sheet and add header

  const sheetName = fileName ? `${fileName} ` : 'mRNAid'
  table[sheetName] = result.map((value, index) => {
    const items = (Object.keys(value) as DataKey[])
      .filter((key) => key !== 'RNA_structure' && key !== 'seqID' && key !== 'RNASeq')
      .map((key) => value[key])
    items.unshift(`Output ${index + 1}`)
    return items
  })
  table[sheetName].unshift(
    (Object.keys(inputData) as DataKey[])
      .filter((key) => key !== 'RNA_structure' && key !== 'RNASeq')
      .map((key) => inputData[key]),
  )
  table[sheetName].unshift(tableHeaders[type])

  return table
}

const resultsToTable = (result: InputAndResultData[], input: InputAndResultData, fileName: string): Table =>
  createPASTable(result, input, fileName)

class SaveFile extends React.PureComponent<SaveFileProps> {
  handleClick = () => {
    const {result, input, fileName} = this.props
    const table = resultsToTable(result, input, fileName)
    const newFileName = fileName || 'mRNAID'

    // ExcelJS
    const workbook = new Excel.Workbook()
    Object.keys(table).forEach((name) => {
      const sheet = workbook.addWorksheet(name.toUpperCase())
      sheet.addRows(table[name])
      workbook.xlsx
        .writeBuffer()
        .then((buffer) => FileSaver.saveAs(new Blob([buffer]), `${newFileName}.xlsx`))

        .catch((err) => message.error('Error writing excel export', err))
    })
  }

  render() {
    return (
      <Button
        className="no-print"
        type="primary"
        icon="download"
        onClick={this.handleClick}
        style={{float: 'right', margin: '10px'}}
      >
        Download as XLSX
      </Button>
    )
  }
}

export default SaveFile
