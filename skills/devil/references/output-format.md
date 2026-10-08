# Output Format

Match the user's language. Use the compact form for Quick reviews and omit any empty or irrelevant section. Every substantial review ends with exactly one verdict.

```markdown
# Devil Review

## Verdict
GO | GO WITH CONDITIONS | REVISE | RETHINK | NO-GO

## Review Depth
Quick | Standard | Deep | Critical — reason for calibration.

## What I Reviewed
Scope, relevant evidence, and limits of the review.

## Steelman
Strongest case for the proposal.

## Strongest Concerns
### [Severity] — Title
- **Status:** VERIFIED | INFERRED | ASSUMED | UNKNOWN
- **Confidence:** High | Medium | Low
- **Evidence:** …
- **Why it matters / failure scenario:** …
- **Recommended mitigation or alternative:** …

## Hidden Assumptions
Only material assumptions and their validation status.

## Relevant Failure Modes and Edge Cases
Prioritized plausible cases only.

## Second-Order Effects
Only decision-changing effects.

## Alternatives
Only credible options, with benefit, cost, risk, and when each is preferable.

## Unknowns That Could Change the Verdict
Decision-critical missing evidence only.

## Conditions Before Proceeding
Required safeguards, accepted risks, or `None.`

## Final Challenge
The one question to answer before commitment.
```

Severity is not the verdict. Use `GO` when no meaningful blocker remains; `GO WITH CONDITIONS` when safeguards make the direction sound; `REVISE` when the design is viable but needs meaningful changes; `RETHINK` when foundational assumptions or trade-offs need reconsideration; and `NO-GO` only for unacceptable unresolved risk.
