# core/source/

This folder contains the **live, blueprint-referenced components** of the Platform Prompt Framework - the files that platforms actually assemble their prompts from.

## What belongs here

A file belongs in `core/source/` if a `platforms/<platform>/blueprint.yaml` can reference it (directly or via override). Concretely: personas, skills, shared-blocks, and output templates that are intended for real use.

If a file exists here, it is considered production-ready and may be picked up by any platform's blueprint.

## What does NOT belong here

- Illustrative or tutorial examples that exist only to demonstrate the format → use a separate `examples/` folder if needed in the future
- Convention docs (authoring guidelines, anti-patterns) → `core/conventions/`
- Machine-readable schemas (YAML validation) → `core/schemas/`

## Structure

```bash
core/source/
  personas/       - persona components (.md with front matter)
  skills/         - skill components
  shared-blocks/  - reusable prompt fragments
  outputs/        - output template components
```

## Override logic

Platform-specific overrides live in `platforms/<platform>/<type>/<name>.md`. If such a file exists, it takes precedence over the `core/source/` version of the same name at assembly time. The `core/source/` file is the fallback.
