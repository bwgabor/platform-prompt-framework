---
name: project-datasheet
type: output-template
version: "1.0"
language: en
status: draft
format: markdown
strictness: structured
tags: [project, datasheet, output]
---

# Purpose

A structured datasheet that captures a project's goal, scope, acceptance criteria, and risks so it can be reviewed, shared, or expanded without re-deriving context from scratch.

# Use When

Use when a new project is being defined, or an existing project needs a concise, reusable reference document independent of its domain.

# Rules

- Cover only what defines the project itself: goal, scope, acceptance criteria, and risks.
- Do not include task-level execution steps or a day-to-day plan.
- Domain-specific sections may be added, but only when they add real structural value for that project type.
- Keep each section factual and specific enough to stand alone without external context.

# Required Sections

| Section             | Required | Notes                                                             |
| ------------------- | -------- | ----------------------------------------------------------------- |
| Goal                | yes      | 1-2 sentences: what the project solves, what outcome is expected  |
| Scope               | yes      | what is included and excluded from the project                    |
| Acceptance Criteria | yes      | conditions under which the project counts as done                 |
| Risks               | yes      | known risks, constraints, dependencies                            |
| Tech Stack          | optional | for IT/DevOps-type projects: tools, platforms, languages          |
| Style Direction     | optional | for graphic/creative projects: visual direction, references, mood |

# Formatting Rules

- Title is an H1 with the project name.
- Each required section is an H2 heading, in the order listed above.
- Optional domain-specific sections appear after the four required ones, as additional H2 headings, only when relevant to the project type.
- Bullet points for scope, criteria, risks, and any list-like content.
- No nested bullets; fold sub-points into one line if needed.