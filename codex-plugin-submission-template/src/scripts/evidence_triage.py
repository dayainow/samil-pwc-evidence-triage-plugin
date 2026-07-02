#!/usr/bin/env python3
import json
import sys
from pathlib import Path


DEFAULT_REQUIRED_EVIDENCE = [
    "contract",
    "approval",
    "invoice",
    "payment_record",
    "supporting_note",
]

SOURCE_LABELS = {
    "contract": "contract evidence",
    "approval": "approval record",
    "invoice": "invoice or bill",
    "payment_record": "voucher or payment record",
    "supporting_note": "supporting note",
}

FIELD_COMPARISON_DOCUMENTS = {
    "amount": ("contract", "approval", "invoice", "payment_record"),
    "counterparty": ("contract", "invoice", "payment_record"),
    "status": ("approval", "invoice"),
    "approver": ("approval",),
}

REVIEW_SUPPORT_NOTE = (
    "This output is review support only. It identifies missing evidence, "
    "inconsistent fields, and follow-up questions based on the provided records. "
    "A human reviewer must make any final business, audit, legal, compliance, "
    "or accounting conclusion."
)


def normalize_case(payload):
    """Support both structured demo input and a simple flat input."""
    if "records" in payload:
        return {
            "case_id": payload.get("case_id", "unknown-case"),
            "problem_context": payload.get("problem_context", ""),
            "control_objective": payload.get("control_objective", ""),
            "required_evidence": payload.get("required_evidence", DEFAULT_REQUIRED_EVIDENCE),
            "records": payload.get("records") or {},
        }

    return {
        "case_id": payload.get("case_id", "legacy-flat-input"),
        "problem_context": payload.get("problem_context", ""),
        "control_objective": payload.get("control_objective", ""),
        "required_evidence": payload.get("required_evidence", DEFAULT_REQUIRED_EVIDENCE),
        "records": {
            key: {"present": value not in (None, "", "missing", False), "status": value}
            for key, value in payload.items()
            if key not in {"case_id", "problem_context", "control_objective", "required_evidence"}
        },
    }


def is_present(record):
    if isinstance(record, dict):
        return bool(record.get("present", True))
    return record not in (None, "", "missing", False)


def field(records, document, name):
    record = records.get(document)
    if not isinstance(record, dict):
        return None
    value = record.get(name)
    return value if value not in ("", None) else None


def evidence_for(records, *documents, field_name=None):
    evidence = []
    for document in documents:
        if document not in records:
            continue
        record = records[document]
        entry = {
            "source": SOURCE_LABELS.get(document, document),
            "document": document,
        }
        if field_name is not None:
            entry["field"] = field_name
            entry["value"] = field(records, document, field_name)
        elif isinstance(record, dict):
            entry["present"] = is_present(record)
        evidence.append(entry)
    return evidence


def add_finding(findings, finding_type, item, severity, message, next_action, evidence=None):
    findings.append({
        "type": finding_type,
        "item": item,
        "severity": severity,
        "message": message,
        "evidence": evidence or [],
        "next_action": next_action,
    })


def review_status(findings):
    active = [finding for finding in findings if finding["type"] != "ok"]
    if not active:
        return "ok"
    if any(finding["type"] == "blocked" for finding in active):
        return "blocked"
    if any(finding["type"] == "missing" for finding in active):
        return "missing_evidence"
    if all(finding["type"] == "needs_follow_up" for finding in active):
        return "needs_follow_up"
    return "needs_review"


def review_note(status):
    notes = {
        "ok": "No obvious evidence gaps or field mismatches were detected in the provided records.",
        "missing_evidence": "Required evidence is missing. Request the missing document or document why it is not required before making a final conclusion.",
        "blocked": "The review cannot proceed because required case information or document linkage is unavailable. Provide the missing identifier or evidence before continuing.",
        "needs_follow_up": "The provided evidence needs reviewer follow-up before a final conclusion can be made.",
        "needs_review": "Potential inconsistencies or follow-up items were detected.",
    }
    return f"{notes.get(status, notes['needs_review'])} {REVIEW_SUPPORT_NOTE}"


def build_field_comparison(records):
    comparisons = []
    for field_name, documents in FIELD_COMPARISON_DOCUMENTS.items():
        values = []
        for document in documents:
            if document not in records or not is_present(records[document]):
                continue
            values.append({
                "source": SOURCE_LABELS.get(document, document),
                "document": document,
                "field": field_name,
                "value": field(records, document, field_name),
            })

        if not values:
            continue

        known_values = {
            entry["value"]
            for entry in values
            if entry["value"] is not None
        }
        comparisons.append({
            "field": field_name,
            "consistent": len(known_values) <= 1 and all(entry["value"] is not None for entry in values),
            "values": values,
        })

    approval_date = field(records, "approval", "date")
    payment_date = field(records, "payment_record", "date")
    if approval_date or payment_date:
        comparisons.append({
            "field": "approval_payment_timing",
            "consistent": bool(approval_date and payment_date and payment_date >= approval_date),
            "values": [
                {
                    "source": SOURCE_LABELS["approval"],
                    "document": "approval",
                    "field": "date",
                    "value": approval_date,
                },
                {
                    "source": SOURCE_LABELS["payment_record"],
                    "document": "payment_record",
                    "field": "date",
                    "value": payment_date,
                },
            ],
        })

    return comparisons


def triage_evidence(payload):
    case = normalize_case(payload)
    expected = case["required_evidence"]
    records = case["records"]
    findings = []

    if not records:
        add_finding(
            findings,
            "blocked",
            "records",
            "high",
            "No evidence records were provided.",
            "Provide at least one evidence record and the sample identifier for this review case.",
        )

    for item in expected:
        if item not in records or not is_present(records[item]):
            add_finding(
                findings,
                "missing",
                item,
                "high",
                f"Missing expected evidence: {item}",
                f"Request the {item} or document why it is not required for this review.",
                evidence=evidence_for(records, item),
            )

    approval_status = str(field(records, "approval", "status") or "").lower()
    invoice_status = str(field(records, "invoice", "status") or "").lower()
    if "approval" in records and approval_status not in {"", "approved"}:
        add_finding(
            findings,
            "needs_follow_up",
            "approval_status",
            "high",
            f"Approval status is not approved: {approval_status}",
            "Confirm whether approval was completed before execution or payment.",
            evidence=evidence_for(records, "approval", field_name="status"),
        )

    if "approval" in records and "invoice" in records:
        if approval_status in {"pending", "rejected"} and invoice_status == "approved":
            add_finding(
                findings,
                "inconsistent",
                "approval_flow",
                "high",
                "Invoice is marked approved while the approval record is not approved.",
                "Reconcile invoice processing status with the approval workflow history.",
                evidence=evidence_for(records, "approval", "invoice", field_name="status"),
            )

    amount_sources = {
        document: field(records, document, "amount")
        for document in ("contract", "approval", "invoice", "payment_record")
        if field(records, document, "amount") is not None
    }
    if len(set(amount_sources.values())) > 1:
        add_finding(
            findings,
            "inconsistent",
            "amount",
            "medium",
            f"Amounts differ across records: {amount_sources}",
            "Verify the authoritative amount and explain any tax, partial payment, or currency difference.",
            evidence=[
                {
                    "source": SOURCE_LABELS.get(document, document),
                    "document": document,
                    "field": "amount",
                    "value": value,
                }
                for document, value in amount_sources.items()
            ],
        )

    counterparty_sources = {
        document: field(records, document, "counterparty")
        for document in ("contract", "invoice", "payment_record")
        if field(records, document, "counterparty") is not None
    }
    if len(set(counterparty_sources.values())) > 1:
        add_finding(
            findings,
            "inconsistent",
            "counterparty",
            "medium",
            f"Counterparties differ across records: {counterparty_sources}",
            "Confirm whether the names refer to the same legal entity or operational party.",
            evidence=[
                {
                    "source": SOURCE_LABELS.get(document, document),
                    "document": document,
                    "field": "counterparty",
                    "value": value,
                }
                for document, value in counterparty_sources.items()
            ],
        )

    approval_date = field(records, "approval", "date")
    payment_date = field(records, "payment_record", "date")
    if approval_date and payment_date and payment_date < approval_date:
        add_finding(
            findings,
            "inconsistent",
            "approval_timing",
            "high",
            f"Payment date {payment_date} is earlier than approval date {approval_date}.",
            "Check whether emergency approval, post-approval, or a date entry error occurred.",
            evidence=[
                {
                    "source": SOURCE_LABELS["approval"],
                    "document": "approval",
                    "field": "date",
                    "value": approval_date,
                },
                {
                    "source": SOURCE_LABELS["payment_record"],
                    "document": "payment_record",
                    "field": "date",
                    "value": payment_date,
                },
            ],
        )

    if "approval" in records and is_present(records["approval"]) and not field(records, "approval", "approver"):
        add_finding(
            findings,
            "needs_follow_up",
            "approver",
            "medium",
            "Approval evidence is present but approver is not identified.",
            "Request the approval log showing approver name, role, and timestamp.",
            evidence=evidence_for(records, "approval", field_name="approver"),
        )

    if not findings:
        add_finding(
            findings,
            "ok",
            "review",
            "info",
            "No obvious gaps detected in the provided evidence set.",
            "Reviewer should still confirm source authenticity and sampling scope.",
        )

    follow_up_questions = [
        finding["next_action"]
        for finding in findings
        if finding["type"] != "ok"
    ][:5]

    status = review_status(findings)
    risk_flags = [finding for finding in findings if finding["type"] != "ok"]

    return {
        "case_id": case["case_id"],
        "problem_context": case["problem_context"],
        "control_objective": case["control_objective"],
        "status": status,
        "checklist": [
            {
                "item": item,
                "present": item in records and is_present(records[item]),
                "source": SOURCE_LABELS.get(item, item),
            }
            for item in expected
        ],
        "field_comparison": build_field_comparison(records),
        "findings": findings,
        "risk_flags": risk_flags,
        "follow_up_questions": follow_up_questions,
        "review_note": review_note(status),
        "human_review_required": True,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: evidence_triage.py <json-input>"}))
        sys.exit(1)

    input_path = Path(sys.argv[1])
    data = json.loads(input_path.read_text())
    result = triage_evidence(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))

