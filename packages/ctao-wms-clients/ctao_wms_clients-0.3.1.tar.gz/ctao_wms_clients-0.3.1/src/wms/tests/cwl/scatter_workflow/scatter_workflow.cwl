cwlVersion: v1.2
class: Workflow
requirements:
    ScatterFeatureRequirement: {}

inputs:
  name_list: string[]
  script1: File
  script2: File

outputs:
  final_outputs:
    type: File[]
    outputSource: step2/processed

steps:
  generate_names:
    run: generate_names.cwl
    in:
      name: name_list
    out: [generated_name]
    scatter: name
    scatterMethod: flat_crossproduct

  step1:
    run: step_1.cwl
    in:
      script: script1
      name: generate_names/generated_name
    out: [outfile]
    scatter: name
    scatterMethod: flat_crossproduct

  step2:
    run: step_2.cwl
    in:
      script: script2
      infile: step1/outfile
    out: [processed]
    scatter: infile
    scatterMethod: flat_crossproduct
