cwlVersion: v1.2
class: ExpressionTool

requirements:
  InlineJavascriptRequirement: {}

inputs:
  name:
    type: string
outputs:
  generated_name:
    type: string
expression: |
  ${
    return { generated_name: "gamma_" + inputs.name };
  }
