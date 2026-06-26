# Change Decision – [Category] – [Brief Description]

- Date: YYYY-MM-DD
- Owner: Nicholas Wilkins
- Iteration: iter-NNN
- Affected Version(s): V0 / V1 / V2
- Category: preprocessing / instructions / fallback

---

## Summary

[One-sentence summary of the change.]

---

## Context

**Problem Identified:**
[Describe the specific failure pattern or issue that triggered this change.]

**Questions Affected:**
[List question IDs or types most affected by this problem. Reference the run report for details.]

**Why This Approach:**
[Explain why this particular change was chosen over alternatives.]

---

## Change Details

### Category: Preprocessing
*Use if modifying V2 text extraction, cleanup, or organization.*

**File(s) Modified:**
- TBD

**Change:**
```
[Exact code change, config change, or script modification.]
```

**Rationale:**
[Why this change should fix the identified problem.]

---

### Category: Agent Instructions
*Use if modifying the system prompt in `workflows/V{0,1,2}workflow.py` or instruction files.*

**Before:**
```
[Original instruction text or relevant excerpt.]
```

**After:**
```
[New instruction text or relevant excerpt.]
```

**Rationale:**
[Why this wording change should address the issue.]

---

### Category: Fallback Response Rules
*Use if adding a deterministic post-processing rule.*

**Rule Description:**
[Describe the fallback rule in plain English.]

**Trigger Condition:**
[What conditions cause this rule to activate?]

**Action:**
[What does the rule do when triggered?]

**Rationale:**
[Why is a fallback rule appropriate here instead of instruction or preprocessing changes?]

---

## Expected Outcome

**If Successful:**
- [What metric(s) should improve?]
- [Which question types should improve?]
- [How much improvement is realistic?]

**If Unsuccessful:**
- [What would indicate this change didn't work?]
- [What would you try next?]

---

## Results

### Metrics Comparison

| Metric | Baseline | Previous | Current | Change | Status |
|--------|----------|----------|---------|--------|--------|
| V0 Correctness (norm) | TBD | TBD | TBD | TBD | ✓ / ✗ / ~ |
| V1 Correctness (norm) | TBD | TBD | TBD | TBD | ✓ / ✗ / ~ |
| V2 Correctness (norm) | TBD | TBD | TBD | TBD | ✓ / ✗ / ~ |

### Per-Question-Type Breakdown

| Question Type | V0 Result | V1 Result | V2 Result | Notes |
|---------------|-----------|-----------|-----------|-------|
| factual | TBD | TBD | TBD | TBD |
| procedural | TBD | TBD | TBD | TBD |
| table | TBD | TBD | TBD | TBD |

### Specific Questions Affected

**Questions That Improved:**
- Q#: TBD (reason)
- Q#: TBD (reason)

**Questions That Regressed:**
- Q#: TBD (reason)

**Questions That Stayed the Same:**
- Q#: (most questions, no change expected)

---

## Decision

**Keep / Revert / Conditional Keep**

**Justification:**
[One paragraph explaining the decision and next steps.]

---

## Next Steps

[ ] Change is live; monitor for edge cases
[ ] Revert change; try different approach
[ ] Modify change before next iteration (describe how)
[ ] Keep but note limitation (describe limitation)

**Recommended Next Iteration:**
[What should be tried next, based on results of this change?]
