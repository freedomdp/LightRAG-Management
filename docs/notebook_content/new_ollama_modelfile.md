---
TITLE: ollama-ollama/docs/modelfile.md at main · lloydchang/ollama-ollama · GitHub
CONTENT: 
Ollama Model File
Note Modelfile syntax is in development A model file is the blueprint to create and share models with Ollama.
Table of Contents
* Format
* Examples
* Instructions
    * FROM (Required)
    * PARAMETER
    * TEMPLATE
    * SYSTEM
    * ADAPTER
    * LICENSE
    * MESSAGE

Format
The format of the Modelfile : | Instruction | Description | | ------ | ------ | | FROM (required) | Defines the base model to use. | | PARAMETER | Sets the parameters for how Ollama will run the model. | | TEMPLATE | The full prompt template to be sent to the model. | | SYSTEM | Specifies the system message that will be set in the template. | | ADAPTER | Defines the (Q)LoRA adapters to apply to the model. | | LICENSE | Specifies the legal license. | | MESSAGE | Specify message history. |

Instructions
FROM (Required)
The FROM instruction defines the base model to use when creating a model.
... [Full text from previous view_file output] ...
---
