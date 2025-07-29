cwlVersion: v1.2
class: Workflow
label: "Main Workflow"
doc: >
  This workflow is composed of two dependent workflows
  each composed of two command line tools:
  - data-generation: produce data
  - fit: run gaussian fit on data

inputs:
  script_data_gen:
    type: File[]
    default: random_data_gen.py
  output_file_name:
    type: string
    default: data_gen.txt
  script_gauss:
    type: File[]
    default: gaussian_fit.py

outputs:
  fit-data:
    type: File[]
    outputSource:
      - fit/fit-data
    linkMerge: merge_flattened
  logs:
    type: File[]?
    outputSource:
      - fit/log
    linkMerge: merge_flattened

steps:
  data-generation:
    run: data-generation.cwl
    in:
      script_data_gen: script_data_gen
      output_file_name: output_file_name
    out: [data, log]

  fit:
    run: gaussian-fit.cwl
    in:
      script_gauss: script_gauss
      data: data-generation/data
    out: [fit-data, log]
