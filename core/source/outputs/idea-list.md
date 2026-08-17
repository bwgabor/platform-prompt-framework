---
name: idea-list
type: output-template
version: "1.0"
language: en
status: stable
format: markdown
tags: [ideation, output]
---

# Template Purpose

A structured list of ideas generated during an ideation session.
Use this template when the output of a brainstorming session needs
to be saved as a reusable artifact.

# Required Sections

- Session header (topic, date, mode used)
- Idea list with descriptions and trade-offs
- Selected direction (filled in after the session)

# Formatting Rules

- Date in `YYYY-MM-DD` format.
- Ideas numbered, name in bold.
- Trade-offs in a separate line, prefixed with `⚠️`.
- Selected direction at the bottom, prefixed with `✅`.

# Template

---
**Topic:** {topic}
**Date:** {YYYY-MM-DD}
**Mode:** ideation
**Persona:** {persona-name}

## Ideas

1. **{Idea Name}**
   {1–2 sentence description of the idea.}
   ⚠️ {Trade-off or risk.}

2. **{Idea Name}**
   {1–2 sentence description.}
   ⚠️ {Trade-off or risk.}

3. **{Idea Name}**
   {1–2 sentence description.}
   ⚠️ {Trade-off or risk.}

## Selected Direction

✅ {Which idea was chosen and why — fill in after the session.}

---

<!-- Optional:

# Example
Topic: "CI/CD pipeline for a Node.js app"
Date: 2026-06-14
...

-->