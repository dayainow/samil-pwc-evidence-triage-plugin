# Submission Checklist

Use this before creating `submission.zip`.

## Required Files

- [ ] `src/.codex-plugin/plugin.json`
- [ ] At least one working plugin component besides `plugin.json`
- [ ] `src/skills/<skill-name>/SKILL.md`
- [ ] `src/.mcp.json` if referenced by `plugin.json`
- [ ] executable code or clear skill workflow
- [ ] `README.md`
- [ ] `logs/`

## Public Source Evidence

- [ ] One company only
- [ ] Public source URLs listed
- [ ] Source files or citations included
- [ ] No private or unverifiable claims
- [ ] No unsupported numbers

## Plugin Quality

- [ ] Problem is framed as a real workflow failure
- [ ] Target user is clear
- [ ] Input records are clear
- [ ] Output format is clear
- [ ] AI-assisted work is separated from human final judgment
- [ ] Safety boundaries are stated
- [ ] Missing or unclear information leads to follow-up, not guessing

## Validation

- [ ] Normal case tested
- [ ] Missing case tested
- [ ] Inconsistent case tested
- [ ] `plugin.json` is valid JSON
- [ ] `.mcp.json` is valid JSON
- [ ] Plugin validator run if available
- [ ] Test results summarized in README

## Logs

- [ ] Logs collected from the required tool or exported in an accepted text format
- [ ] Logs are original and unedited
- [ ] Logs do not contain secrets
- [ ] Logs match the plugin and README narrative

## Packaging

- [ ] Final zip contains `src/`, `README.md`, and `logs/`
- [ ] Final zip does not contain `.DS_Store`
- [ ] Final zip does not contain `tmp/`
- [ ] Final zip does not contain secret files
- [ ] Final zip does not contain public GitHub-only files unless allowed

