# HW2

This repository contains a small reproducible prototype for meeting-note summarization.

## Workflow

The prototype takes raw meeting notes from a text file, sends them to an LLM, and produces a structured summary with action items and uncertainties.

## Files

- `app.py`: command-line prototype for the workflow
- `sample_meeting_notes.txt`: example input a grader can use
- `prompts.md`: system prompt used by the prototype
- `eval_set.md`: evaluation examples and notes
- `report.md`: assignment report draft

## How To Run

1. Make sure Python 3 is installed.
2. Install the OpenAI Python package only if you want to compare SDK examples in the docs. This prototype itself uses only Python standard library modules.
3. Set your API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

4. Run the prototype:

```bash
python3 app.py --input sample_meeting_notes.txt --output output/meeting_summary.json
```

5. Optionally override the default instructions:

```bash
python3 app.py \
  --input sample_meeting_notes.txt \
  --instructions "Summarize the meeting briefly and be conservative about action items."
```

## What The Script Produces

- Structured sections printed to the terminal
- A JSON file saved to `output/meeting_summary.json` by default

## Walkthrough Video

Video Link: https://youtu.be/-NHZQAKDu88
