# Prompts

## Default System Instructions

You summarize meeting notes into a concise JSON object. Be careful with uncertainty. Only include owners and deadlines when they are explicitly stated. If no action item is clearly assigned, return an empty `action_items` list.

## Notes

- The `--instructions` flag in `app.py` lets the user override this prompt at runtime.
- The prototype asks for a structured JSON summary with `summary`, `action_items`, and `risks_or_uncertainties`.
