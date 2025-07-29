cwlVersion: v1.2
class: CommandLineTool
label: "Benchmark Data Generation Tool"

inputs:
  script_data_gen:
    type: File[]
    default: random_data_gen.py
    inputBinding:
      position: 1

  output_file_name:
    type: string
    default: data.txt
    inputBinding:
      prefix: "--file-path"
      position: 2

outputs:
  data:
    type: File[]
    outputBinding:
      glob: $(inputs.output_file_name)
  log:
    type: File[]?
    outputBinding:
      glob: "*.log"

baseCommand: ["python"]
