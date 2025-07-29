cwlVersion: v1.2
class: CommandLineTool

inputs:
  local_script:
    type: File
    inputBinding:
      position: 1

outputs:
  local_output:
    type: File
    outputBinding:
      glob: "output.txt"

baseCommand: ["python"]

hints:
  DockerRequirement:
    dockerPull: harbor.cta-observatory.org/proxy_cache/library/python:3.12-slim
