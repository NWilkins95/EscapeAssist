# EscapeAssist Instruction Versions – Comparison Matrix & Recommendation

- Date: May 7th, 2026
---

## Comparison Matrix

| Criterion | Version A | Version B | Version C | Version D |
|-----------|-----------|-----------|-----------|-----------|
| **Grounding Reliability** | 7/10 | 8.5/10 | 7/10 | 7/10 |
| **Safety Behavior** | 10/10 | 10/10 | 10/10 | 10/10 |
| **Tone & Style** | 9/10 | 9.5/10 | 9/10 | 9/10 |
| **Clarity & Readability** | 8/10 | 9/10 | 8.5/10 | 8.5/10 |
| **User-Friendliness** | 7/10 | 9/10 | 8/10 | 7.5/10 |
| **Consistency** | 9/10 | 9/10 | 9/10 | 9.5/10 |
| **Overall Score** | **7.8/10** | **9.2/10** | **8.4/10** | **8.4/10** |

---

## Detailed Performance Breakdown

### Grounding & Accuracy

| Version | Hallucination Issues | Grounding Drift | Correct Answers | Precision |
|---------|---------------------|-----------------|-----------------|-----------|
| **A** | Wrench light (major) | Tire pressure | 5/7 | Poor on diagnostics |
| **B** | None | Tire pressure (minor) | 6.5/7 | Excellent; correctly ID'd wrench light |
| **C** | Wrench light (major) | Tire pressure | 5/7 | Poor on diagnostics |
| **D** | Wrench light (major) | Tire pressure | 5/7 | Poor on diagnostics |

**Winner:** Version B – Only minor grounding drift; correctly answered wrench light warning.

---

### Safety & Refusal Behavior

| Version | Unsafe Suggestions | Over-Confident Guidance | Refusal Quality | Safety Score |
|---------|-------------------|------------------------|-----------------|--------------|
| **A** | None | None | Correct | 10/10 |
| **B** | None | None | Correct | 10/10 |
| **C** | None | None | Correct | 10/10 |
| **D** | None | None | Correct | 10/10 |

**Winner:** Tie – All versions demonstrate excellent, consistent safety behavior. No version is better or worse in this category.

---

### Tone, Clarity & User Experience

| Version | Tone | Verbosity | Formatting | Readability | UX Appeal |
|---------|------|-----------|-----------|------------|-----------|
| **A** | Professional | Concise | Structured | Good | Neutral |
| **B** | Friendly, supportive | More detailed | Structured | Excellent | High |
| **C** | Formal, procedural | Moderate | Rigid steps | Very good | Moderate |
| **D** | Neutral, concise | Moderate | Bullet-points in steps | Very good | Moderate |

**Winner:** Version B – Friendly tone and additional detail improve user confidence without sacrificing accuracy. The extra verbosity is a *strength*, not a weakness.

---

### Consistency & Predictability

| Version | Output Consistency | Formatting Adherence | Style Stability | Performance Variability |
|---------|-------------------|---------------------|-----------------|------------------------|
| **A** | 9/10 | 9/10 | 9/10 | Low variability |
| **B** | 9/10 | 9/10 | 9/10 | Low variability |
| **C** | 9/10 | 9.5/10 | 9/10 | Low variability |
| **D** | 9.5/10 | 9.5/10 | 9/10 | Very low variability |

**Winner:** Version D – Slightly more consistent formatting (bullet-points within steps), but the difference is minimal and not significant enough to outweigh other factors.

---

## Failure Analysis

### Common Issues Across All Versions

- **Wrench Warning Light Hallucination** (Versions A, C, D only):
  - All three confused the wrench/powertrain light with TPMS system information.
  - Version B **correctly identified** the wrench light, suggesting stronger instruction clarity.
  - **Impact:** Major concern for versions A, C, and D.

- **Tire Pressure Grounding Drift** (All Versions):
  - All versions mixed example pressures with the actual procedure.
  - All versions **correctly noted** that the real value is on the Safety Compliance Certification Label.
  - **Impact:** Minor drift; not critical, but avoidable.

### Version-Specific Issues

- **Version A:** Hallucination on wrench light; minor drift on tire pressure.
- **Version B:** Only minor grounding drift on tire pressure (best performer).
- **Version C:** Hallucination on wrench light; minor drift on tire pressure; slightly unclear on Auto Start‑Stop.
- **Version D:** Hallucination on wrench light; minor drift on tire pressure; slightly unclear wording on hood release.

---

## Strengths & Weaknesses Summary

| Version | Key Strengths | Key Weaknesses | Best Use Cases |
|---------|---------------|-----------------|-----------------|
| **A** | Safety, concise, professional tone | Wrench light hallucination, less user-friendly | Technical audiences; formal contexts |
| **B** | Best grounding accuracy, friendly tone, improved clarity, user-friendly | Minor tire pressure drift (negligible) | General users; customer-facing assistant; clarity-focused |
| **C** | Formal structure, procedural clarity, consistent | Wrench light hallucination, rigid tone | Step-by-step instructions; manual-like formatting |
| **D** | Bullet-point formatting, very consistent, concise | Wrench light hallucination, least user-friendly | Structured instructions; technical audiences |

---

## Recommendation

### **PRIMARY RECOMMENDATION: Version B**

**Version B is the clear winner and should be the final instruction set.**

#### Rationale:

1. **Best Grounding Accuracy:**
   - Version B is the *only* version to correctly answer the wrench warning light question.
   - This demonstrates superior instruction clarity and reduced hallucination tendency.
   - The minor tire pressure grounding drift is negligible and present in all versions.

2. **Excellent Safety Behavior:**
   - All versions tie on safety; Version B shows no safety shortcomings.
   - Consistently refused unsafe requests.

3. **Superior User Experience:**
   - Friendly, supportive tone builds user confidence.
   - Additional verbosity improves clarity without introducing hallucinations.
   - The extra detail is *intentional and beneficial*, not a flaw.
   - Best readability and user-friendliness among all versions.

4. **Consistency & Predictability:**
   - As consistent as other versions; tied with A and C, only slightly lower than D.
   - The 0.5-point difference is negligible.

5. **Future-Proof:**
   - If grounding issues are fixed across versions (e.g., by improving retrieval or adding stronger hallucination-prevention rules), Version B's tone and user-friendliness will remain an asset.
   - The wrench-light hallucination in A, C, and D suggests these versions have fundamental grounding weaknesses that won't be resolved by tone adjustments.

#### Impact if Version B is Selected:
- Users will experience a **friendly, accurate, and highly readable** assistant.
- Safety is maintained at the highest level.
- Reduced hallucination risk compared to A, C, and D.
- The minor tire pressure drift is a known issue present in all versions and can be addressed separately if needed.

---

### Secondary Recommendation (if Version B requires revision):

**If Version B cannot be used for any reason, the fallback order is:**

1. **Version C** (second choice):
   - Better structured than A; more formal tone acceptable for manual-like content.
   - Same grounding reliability as A and D, but worse user experience.

2. **Version D** (third choice):
   - Most consistent formatting; appeals to formal/technical audiences.
   - Same grounding reliability as A and C; slightly worse clarity in specific answers.

3. **Version A** (last resort):
   - Acceptable safety and consistency, but weaker on grounding and user experience.
   - Hallucination on wrench light is concerning.

---

## Known Issues & Recommendations for Follow-Up

### All Versions Share:
- **Wrench Warning Light Hallucination** (A, C, D):
  - Recommend adding explicit content pinning or retrieval verification for warning light topics.
  - Version B's correct answer suggests adding emphasis in instructions about warning light accuracy.

- **Tire Pressure Grounding Drift** (All):
  - Recommend instruction revision to emphasize: "Always direct users to the Safety Compliance Certification Label; do not provide example pressures as alternatives."

### Version-Specific:
- **Version C:** Consider clarifying Auto Start‑Stop explanation; explicitly mention "OFF" indicator state.
- **Version D:** Consider clarifying hood release instruction; use "driver door" instead of "left‑hand front door."

---

## Conclusion

**Version B is recommended for use.** It outperforms all other versions on grounding accuracy, user experience, and clarity while maintaining the highest safety standards. The minor tire pressure drift is a known issue across all versions and can be addressed in future instruction refinements.