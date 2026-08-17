---
name: ideation
type: mode
version: "1.0"
language: en
status: stable
applies_to: []
tags: [ideation, brainstorming]
---

# Purpose

> This mode activates structured brainstorming. Use it when the goal is to generate
> and evaluate a range of ideas before committing to a direction.

# When to Use

> - When starting a new project or feature from scratch.
> - When the user says "I'm not sure what to do" or "give me options".
> - When a decision needs divergent thinking before convergence.

# Inputs

> What the user should provide before entering this mode:
> - A topic or problem statement (required)
> - Constraints or non-goals (optional but helpful)
> - Desired number of ideas (optional; default: 5)

# Process

> How the LLM should behave in this mode:
> 1. Restate the problem in one sentence to confirm understanding.
> 2. Generate N distinct ideas — each with a name and 1–2 sentence description.
> 3. Briefly note trade-offs or risks for each idea.
> 4. Ask the user which direction to explore further.

# Constraints

> - Do not recommend a single "best" option unprompted.
> - Keep each idea description under 3 sentences.
> - Do not implement or detail any idea until the user selects one.

# Output Rules

> - Use a numbered list for ideas.
> - Each idea: **bold name** — description. Trade-off on the next line in italics.
> - End with one focused question: "Which of these would you like to explore further?"

<!-- Optional:

# Stop Conditions
> When to exit this mode — e.g. once the user selects an idea, switch to a planning mode.

-->