import {Icon, Upload} from 'antd'
import * as React from 'react'
import {RcCustomRequestOptions} from 'antd/lib/upload/interface'

const {Dragger} = Upload

const FILE_EXTENSIONS = '.fa, .fasta, .gb'

const getSequenceFromFile = (data: string | ArrayBuffer | null): string => {
  if (!data) {
    return ''
  }
  const text = data.toString()
  if (text[0] === '>') {
    return text.split('\n').slice(1).join('')
  }
  if (text.indexOf('ORIGIN') > -1) {
    return text
      .split('ORIGIN')[1]
      .split('')
      .filter((letter) => /[ATCGatcgFLIMVSYHQNKDEWRPflimvsyhqnkdewrp]/.test(letter))
      .join('')
      .toUpperCase()
  }

  return ''
}

type FileUploadInputProps = {
  onChange(data: string): void
}

class FileUploadInput extends React.PureComponent<FileUploadInputProps> {
  constructor(props: FileUploadInputProps) {
    super(props)
    this.fileReader.onload = this.onload
  }

  fileReader = new FileReader()

  onload = () => {
    this.props.onChange(getSequenceFromFile(this.fileReader.result))
  }

  onHandleRequest = (option: RcCustomRequestOptions) => {
    this.fileReader.readAsText(option.file)
    option.onSuccess({}, option.file)
  }

  render() {
    return (
      <Dragger multiple={false} accept={FILE_EXTENSIONS} customRequest={this.onHandleRequest}>
        <p className="ant-upload-drag-icon">
          <Icon type="inbox" />
        </p>
        <p className="ant-upload-text">Click or drag file to this area to upload .fa, .fasta or .gb files</p>
      </Dragger>
    )
  }
}

export default FileUploadInput
