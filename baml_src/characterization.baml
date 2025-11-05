
// class LitCharacterization {
//   Character string
//   Protagonist bool
//   Traits string[]
//   Relationships string
// }

function AnalyzeText(input: string) -> string {
  // Perform text analysis
  client "LocalOllama3"

  prompt #"
    Identify the characters and describe their relationships with each other and output updated previous output.
    {{input}}
  "#
}


// test AnalyzeSampleText {
//   functions [AnalyzeText]
//   args {
//     input "In a village of La Mancha, the name of which I have no desire to call to mind..."
//   }
// }