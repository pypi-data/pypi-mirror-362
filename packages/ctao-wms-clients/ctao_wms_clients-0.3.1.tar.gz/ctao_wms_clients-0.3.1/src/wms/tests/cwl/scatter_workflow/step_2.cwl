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
  infile:
    type: File
    inputBinding:
      position: 2
outputs:
  processed:
    type: File
    outputBinding:
      glob: $(inputs.infile.basename.replace(".txt", "_processed.txt"))
