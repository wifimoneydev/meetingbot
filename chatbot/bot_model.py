from typing import List, Dict, Any
from transformers import pipeline

# ==================== Initialize pre-trained models ====================

# Q&A model
qa_model = pipeline(
    "question-answering",
    model="distilbert-base-uncased-distilled-squad"
)

# Summarizer
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

# Automatic Speech Recognition (ASR) model for Whisper
asr_model = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small"
)

# ==================== Dummy meeting transcript ====================
MEETING_TRANSCRIPT: str = """
Your meeting was held on Wednesday at 10:30 AM via Zoom. The meeting started with a quick check-in on everyone’s current tasks.

**Participants:**  
- Sarah (Project Manager)  
- Daniel (Software Engineer)  
- Maria (UX Designer)  
- David (Marketing Lead)  

**Discussion Summary:**  
Sarah gave an overview of the new product feature (the dashboard) and its goals for Q3. Daniel provided an update on backend integration and noted that the API is stable, but unit tests still need to be completed. Maria shared the new design mockups and explained the changes in the UI. David gave a brief market update, pointing out that competitor A launched a similar product last week.

**Key Action Items:**  
- Daniel to finish API unit tests and document them by next Tuesday.  
- Maria to update the design prototype based on Sarah's feedback and share the new version by Friday.  
- David to draft a new marketing campaign plan emphasizing the dashboard features and send it by next Monday.

**Decisions Made:**  
- The team agreed to shift the next sprint focus to dashboard usability testing.  
- The release date for the beta version was moved from August 10 to August 15 to give more buffer for QA.

**Next Steps:**  
Sarah will follow up with QA about test requirements and coordinate with IT for deployment logistics. Daniel will also prepare a demo of the working dashboard for the next meeting.

**Next meeting:**  
The next meeting is scheduled for Tuesday at 9 AM. Agenda: review progress on action items and finalize the product launch timeline.
"""

# ==================== Helper Functions ====================

def extract_action_items(transcript: str) -> str:
    action_lines = []
    capture = False
    for line in transcript.splitlines():
        if "Key Action Items" in line:
            capture = True
            continue
        if capture:
            if line.strip() == "" or line.startswith("**"):
                break
            if line.strip().startswith("-"):
                action_lines.append(line.strip("- ").strip())
    return "\n".join(action_lines) if action_lines else "No action items found."

def extract_decisions(transcript: str) -> str:
    decision_lines = []
    capture = False
    for line in transcript.splitlines():
        if "Decisions Made" in line:
            capture = True
            continue
        if capture:
            if line.strip() == "" or line.startswith("**"):
                break
            if line.strip().startswith("-"):
                decision_lines.append(line.strip("- ").strip())
    return "\n".join(decision_lines) if decision_lines else "No decisions found."

def extract_next_steps(transcript: str) -> str:
    next_steps = []
    capture = False
    for line in transcript.splitlines():
        if "Next Steps" in line:
            capture = True
            continue
        if capture:
            if line.strip() == "" or line.startswith("**"):
                break
            next_steps.append(line.strip())
    return "\n".join(next_steps) if next_steps else "No next steps found."

def extract_participants(transcript: str) -> str:
    """Extract participant names from the meeting transcript under the Participants section."""
    participants = []
    capture = False
    for line in transcript.splitlines():
        if "Participants" in line:
            capture = True
            continue
        if capture:
            # Stop capturing after blank or next section
            if line.strip() == "" or line.startswith("**"):
                break
            # Get the part before parentheses to just list the names
            if line.strip().startswith("-"):
                name = line.strip("- ").split("(")[0].strip()
                participants.append(name)
    return ", ".join(participants) if participants else "No participant info found."

def extract_challenges(transcript: str) -> str:
    """Try to extract challenges or issues mentioned in the Discussion Summary."""
    summary_start = transcript.find("Discussion Summary:")
    if summary_start == -1:
        return "No challenges found."
    # Capture the summary text
    summary_text = transcript[summary_start:].splitlines()[1:]  # all lines after Discussion Summary:
    summary_text = [line for line in summary_text if line.strip() and not line.startswith("**")]
    # This is very basic — you could do regex to look for keywords like 'challenge', 'problem', etc.
    return " ".join(summary_text) if summary_text else "No explicit challenges found."



# ==================== Transcript Setter ====================

def set_transcript(new_text: str) -> None:
    """Allow dynamic update of the meeting transcript in this bot session."""
    global MEETING_TRANSCRIPT
    MEETING_TRANSCRIPT = new_text

# ==================== Audio Transcription ====================

def transcribe_audio(file_path: str) -> str:
    """Transcribe an audio file into text using Whisper (openai/whisper-small)."""
    result = asr_model(file_path)
    return result.get('text', '')

# ==================== Main bot response ====================

# ==================== Main bot response ====================

from typing import List, Dict, Any

def get_bot_response(message: str) -> str:
    normalized = message.lower().strip()

    # Explicit checks
    if "when" in normalized or "next meeting" in normalized:
        result: Dict[str, Any] = qa_model(
            question="When is my next meeting?",
            context=MEETING_TRANSCRIPT
        )
        return result.get('answer', "Sorry, I couldn't find the next meeting.")

    elif "summarize" in normalized or "summary" in normalized:
        summary_result: List[Dict[str, str]] = summarizer(
            MEETING_TRANSCRIPT,
            max_length=100,
            min_length=40,
            do_sample=False
        )
        return summary_result[0].get('summary_text', "Sorry, I couldn't summarize the meeting.")

    elif "action items" in normalized:
        return extract_action_items(MEETING_TRANSCRIPT)

    elif "decisions" in normalized or "made" in normalized:
        return extract_decisions(MEETING_TRANSCRIPT)

    elif "next steps" in normalized:
        return extract_next_steps(MEETING_TRANSCRIPT)

    elif "participants" in normalized or "attended" in normalized:
        return extract_participants(MEETING_TRANSCRIPT)

    elif "challenges" in normalized or "problems" in normalized or "issues" in normalized:
        return extract_challenges(MEETING_TRANSCRIPT)

    # ✅ Fallback to generic Q&A
    result: Dict[str, Any] = qa_model(
        question=message,
        context=MEETING_TRANSCRIPT
    )
    return result.get('answer', "Sorry, I couldn't find that information in the meeting transcript.")
