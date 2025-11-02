class Subtask {
  id int
  name string
}

enum Priority {
  HIGH
  MEDIUM
  LOW
}

class Ticket {
  id int
  name string 
  description string
  priority Priority
  assignees string[]
  subtasks Subtask[]
  dependencies int[]
}


function ExtractTasks(transcript: string) -> Ticket[] {
  client "LocalOllama"
  prompt #"
    You are an expert at analyzing meeting transcripts and extracting structured action items and tasks.
    Extract all action items, tasks and subtasks from the meeting transcript below.
    For each task:
    - Generate a unique ID
    - Include who is assigned to it
    - Set appropriate priority level
    - Identify subtasks if any
    - Note any dependencies on other tasks

    {{ ctx.output_format }}

    {{ _.role("user") }} {{ transcript }}
  "#
}

test SimpleTranscript {
  functions [ExtractTasks]
  args {
    transcript #"
        Alice: We need to update the website by next week. This is high priority.
        Bob: I can handle that. I'll need Carol's help with the design though.
        Carol: Sure, I can help with the design part.
    "#
  }
}

test ComplexTranscript {
  functions [ExtractTasks]
  args {
    transcript #"
        Alice: Hey team, we have several critical tasks we need to tackle for the upcoming release. First, we need to work on improving the authentication system. It's a top priority.
        Bob: Got it, Alice. I can take the lead on the authentication improvements. Are there any specific areas you want me to focus on?
        Alice: Good question, Bob. We need both a front-end revamp and back-end optimization. So basically, two sub-tasks.
        Carol: I can help with the front-end part of the authentication system.
        Bob: Great, Carol. I'll handle the back-end optimization then.
        Alice: Perfect. Now, after the authentication system is improved, we have to integrate it with our new billing system. That's a medium priority task.
        Carol: Is the new billing system already in place?
        Alice: No, it's actually another task. So it's a dependency for the integration task. Bob, can you also handle the billing system?
        Bob: Sure, but I'll need to complete the back-end optimization of the authentication system first, so it's dependent on that.
        Alice: Understood. Lastly, we also need to update our user documentation to reflect all these changes. It's a low-priority task but still important.
        Carol: I can take that on once the front-end changes for the authentication system are done. So, it would be dependent on that.
        Alice: Sounds like a plan. Let's get these tasks modeled out and get started.
    "#
  }
}

