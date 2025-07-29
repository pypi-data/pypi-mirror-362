cwlVersion: v1.2
class: CommandLineTool

requirements:
  InlineJavascriptRequirement: {}


hints:
  DockerRequirement:
    dockerPull: harbor.cta-observatory.org/proxy_cache/library/python:3.12-slim

baseCommand: python
inputs:
  script:
    type: File
    inputBinding:
      position: 1
  name:
    type: string
    inputBinding:
      position: 2
outputs:
  outfile:
    type: File
    outputBinding:
      glob: $(inputs.name + ".txt")
