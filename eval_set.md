## Evaluation Set: Meeting Summarization

### Case 1 (Normal)
Input:
We discussed launching the new app next month. John will prepare the marketing plan. Sarah will finalize the budget by Friday.

Expected:
- Clear summary
- Action items listed
- Owners and deadlines extracted correctly

---

### Case 2 (Normal)
Input:
Team agreed to improve onboarding process. Mike will redesign the tutorial. No deadline mentioned.

Expected:
- Action item extracted
- Owner identified
- No hallucinated deadline

---

### Case 3 (Edge)
Input:
We had a general discussion about improving collaboration and communication.

Expected:
- Summary provided
- No fake action items generated

---

### Case 4 (Edge)
Input:
Notes are messy:
- app delay?
- maybe push timeline
- talk to design

Expected:
- Interpret cautiously
- Avoid overconfident assumptions
- Extract only reasonable action items

---

### Case 5 (Failure Risk / Human Review)
Input:
We might consider expanding to Europe, but no decisions were made. Someone mentioned checking legal requirements, though no owner or timeline was assigned.

Expected:
- No action items
- No hallucinated commitments, owners, or plans
- Flag uncertainty and note that human review may be needed before treating this as a follow-up
