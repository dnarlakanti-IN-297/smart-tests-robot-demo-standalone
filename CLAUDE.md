# Adoption Journey Implementation Guide Standards

This file provides Claude Code with the standards for producing adoption journey implementation guides. If this repo already has a CLAUDE.md, incorporate the contents below into it.

## What This Repo Contains

This repo contains a demo application and an adoption journey implementation guide. The implementation guide is the primary delivery artifact: a validated, step-by-step guide that takes a customer from prerequisites to a working outcome.

## Guide Format

- **AsciiDoc only.** All implementation guides must be `.adoc` files. The PS docsite (Antora) requires AsciiDoc.
- **Standard header metadata.** Every guide starts with AsciiDoc attributes for journey metadata, followed by the PS docsite attribution block:

```asciidoc
= [Guide Title]
:product-area: [FM / Smart Tests / SDLC Metrics / CI Insights / Release Orchestration / Onboarding]
:edition-required: [Edition 1 / Edition 2 / Edition 3 / standalone FM / TBD]
:journey-slug: [kebab-case slug, e.g., fm/ui-path or smart-tests/python-pytest]
:toc: left
:toclevels: 3

[cols="1,2"]
|===
|**Author(s)**
|**Details**

|[Your Name] ([username])
|Team: PS

Date: [YYYY-MM-DD]

|**Required Check(s)**
|**Status**

|PS Official
|Pending

|ENG Approval
|Pending

|===
```

The "Success Point(s)" row is omitted for implementation guides; it only applies to ISP delivery scripts.

## Required Sections (in order)

1. **Overview**: What the customer achieves, what they have when done, who the guide is for.
2. **Prerequisites**: Concrete, verifiable checklist. Categories: product, technical, access, parameterized values table.
3. **Step-by-Step Implementation**: Numbered steps, one action per step, copy-pasteable code blocks, expected output after key steps.
4. **Verification**: At least one verification step per major capability with expected results.
5. **Troubleshooting**: Known issues and resolutions. If none yet, include the section with a placeholder note.

## Style Rules (Non-Negotiable)

1. **No emojis in prose.** Not in headings, checkpoints, knowledge check markers, or document formatting. Use text labels instead (e.g., "Success:" not "checkmark emoji"). Emojis inside code blocks or expected tool/application output are acceptable (they are part of the application, not the document).
2. **No em dashes.** Use commas, semicolons, colons, periods, or parentheses.
3. **Active voice, second person, present tense.** "Run the following command" not "The following command should be run."
4. **Code blocks specify language.** Always use `[source,bash]`, `[source,go]`, `[source,python]`, `[source,yaml]`, etc.
5. **No internal references.** No Slack channels, no internal-only URLs. Guides are customer-facing.
6. **No unverified licensing or pricing claims.** If edition requirement is uncertain, use `:edition-required: TBD` and flag it.

## Code Quality Rules

- **Every command and code snippet must be tested** against this repo's demo application and confirmed working.
- **Expected output must match actual output.** Do not show output from a different branch or version than the one the reader is following.
- **No placeholder content.** No `TODO`, `TBD`, `[screenshot here]`, `https://your-instance.example.com`, or similar. Every value must be real or a documented parameterized placeholder using the format `<YOUR_VALUE>`.
- **All referenced files must exist** in this repository. Do not reference files that haven't been created.
- **Parameterized values** (values that vary per customer) use a consistent `<YOUR_VALUE>` format and are documented in the Prerequisites section.

## Definition of Done

Before declaring the guide ready for review, every item must be true:

### Format and Metadata
- [ ] Written in AsciiDoc (`.adoc`)
- [ ] All header metadata attributes present and filled in
- [ ] Edition/licensing confirmed (not assumed or copied from another guide)

### Content Completeness
- [ ] Overview explains what the customer achieves
- [ ] All prerequisites listed, concrete, and verifiable
- [ ] Every step numbered, one action per step
- [ ] Verification section with expected results
- [ ] Troubleshooting section exists

### Code Quality
- [ ] Every command executed against this repo's demo application
- [ ] Every command produces the documented result
- [ ] All referenced files exist in this repository
- [ ] No placeholder content (TODO, TBD, screenshot placeholders, example.com URLs)
- [ ] Expected output matches actual output from the branch the reader follows
- [ ] Parameterized values use consistent format and documented in Prerequisites

### Style Compliance
- [ ] No emojis in prose (emojis in code blocks and tool output are acceptable)
- [ ] No em dashes
- [ ] Active voice, second person, present tense
- [ ] Code blocks specify language
- [ ] No Slack channels or internal-only references
- [ ] No unverified licensing or pricing claims

### Integration
- [ ] Demo application builds and runs successfully
- [ ] Guide can be followed start-to-finish on a clean setup
- [ ] Author has followed the guide end-to-end at least once

## ISP Downstream Use

This guide's content may be used to create an ISP (Integrated Success Plan) delivery script for instructor-led customer sessions. Well-structured guides with clear steps, knowledge checks, and verification points translate directly into delivery scripts. Keep this in mind when organizing content into logical modules.

## Review Process

When the guide is ready, notify Rene Cabral with the file path. Rene reviews against these standards and updates the journey spec and dashboard status in the adoption-journeys repo.
