# core/schemas/

This folder contains **machine-readable YAML schemas** - one per component type. They define the required and optional front matter fields and Markdown sections for each component. Use them for validation and IDE autocomplete.

They are not assembled into prompts and not referenced by blueprints.

## Files

| File                   | Validates                                                         |
| ---------------------- | ----------------------------------------------------------------- |
| `persona.yaml`         | Front matter and structure of `core/source/personas/**/*.md`      |
| `skill.yaml`           | Front matter and structure of `core/source/skills/**/*.md`        |
| `shared-block.yaml`    | Front matter and structure of `core/source/shared-blocks/**/*.md` |
| `output-template.yaml` | Front matter and structure of `core/source/outputs/**/*.md`       |

## Relationship to conventions

The schemas define **what** fields are required; the convention docs in `core/conventions/` explain **why** and **how** to fill them in. Use both together when authoring a new component.

## Relationship to blueprint.schema.json

`blueprint.schema.json` (in the repo root) validates `platforms/<platform>/blueprint.yaml` files. It is separate from the component schemas here, which validate individual component files.
