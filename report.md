# Report: Meeting Summarization Into Action Items

## Business Use Case

The business use case for this project is summarizing meetings into action items. Many teams leave meetings with rough notes, partial transcripts, or informal bullet points rather than a clean task list. That creates a practical coordination problem: people may forget who owns a follow-up, whether a deadline was mentioned, or whether an idea was actually approved. A lightweight summarization tool can help convert messy meeting notes into a short summary plus structured action items, which can save time and reduce missed follow-ups.

This workflow is valuable because it is frequent, repetitive, and usually does not require a perfect final answer on the first pass. A draft summary is still useful if it helps a human reviewer move faster. For that reason, meeting summarization is a reasonable candidate for partial automation, especially when the system is positioned as an assistant rather than a final source of record.

## Model Choice And Why

For the prototype, I used `gpt-5.4-mini` through the OpenAI Responses API. I chose it because the assignment required a small reproducible Python prototype with at least one LLM API call, and this model fit that goal well: it is strong enough to follow structured instructions, produce JSON output, and handle uncertainty better than a very small or overly generic model. I also wanted a model that worked cleanly with the structured-output design in `app.py`, where the system returns `summary`, `action_items`, and `risks_or_uncertainties`.

The assignment recommends Google AI Studio as a default choice, and that would also have been a reasonable option. I stayed with the OpenAI-based prototype because it matched the code path I had already implemented and made it straightforward to enforce structured JSON output. I did not run a full cross-model benchmark, so I cannot make a strong claim that this is the best possible model. My conclusion is narrower: it was a practical choice for a small, reproducible prototype.

## Baseline Vs. Final Design

The baseline prompt was very simple: "Summarize the meeting notes and list the action items." That version could usually produce a readable summary, but it left too much room for the model to guess details that were not actually present. In particular, it was more likely to infer implied action items, owners, or deadlines when the notes were vague.

The first revision added two important constraints: output should be a concise JSON object, and owners or deadlines should be included only when explicitly stated. This improved reliability because it reduced the number of invented details. However, the model could still turn uncertain discussion points into action items when the notes were messy.

The second revision added an even stronger rule about uncertainty: if no action item is clearly assigned, the model should return an empty `action_items` list. This change was directly motivated by the evaluation set, especially the edge case with vague collaboration discussion and the failure-risk case about expanding to Europe without a decision. Compared with the baseline, the final prompt is more conservative. That means it sometimes risks under-calling borderline tasks, but it is much better aligned with the real goal of avoiding fabricated commitments.

Overall, prompt iteration improved the output by making the prototype safer and more trustworthy. The summary quality stayed roughly similar across versions, but the final design did a better job of separating confirmed follow-ups from speculative or incomplete discussion.

## Remaining Failure Cases And Need For Human Review

The prototype still fails in situations where meeting notes are ambiguous, incomplete, or politically sensitive. For example, if the notes say "maybe," "consider," or "someone should look into this," the model may still struggle to decide whether that counts as a real task or just discussion. It can also miss contextual meaning that a human teammate would understand, such as whether a named person is truly the owner of a task or whether a deadline was tentative.

Because of that, human review is still needed before using the output as an official task record. The model is best treated as a drafting assistant, not as the final authority for assigning work. This is especially important for high-stakes decisions, compliance-related discussions, or meetings where participants speak indirectly and responsibilities are negotiated rather than clearly stated.

## Deployment Recommendation

I would recommend deploying this workflow only with review controls. Specifically, I would deploy it as a first-draft assistant that generates a meeting summary and proposed action items for a human to confirm, edit, or reject. I would not recommend deploying it as a fully automatic system that sends tasks directly to project management software without review.

Under those conditions, the workflow is useful. It can save time, improve consistency, and make informal meeting notes easier to act on. Without those conditions, the risk of hallucinated or misinterpreted action items is too high. My evidence from prompt iteration suggests that the system can be made noticeably safer, but not safe enough to eliminate human oversight.
