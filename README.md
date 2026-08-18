# platform-prompt-framework

A Markdown-first framework for structuring LLM platform configurations — personas, skills, shared instruction blocks, and output templates — with a platform-configuration system on top. Each platform (Claude, ChatGPT, ...) declares in a `blueprint.yaml` which shared components it uses and which ones it overrides, so the same underlying content can be assembled differently per platform without duplicating it.

---

## Repository structure

```bash
platform-prompt-framework/
├── README.md
├── ARCHITECTURE.md          # Key design decisions, in short form
├── blueprint.schema.json    # JSON Schema for platforms/*/blueprint.yaml
├── core/                    # Shared components, defined once
│   ├── source/              # Live, blueprint-referenced components
│   │   ├── personas/
│   │   ├── skills/
│   │   ├── shared-blocks/
│   │   └── outputs/
│   ├── conventions/         # Why/how authoring guides per component type
│   └── schemas/             # Machine-readable schema per component type
├── platforms/               # One folder per platform
│   ├── claude/
│   │   ├── blueprint.yaml   # What Claude uses from core/source/, and overrides
│   │   ├── README.md
│   │   └── skills/          # Claude-specific overrides, if any
│   ├── chatgpt/
│   ├── gemini/
│   ├── perplexity/
│   └── ...
├── templates/               # Starter files (non-schema-based only)
│   └── blueprint.yaml.template
├── scripts/                 # Developer utilities
│   └── generate_template.py # Generates component .md starters from core/schemas/
└── tests/                   # Generated example outputs, used to validate the framework
```

- **`core/source/`** holds every blueprint-referenced component that isn't platform-specific. Written once, reused everywhere. `core/conventions/` and `core/schemas/` hold supporting docs and schemas — not assembled into prompts.
- **`platforms/`** holds only what's different per platform: the `blueprint.yaml` and any override files.
- **`templates/`** holds blank starting points for non-schema-based files (currently only `blueprint.yaml.template`). For component types with a schema (`persona`, `skill`, `shared-block`, `output-template`), use `scripts/generate_template.py` instead — it generates the starter file from the schema directly.

## The blueprint system

Each platform has exactly one `platforms/<platform>/blueprint.yaml`. It lists, under `components`, which persona(s), skills, shared-blocks and output-templates that platform uses - by component `name`, not by file path.

**Source resolution (override logic):** for each component listed in a blueprint, the actual content comes from `platforms/<platform>/<type>/<name>.md` if that file exists, otherwise from `core/source/<type>/<name>.md`. This means adding a platform-specific version of a component never requires touching the blueprint - just add the file at the matching path and it takes over automatically.

**Output assembly:** by default every component gets its own output file. If a platform's prompt slots don't line up 1:1 with components (e.g. no separate skill slot, or the same content needs to land in two files), the blueprint's optional `outputs` section maps target file names to lists of `type:name` references. See `ARCHITECTURE.md` ("Output assembly") for the full rules - in short, `outputs` only ever contains references, never literal prompt text.

Every `blueprint.yaml` validates against `blueprint.schema.json`.

## Adding a new platform

1. Create `platforms/<platform>/`.
2. Copy `templates/blueprint.yaml.template` to `platforms/<platform>/blueprint.yaml` and fill it in - list the components the platform should use.
3. If the platform needs a component to behave differently than the core version, add a file at `platforms/<platform>/<type>/<name>.md` with the same `name`; it overrides the core version automatically.
4. If the platform's actual config/prompt slots don't match one-file-per-component, add an `outputs` section mapping target files to component references.
5. Validate the blueprint against `blueprint.schema.json`, and confirm every referenced component exists in `core/source/` or is overridden locally.
6. Add a short `platforms/<platform>/README.md` describing what's platform-specific and why (see `platforms/claude/README.md` for the reference example).

## Adding a new component

1. Pick the component type: `persona`, `skill`, `shared-block`, or `output-template`.
2. Read the matching convention doc in `core/conventions/` for what the component is for and common anti-patterns.
3. Generate a starter file with `scripts/generate_template.py` and fill it in:
   ```bash
   python scripts/generate_template.py --type <type> --name <name> --output core/source/<type>s/<name>.md
   ```
   The script reads `core/schemas/<type>.yaml` and produces a file with the correct front matter and all required/optional sections.
4. Save it under `core/source/<type>/<name>.md` if it's shared, or `platforms/<platform>/<type>/<name>.md` if it's an override for one platform only.
5. Add the component's `name` to the relevant blueprint(s) under `components`.

## Reference material

- `ARCHITECTURE.md` - the design decisions behind `core/` + `platforms/` and the blueprint system.
- `core/conventions/` - what each component type is for, and anti-patterns to avoid.
- `core/schemas/` and `blueprint.schema.json` - the machine-readable field/section requirements.
- `platforms/claude/` - the reference platform configuration; a working example to model new platforms on.

## What's NOT in this version

- ChatGPT, Perplexity, Gemini, Copilot, Grok, Manus platform configurations (folders exist as placeholders; content comes in a later round)
- A build/assembly tool that turns a blueprint into finished prompt files (currently manual)
- Automated validation or a CI pipeline
- A large persona/skill example catalog
