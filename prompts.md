# Prompts

## Initial Version

Summarize the meeting notes and list the action items.

What changed and why:
This first draft was intentionally simple, but it left too much room for the model to guess missing details. Early outputs were often too confident when the notes were vague or incomplete.

What improved, stayed the same, or got worse:
It could usually produce a readable summary, so the basic task was working. However, it was more likely to hallucinate owners, deadlines, or implied decisions than I wanted.

## Revision 1

Summarize the meeting notes into a concise JSON object. Include a short summary and a list of action items. Only include owners and deadlines if they are explicitly mentioned in the notes.

What changed and why:
I added stronger instructions about JSON output and explicitly told the model not to invent owners or deadlines. This revision was based on the failure mode where messy notes led to overconfident extra details.

What improved, stayed the same, or got worse:
This reduced hallucinated owners and deadlines, which made the action items more trustworthy. The summaries were still useful, but the model sometimes treated ambiguous discussion points as actual tasks.

## Revision 2

You summarize meeting notes into a concise JSON object. Be careful with uncertainty. Only include owners and deadlines when they are explicitly stated. If no action item is clearly assigned, return an empty `action_items` list.

What changed and why:
I added a direct instruction about uncertainty and told the model to return an empty `action_items` list when the notes do not contain a clearly assigned follow-up. This was meant to handle edge cases where the meeting included ideas or tentative discussion without a real decision.

What improved, stayed the same, or got worse:
This version was more conservative and better aligned with the evaluation set, especially the edge and failure-risk examples. The tradeoff is that it may occasionally miss a borderline action item, but that is better than inventing commitments that were never made.

## Current Use In The Prototype

- `app.py` uses Revision 2 as the default system instruction.
- The `--instructions` flag in `app.py` lets the user override the prompt at runtime.
