---
name: internal-control-evidence-review
description: Triage internal-control evidence packages by generating evidence checklists, detecting missing proof, flagging contract-voucher-approval inconsistencies, and drafting follow-up questions without making final audit judgments.
---

Use this skill when the user wants to:
1. Review an internal-control, internal audit, or internal accounting management sample.
2. Check whether required evidence is present for a transaction or control sample.
3. Compare contract, invoice, voucher, approval, payment, memo, or spreadsheet fields.
4. Identify missing evidence, approval gaps, timing issues, amount differences, or counterparty mismatches.
5. Produce a structured checklist, risk flags, and follow-up questions for a human reviewer.

Do not use this skill as a general document summarizer. The primary job is evidence triage: organize the review package, expose missing or inconsistent proof, and help the reviewer decide what to verify next.

Problem framing:
- The target scenario is Samil PwC-style internal audit and internal accounting management review.
- The business problem is not that standards are absent. The bottleneck is that evidence, approvals, and transaction records are distributed across documents and systems, so reviewers must manually reconcile them.
- The plugin should behave as a review assistant. It should structure the evidence package and surface gaps, not issue a final audit opinion.

Expected input:
- A case description, including control objective and transaction type.
- Available evidence such as contract, invoice, voucher, approval record, payment record, supporting memo, or spreadsheet extract.
- Optional expected evidence list if the user already has a control matrix.
- Optional source labels such as file name, page, row, system name, or document section.

Recommended JSON shape for the helper script:

```json
{
  "case_id": "AP-2026-001",
  "control_objective": "Vendor payment must be supported by contract, invoice, approval, and payment evidence.",
  "required_evidence": ["contract", "approval", "invoice", "payment_record", "supporting_note"],
  "records": {
    "contract": {"present": true, "amount": 12000000, "date": "2026-05-01", "counterparty": "ABC Vendor"},
    "approval": {"present": true, "status": "approved", "amount": 12000000, "date": "2026-05-03", "approver": "Finance Lead"},
    "invoice": {"present": true, "status": "approved", "amount": 12000000, "date": "2026-05-04", "counterparty": "ABC Vendor"}
  }
}
```

Workflow:
1. Identify the review case: process, control objective, period, transaction, amount, and owner.
2. Inventory available documents: contract, invoice, voucher, approval record, payment record, spreadsheet extract, and supporting memo.
3. Determine the expected evidence set from the user-provided control objective or use the default minimum set: contract, approval, invoice, payment_record, supporting_note.
4. Generate an evidence checklist that marks each expected item as present, missing, or unclear.
5. Compare records for completeness and consistency:
   - missing documents or attachments,
   - approval status not approved,
   - invoice approved while approval is pending or absent,
   - amount/date/counterparty mismatch across records,
   - payment before approval,
   - missing approver or unclear responsibility.
6. Convert each issue into a risk flag with type, severity, message, source evidence, and reviewer next action.
7. Draft concrete follow-up questions for the business owner or evidence provider.
8. If the user provides a JSON case file, suggest running `python3 src/scripts/evidence_triage.py <file>` and use the output as structured evidence for the review-support memo.

Output requirements:
- Use this top-level structure when possible:
  - `case_id`
  - `status`: `ok`, `missing_evidence`, `needs_review`, `needs_follow_up`, or `blocked`
  - `checklist`: expected evidence and whether each item is present
  - `risk_flags`: missing, inconsistent, blocked, or needs-follow-up items
  - `field_comparison`: key values compared across records when available
  - `follow_up_questions`: concrete questions for the evidence owner
  - `review_note`: fixed reminder that the output is review support only
- Mark each issue as `missing`, `inconsistent`, `needs_follow_up`, or `blocked`.
- Include severity: `high`, `medium`, `low`, or `info`.
- Include source/evidence fields when a risk flag is based on a specific document value.
- Include a short `next_action` for each issue.
- Include 3 to 5 follow-up questions when the case is not clean.
- Include a short note that the result is review support and not a final audit conclusion.
- Keep the final judgment human-reviewable and avoid automatic approval.

Risk flag guidance:
- Use `high` for missing approval evidence, missing required evidence that blocks control testing, payment before approval, approval rejected or pending while processing is complete, or unclear sample identity.
- Use `medium` for amount mismatch, counterparty mismatch, missing approver, unclear document linkage, or date inconsistencies that need explanation.
- Use `low` for formatting differences, naming variants, or minor metadata gaps that do not block review by themselves.
- Use `blocked` when the sample cannot be identified, required records are absent, or document linkage is too unclear to compare.

Safety and judgment boundaries:
- Never conclude that a control is effective, deficient, audit-reportable, compliant, non-compliant, legal, or illegal.
- Never write "pass", "fail", "control deficiency", or "audit finding" as a final conclusion.
- Use phrases such as "potential inconsistency", "missing evidence", "requires reviewer confirmation", and "follow-up needed".
- Do not decide whether alternative evidence is sufficient. Flag it for human review.
- Do not infer missing amounts, dates, counterparties, approvers, approval status, or document contents.
- If a field is not visible in the provided material, mark it as `unknown`, `not_found`, or `unavailable`.
- If matching evidence to the same sample is uncertain, return `blocked` or `needs_follow_up` instead of guessing.
- Every non-clean result must tell the reviewer what to ask for next.
- Every result must preserve human accountability for the final audit or control conclusion.

Important:
- Do not claim the review is complete unless the required evidence is clearly present.
- If information is missing, ask for the missing document or record rather than guessing.
- Prefer evidence-based conclusions over assumptions.
- Frame the result as a decision-support review, not as a final legal or audit judgment.
- Do not invent document contents. If a field is not visible in the provided material, mark it as unavailable.
- Do not store or request confidential client data for the hackathon demo. Use anonymized samples.
- If no evidence records are provided, or if the document linkage is too unclear to compare, stop with a blocked or needs-follow-up result instead of guessing.

Preferred review note:

```text
This output is review support only. It identifies missing evidence, inconsistent fields, and follow-up questions based on the provided records. A human reviewer must make any final internal-control, audit, legal, or accounting conclusion.
```
