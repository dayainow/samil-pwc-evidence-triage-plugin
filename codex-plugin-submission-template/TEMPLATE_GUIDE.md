# Template Guide

Use this guide when turning the template into a real Codex plugin submission.

## 1. Pick One Company

The submission should target one company only. Do not combine multiple companies in one plugin.

Fill this in:

```text
Company:
Industry:
Target user:
Workflow moment:
Public source URLs:
Observed problem:
Plugin-assisted task:
Human final judgment:
```

## 2. Prove The Problem With Public Sources

Acceptable sources:

- company reports,
- annual reports,
- sustainability reports,
- audit reports,
- public filings,
- official help pages,
- public standards,
- news articles from reliable outlets,
- regulator or industry publications.

Avoid:

- private experience without source,
- internal company information,
- unverifiable numbers,
- confidential customer data.

## 3. Narrow The Workflow

A strong plugin does not solve the entire company problem. It solves a narrow bottleneck.

Use this sentence:

```text
When [target user] performs [specific task], they get blocked at [workflow moment] because [evidence or data problem]. The plugin helps by [AI-supported action], and the human decides [final judgment].
```

## 4. Customize The Plugin

Edit `src/.codex-plugin/plugin.json`:

- `name`: lowercase hyphen-case, 64 characters or fewer.
- `description`: one sentence explaining the plugin.
- `keywords`: domain-specific terms.
- `interface.displayName`: readable name shown to users.
- `interface.shortDescription`: short value proposition.
- `interface.longDescription`: target user, workflow, and guardrails.
- `interface.capabilities`: concrete actions the plugin supports.
- `interface.defaultPrompt`: examples of what the user asks the plugin.

Edit `src/skills/company-problem-review/SKILL.md`:

- Replace the generic problem framing.
- Define expected inputs.
- Define output structure.
- Define safety boundaries.
- Define what the AI must not decide.

Edit `examples/*.json`:

- `normal-case.json`: clean case.
- `missing-case.json`: missing required evidence or data.
- `inconsistent-case.json`: contradiction across records.

## 5. Validate Behavior

Run:

```bash
python3 src/scripts/evidence_triage.py examples/normal-case.json
python3 src/scripts/evidence_triage.py examples/missing-case.json
python3 src/scripts/evidence_triage.py examples/inconsistent-case.json
python3 -m json.tool src/.codex-plugin/plugin.json
python3 -m json.tool src/.mcp.json
```

Record what changed in each result:

```text
Normal case:
Missing case:
Inconsistent case:
Remaining limitation:
```

## 6. Prepare Logs

If your competition requires original AI conversation logs, store them in `logs/` without editing, deleting, or summarizing.

Do not manually rewrite raw logs. If the rules require a specific log hook, install and trust that hook before starting the real build conversation.

## 7. Package Submission

The final zip should usually look like:

```text
submission.zip
├── src/
│   ├── .codex-plugin/plugin.json
│   ├── skills/company-problem-review/SKILL.md
│   ├── .mcp.json
│   └── scripts/evidence_triage.py
├── README.md
└── logs/
```

Keep public portfolio files and competition submission files separate when needed.

