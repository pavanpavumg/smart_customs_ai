def process_meeting_notes(raw_text):
    # A real company uses a 'Trigger List' to find tasks
    triggers = ["needs to", "should", "must", "fix", "draft", "update"]
    
    notes_list = raw_text.split('.')
    action_items = []
    
    for line in notes_list:
        # Check if ANY of our triggers are in the sentence
        if any(trigger in line.lower() for trigger in triggers):
            action_items.append(line.strip())

    return {
        "summary": raw_text.split('.')[0] + ".",
        "actions": action_items
    }