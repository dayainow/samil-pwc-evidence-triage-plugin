---
name: company-problem-review
description: Turn a public, verifiable company problem into a structured Codex review workflow with evidence checklists, risk flags, follow-up questions, and human-review guardrails.
---

Use this skill when the user wants to build or run a Codex plugin for one selected company, based on public sources and a concrete business problem.

Do not use this skill as a generic document summarizer. The primary job is to convert public problem evidence into a practical review workflow that helps a human user inspect missing information, inconsistent records, and next questions.

Customization checklist:
1. Replace the selected company name in `README.md` and `plugin.json`.
2. Add public source URLs and source files under `references/`.
3. Define the target user, task timing, input records, and expected output.
4. Adapt the expected evidence list in the examples and script if the domain is not transaction evidence.
5. Keep final judgment with the human reviewer.

Expected input:
- Selected company and public-source problem statement.
- Source URLs, reports, disclosures, articles, standards, or other verifiable material.
- A case description such as process, review objective, sample identifier, period, transaction, customer journey, or operational event.
- Available records or evidence items.
- Optional expected evidence list or review checklist.

Recommended JSON shape for the helper script:

```json
{
  "case_id": "DEMO-001",
  "problem_context": "A reviewer must verify whether one sample has the required evidence package.",
  "control_objective": "The sample must be supported by contract, approval, invoice, payment record, and supporting note.",
  "required_evidence": ["contract", "approval", "invoice", "payment_record", "supporting_note"],
  "records": {
    "contract": {"present": true, "amount": 12000000, "date": "2026-05-01", "counterparty": "ABC Vendor"},
    "approval": {"present": true, "status": "approved", "amount": 12000000, "date": "2026-05-03", "approver": "Finance Lead"},
    "invoice": {"present": true, "status": "approved", "amount": 12000000, "date": "2026-05-04", "counterparty": "ABC Vendor"}
  }
}
```

Workflow:
1. Identify the company, public source, user, and concrete situation.
2. Restate the problem as an operational failure, not just a broad inconvenience.
3. Define what the plugin can safely assist with and what a human must decide.
4. Inventory the provided evidence or records.
5. Generate a checklist for expected evidence.
6. Flag missing records, unclear records, inconsistent values, timing issues, or unsupported status changes.
7. Produce follow-up questions that a human can send to the evidence owner.
8. Preserve source references and avoid unsupported claims.

Output requirements:
- Use this top-level structure when possible:
  - `case_id`
  - `problem_context`
  - `status`: `ok`, `missing_evidence`, `needs_review`, `needs_follow_up`, or `blocked`
  - `checklist`
  - `risk_flags`
  - `field_comparison`
  - `follow_up_questions`
  - `review_note`
  - `human_review_required`
- Include severity: `high`, `medium`, `low`, or `info`.
- Include source/evidence fields when a risk flag is based on a specific document value.
- Include a concrete `next_action` for each issue.
- Include a short note that the result is review support only.

Safety and judgment boundaries:
- Never claim a final business, legal, audit, compliance, accounting, or medical conclusion.
- Never invent missing source contents, numbers, dates, names, or regulatory requirements.
- If evidence is unavailable, mark it as missing, unknown, unavailable, or blocked.
- If records cannot be linked to the same case, return `blocked` or `needs_follow_up`.
- Do not request or store secrets, API keys, passwords, confidential client data, or personally sensitive information for demo cases.
- Use anonymized examples for hackathon or public portfolio material.

Preferred review note:

```text
This output is review support only. It identifies missing evidence, inconsistent fields, and follow-up questions based on the provided records. A human reviewer must make any final business, audit, legal, compliance, or accounting conclusion.
```

