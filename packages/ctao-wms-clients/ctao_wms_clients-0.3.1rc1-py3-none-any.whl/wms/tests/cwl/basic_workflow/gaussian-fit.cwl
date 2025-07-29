cwlVersion: v1.2
class: CommandLineTool
label: "Gaussian Fit Tool"

inputs:
  script_gauss:
    type: File[]
    default: gaussian_fit.py
    inputBinding:
      position: 1
  data:
    type: File[]
    inputBinding:
      position: 2

outputs:
  fit-data:
    type: File[]
    outputBinding:
      glob: ["fit.txt"]
  log:
    type: File[]
    outputBinding:
      glob: ["fit.log"]

baseCommand: ["python"]
