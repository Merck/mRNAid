import * as React from 'react'
import {Document, Text, Page, StyleSheet, View} from '@react-pdf/renderer'
import {InputAndResultData, InputParameters} from 'src/types/Api'

type SavePdfProps = {
  result: InputAndResultData[]
  inputParameters: InputParameters
  loading?: boolean
  onChange?(data: object): void
}
const styles = StyleSheet.create({
  body: {
    backgroundColor: '#fff',
    paddingTop: 35,
    paddingBottom: 65,
    paddingHorizontal: 35,
  },
  header: {
    fontSize: 16,
    marginBottom: 10,
    textAlign: 'center',
    fontWeight: 'bold',
  },
  pageNumbers: {
    position: 'absolute',
    bottom: 30,
    left: 0,
    right: 0,
    textAlign: 'center',
    fontSize: 12,
  },
  title: {
    fontSize: 14,
    marginBottom: 10,
    marginTop: 10,
    fontWeight: 'bold',
  },
  subtitle: {
    display: 'flex',
    justifyContent: 'space-between',
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 5,
    fontSize: 12,
  },
  textField: {fontSize: 12, margin: 10},
  parameter: {
    fontSize: 14,
    marginBottom: 5,
  },
  output: {
    marginTop: 10,
    marginBottom: 5,
  },
  row: {
    display: 'flex',
    flexDirection: 'row',
  },
  column: {
    width: 300,
    fontSize: 10,
  },
})

class SavePdf extends React.PureComponent<SavePdfProps> {
  constructor(props: SavePdfProps) {
    super(props)
    this.state = {}
  }
  render() {
    const {result, inputParameters} = this.props
    return (
      <Document>
        <Page size="A4" style={styles.body}>
          <Text style={styles.header}>mRNAid</Text>
          <Text style={styles.title}>Input</Text>
          <View>
            <Text style={styles.subtitle}>Five Prime Flanking Sequence: {inputParameters.five_end}</Text>
            <Text style={styles.subtitle}>Three Prime Flanking Sequence: {inputParameters.three_end}</Text>
            <Text style={styles.subtitle}>mRNA Sequence: {inputParameters.input_mRNA}</Text>
          </View>
          <View>
            <Text style={styles.subtitle}>Codon Usage: {inputParameters.organism}</Text>
            <Text style={styles.subtitle}>Codon Usage freq.threshold: {inputParameters.usage_threshold}</Text>
            <Text style={styles.subtitle}>Uridine depletion: {inputParameters.uridine_depletion}</Text>
            <Text style={styles.subtitle}>avoid Motifs: {inputParameters.avoid_motifs}</Text>
          </View>
          <View>
            <Text style={styles.parameter}>Parameters</Text>
            <View style={styles.row}>
              <Text style={styles.column}>Min GC Content: {inputParameters.min_GC_content}</Text>
              <Text style={styles.column}>Max GC Content: {inputParameters.max_GC_content}</Text>
            </View>
            <View style={styles.row}>
              <Text style={styles.column}>Window Size for local GC Content: {inputParameters.GC_window_size}</Text>
              <Text style={styles.column}>Entropy Window size: {inputParameters.entropy_window}</Text>
            </View>
          </View>
          <View>
            <Text style={styles.title}>Optimized Outputs</Text>
            <View>
              {result.map((value, index) => (
                <View style={styles.output} key={`${value.MFE} ${value.score}`}>
                  <Text style={styles.subtitle}>{`Output ${index + 1}`}</Text>

                  <Text style={styles.textField}>
                    RNA Sequence: {}
                    {value.RNASeq}
                  </Text>
                  <Text style={styles.textField}>
                    DNA Sequence: {}
                    {value.DNASeq}
                  </Text>
                  <View>
                    <Text style={styles.parameter}>Parameters</Text>
                    <View style={styles.row}>
                      <Text style={styles.column}>
                        A Ratio:
                        {value.A_ratio}
                      </Text>
                      <Text style={styles.column}>
                        AT Ratio:
                        {value.AT_ratio}
                      </Text>
                    </View>
                    <View style={styles.row}>
                      <Text style={styles.column}>
                        T/U Ratio:
                        {value.TU_ratio}
                      </Text>

                      <Text style={styles.column}>
                        GC Ratio:
                        {value.GC_ratio}
                      </Text>
                    </View>
                    <View style={styles.row}>
                      <Text style={styles.column}>
                        G Ratio:
                        {value.G_ratio}
                      </Text>
                      <Text style={styles.column}>
                        MFE:
                        {value.MFE}
                      </Text>
                    </View>
                    <View style={styles.row}>
                      <Text style={styles.column}>
                        C Ratio:
                        {value.C_ratio}
                      </Text>
                      <Text style={styles.column}>
                        Score:
                        {value.score}
                      </Text>
                    </View>
                    <View style={styles.row}>
                      <Text style={styles.column}>
                        5 MFE:
                        {value.MFE_5}
                      </Text>
                      <Text style={styles.column}>
                        CAI:
                        {value.CAI}
                      </Text>
                    </View>
                  </View>
                </View>
              ))}
            </View>
          </View>
          <Text
            style={styles.pageNumbers}
            render={({pageNumber, totalPages}) => `${pageNumber} of ${totalPages}`}
            fixed
          />
        </Page>
      </Document>
    )
  }
}

export default SavePdf
