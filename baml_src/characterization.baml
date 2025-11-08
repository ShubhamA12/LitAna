
// class LitCharacterization {
//   Character string
//   Protagonist bool
//   Traits string[]
//   Relationships string
// }

// class characters {
//   name string
//   role string @description(#"
//     Valid values: "protagonist", "antagonist", "supporting", "minor"
//   "#)
//   relationships Relationship[] @description(#"
//     List of relationships with other characters.
//   )
// }

// class Relationships(
//   name string,
//   type string @description(#"
//     Valid values: "family", "friend", "romantic", "rival", "mentor", "colleague", "other"
//   "#)
// )

enum Weight{
  ACQUAINTANCE
  OUTER_CIRCLE
  INNER_CIRCLE
}

class Relationship{
  name string
  type string @description(#"The type of relationship, e.g., friendship, rivalry, mentorship."#)
  weight Weight @description(#"strength of relationship"#)
}

class Characters{
  name string
  role string @description(#"The role of the character in the story, e.g., protagonist, antagonist, sidekick."#)
  relationships Relationship[] @description(#"A list of relationships the character has with other characters in the story."#)
}

class TextSections{
  section_id int
  text string
}


function AnalyzeText(input: string) -> Characters[] {
  // Perform text analysis
  client "LocalOllama3"

  prompt #"
    {{_.role('user')}}
    Identify the characters and describe their relationships with each other and output updated previous output.
    {{input}}
    {{ctx.output_format}}
  "#
}


// test AnalyzeSampleText {
//   functions [AnalyzeText]
//   args {
//     input "In a village of La Mancha, the name of which I have no desire to call to mind..."
//   }
// }


// function CharacterRelationships(txt: string, prev_output: Characters[]) -> Characters[] {
//   client ""
//   prompt #"
//     {% if not prev_output %}
//     Given the following text, identify the main characters and describe their relationships with each other.
//     <text>{{txt}}</text>
//     {% else %}
//     Given the following text and previous output, identify the main characters and describe their relationships with each other and output updated previous output.
//     <text>{{txt}}</text>
//     <previous>{{prev_output}}</previous>
//     {% endif %}
//     {{ctx.output_format}}
//   "#

// }