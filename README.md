# Samil PwC Internal Control Evidence Triage Plugin

Codex plugin prototype for the AX Hackathon preliminary round.  
This project turns a public, verifiable business problem into a working Codex plugin: helping internal-control reviewers detect missing evidence and document inconsistencies before drafting audit workpapers.

## Summary

Internal-control and internal accounting management reviews often require a reviewer to reconcile multiple pieces of evidence for one transaction sample: contracts, approvals, invoices, vouchers, payment records, supporting notes, and spreadsheet extracts.

The hard part is not that documents exist. The bottleneck is that reviewers must manually determine whether those scattered records form a complete and consistent evidence package.

This plugin focuses on that exact pre-review stage. It does not make audit conclusions. It structures evidence, flags missing or inconsistent records, and drafts follow-up questions for a human reviewer.

## What It Does

Given one internal-control sample package, the plugin produces:

- `checklist`: required evidence and whether each item is present
- `field_comparison`: amount, counterparty, approval status, approver, and timing comparisons
- `risk_flags`: missing evidence and inconsistency candidates
- `follow_up_questions`: questions to send back to the evidence owner
- `review_note`: a guardrail reminding users that the output is review support only

Example use case:

> A junior internal-audit reviewer is preparing workpapers for vendor-payment samples. The reviewer has a contract, invoice, payment record, and approval log, but needs to know whether required evidence is missing and whether the amount, vendor name, approval status, and payment timing align.

## Why This Problem

Samil PwC publicly describes Assurance, internal audit, internal control, internal accounting management, and Digital/AI Trust as key service areas. Those areas all rely on reliable evidence and repeatable review workflows.

Public sources used for problem framing:

- Samil PwC Assurance: https://www.pwc.com/kr/ko/assurance.html
- Samil PwC Internal Audit and Internal Control Advisory: https://www.pwc.com/kr/ko/assurance/internal-audit.html
- Samil PwC Internal Accounting Management System Advisory: https://www.pwc.com/kr/ko/assurance/internal-accounting-management-system.html
- Samil PwC Tax Agent: https://www.pwc.com/kr/ko/digital-solutions/tax-agent.html

The project narrows this broad domain into a practical workflow: transaction-sample evidence triage. That scope keeps the AI useful while avoiding unsafe claims about final audit judgment, legal responsibility, or control effectiveness.

## Target User

Primary user:

- Junior internal-audit reviewer
- Internal-control testing staff
- Audit assistant preparing sample-level workpapers

Moment of use:

- After evidence has been collected from the business owner
- Before workpaper drafting or senior review
- When the reviewer needs to know what is missing, inconsistent, or unclear

## Plugin Structure

```text
src/
├── .codex-plugin/
│   └── plugin.json
├── .mcp.json
├── skills/
│   └── company-issue-research/
│       └── SKILL.md
└── scripts/
    └── evidence_triage.py

examples/
├── normal-case.json
├── missing-case.json
└── inconsistent-case.json
```

Key files:

- `src/.codex-plugin/plugin.json`: Codex plugin manifest
- `src/skills/company-issue-research/SKILL.md`: skill instructions, workflow, output schema, and safety boundaries
- `src/scripts/evidence_triage.py`: deterministic helper script used for validation and demo scenarios
- `examples/*.json`: normal, missing-evidence, and inconsistency test cases

## How It Works

The helper script accepts a structured transaction sample.

```json
{
  "case_id": "AP-2026-001",
  "control_objective": "Vendor payment must be supported by contract, invoice, approval, payment record, and supporting note.",
  "required_evidence": ["contract", "approval", "invoice", "payment_record", "supporting_note"],
  "records": {
    "contract": {
      "present": true,
      "amount": 12000000,
      "date": "2026-05-01",
      "counterparty": "ABC Vendor"
    },
    "approval": {
      "present": true,
      "status": "approved",
      "amount": 12000000,
      "date": "2026-05-03",
      "approver": "Finance Lead"
    },
    "invoice": {
      "present": true,
      "status": "approved",
      "amount": 12000000,
      "date": "2026-05-04",
      "counterparty": "ABC Vendor"
    }
  }
}
```

It returns a review-support result with:

- one overall `status`
- an evidence checklist
- field-level comparisons
- risk flags with severity and source values
- follow-up questions
- a human-review-required note

## Quick Start

Run the three validation cases:

```bash
python3 src/scripts/evidence_triage.py examples/normal-case.json
python3 src/scripts/evidence_triage.py examples/missing-case.json
python3 src/scripts/evidence_triage.py examples/inconsistent-case.json
```

Validate JSON files:

```bash
python3 -m json.tool src/.codex-plugin/plugin.json
python3 -m json.tool src/.mcp.json
python3 -m json.tool examples/normal-case.json
python3 -m json.tool examples/missing-case.json
python3 -m json.tool examples/inconsistent-case.json
```

## Validation Results

| Case | Expected status | Actual status | Risk flags | Follow-up questions | Result |
|---|---|---|---:|---:|---|
| Normal | `ok` | `ok` | 0 | 0 | Pass |
| Missing evidence | `missing_evidence` | `missing_evidence` | 2 | 2 | Pass |
| Inconsistent records | `needs_review` | `needs_review` | 6 | 5 | Pass |

The tests cover:

- a complete and consistent evidence package
- missing approval and supporting note evidence
- pending approval while invoice is approved
- payment before approval
- amount mismatch
- counterparty mismatch
- missing approver

## AI Design Boundaries

The plugin intentionally avoids final audit conclusions.

AI-assisted:

- evidence inventory
- required-document checklist
- field comparison
- missing-evidence detection
- inconsistency candidate detection
- follow-up question drafting

Human-owned:

- final internal-control conclusion
- audit finding decision
- legal or accounting responsibility
- sufficiency of alternative evidence
- final workpaper sign-off

This boundary is implemented in both the skill instructions and the script output. Every non-clean output is framed as a review-support finding, not a final audit opinion.

## What I Focused On

This project was designed to show practical AI product judgment, not just prompt writing.

Engineering and product choices:

- narrowed a broad assurance/internal-control domain into a testable sample-review workflow
- kept the plugin scoped to pre-judgment evidence triage
- used deterministic example cases to make validation repeatable
- separated AI assistance from human accountability
- used public sources and anonymized sample data
- packaged the workflow as a Codex plugin with a skill, manifest, MCP config, helper script, examples, and README

## Hackathon Submission Notes

The competition submission is packaged separately as `submission.zip`.  
For public GitHub hygiene, raw conversation logs and local hook files are excluded from version control through `.gitignore`.

Excluded from the public repository:

- `logs/`
- `submission/`
- `submission.zip`
- `log-hooks.zip`
- `.codex/`
- `.claude/`
- `tools/`
- `tmp/`

## Disclaimer

This repository is a hackathon prototype using public materials and anonymized sample data. It is not affiliated with or endorsed by Samil PwC. It does not provide audit, legal, accounting, or compliance conclusions.
