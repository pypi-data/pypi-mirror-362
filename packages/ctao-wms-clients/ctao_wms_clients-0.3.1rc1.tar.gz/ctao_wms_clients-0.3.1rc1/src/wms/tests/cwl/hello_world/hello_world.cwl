cwlVersion: v1.2
class: CommandLineTool

inputs:
  message:
    type: string
    default: "Hello, World!"  # Default message if no input is provided
    inputBinding:
      position: 1  # Places the input after `echo`

outputs: []

baseCommand: echo
