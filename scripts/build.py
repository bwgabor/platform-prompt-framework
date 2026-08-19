#!/usr/bin/env python3
"""
build.py — Assemble platform prompt files from blueprint.yaml

Usage:
    python scripts/build.py --platform claude
    python scripts/build.py --platform claude --output-dir platforms/claude/dist
    python scripts/build.py --platform claude --validate
    python scripts/build.py --platform claude --separator=hr
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

# Maps blueprint component type → core/source subdirectory name
CORE_DIR_MAP = {
    "personas": "personas",
    "skills": "skills",
    "shared-blocks": "shared-blocks",
    "output-templates": "outputs",
}

COMPONENT_TYPES = list(CORE_DIR_MAP.keys())


def find_repo_root() -> Path:
    """Return the repo root (parent of the scripts/ directory)."""
    return Path(__file__).resolve().parent.parent


def load_blueprint(root: Path, platform: str) -> dict:
    bp_path = root / "platforms" / platform / "blueprint.yaml"
    if not bp_path.exists():
        sys.exit(f"ERROR: Blueprint not found: {bp_path}")
    with bp_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_blueprint(root: Path, blueprint: dict):
    try:
        import jsonschema
    except ImportError:
        sys.exit("ERROR: --validate requires the 'jsonschema' package. Install it with: pip install jsonschema")
    schema_path = root / "blueprint.schema.json"
    if not schema_path.exists():
        sys.exit(f"ERROR: Schema not found: {schema_path}")
    import json
    with schema_path.open(encoding="utf-8") as f:
        schema = json.load(f)
    try:
        jsonschema.validate(blueprint, schema)
        print("Blueprint validation OK.")
    except jsonschema.ValidationError as e:
        sys.exit(f"ERROR: Blueprint validation failed: {e.message}")


def resolve_component(root: Path, platform: str, comp_type: str, name: str) -> Path:
    """Return the source file path for a component, applying override logic."""
    override = root / "platforms" / platform / comp_type / f"{name}.md"
    core_dir = CORE_DIR_MAP.get(comp_type)
    if core_dir is None:
        sys.exit(f"ERROR: Unknown component type: {comp_type}")
    core = root / "core" / "source" / core_dir / f"{name}.md"

    if override.exists():
        return override
    if core.exists():
        return core
    sys.exit(f"ERROR: Component not found: {comp_type}/{name}\n  Checked:\n    {override}\n    {core}")


def strip_front_matter(text: str) -> str:
    """Remove YAML front matter (between first and second '---' lines)."""
    lines = text.splitlines(keepends=True)
    if not lines:
        return text
    # Front matter starts with '---' on line 0
    if lines[0].strip() != "---":
        return text
    # Find closing '---'
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[i + 1:])
    return text  # No closing --- found, return as-is


def extract_shared_block_instructions(text: str) -> str:
    """
    For shared-blocks: find '# Instructions' heading and return everything after it
    (the heading line itself is excluded).
    """
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if re.match(r"^#\s+Instructions\s*$", line, re.IGNORECASE):
            return "".join(lines[i + 1:])
    # No Instructions heading found — return full text with a warning
    print("WARN: shared-block has no '# Instructions' heading — using full content.")
    return text


def downshift_headings(text: str) -> str:
    """Shift all markdown headings down by one level (H1→H2, H2→H3, ..., H6→H6)."""
    def replacer(m):
        hashes = m.group(1)
        rest = m.group(2)
        new_level = min(len(hashes) + 1, 6)
        return "#" * new_level + rest
    return re.sub(r"^(#{1,6})([ \t].*)$", replacer, text, flags=re.MULTILINE)


def get_body(path: Path, comp_type: str) -> str:
    """Read a component file and return its body (front matter stripped, shared-block extracted)."""
    text = path.read_text(encoding="utf-8")
    body = strip_front_matter(text)
    if comp_type == "shared-blocks":
        body = extract_shared_block_instructions(body)
    return body.strip()


def assemble_multi(components: list[tuple[str, str, Path]], separator: str) -> str:
    """
    Assemble multiple components into one file.
    Inserts H1 separator heading + downshifts headings for each component.
    """
    parts = []
    for comp_type, name, path in components:
        body = get_body(path, comp_type)
        body_shifted = downshift_headings(body)
        # Separator heading: "# tipo: name"
        type_label = comp_type.rstrip("s")  # "personas"→"persona", "skills"→"skill", etc.
        header = f"# {type_label}: {name}"
        parts.append(f"{header}\n\n{body_shifted}")

    if separator == "hr":
        return "\n\n---\n\n".join(parts)
    else:
        return "\n\n".join(parts)


def assemble_single(comp_type: str, name: str, path: Path) -> str:
    """Assemble a single component (no heading changes)."""
    return get_body(path, comp_type)


def build(root: Path, platform: str, output_dir: Path, separator: str):
    blueprint = load_blueprint(root, platform)
    components_decl = blueprint.get("components", {})
    outputs_decl = blueprint.get("outputs", {})

    # Resolve all declared components
    resolved: dict[str, dict[str, Path]] = {}  # type → {name → path}
    for comp_type in COMPONENT_TYPES:
        resolved[comp_type] = {}
        for name in components_decl.get(comp_type, []):
            path = resolve_component(root, platform, comp_type, name)
            resolved[comp_type][name] = path

    # Track which components are referenced in outputs
    referenced: dict[str, set[str]] = {t: set() for t in COMPONENT_TYPES}

    output_dir.mkdir(parents=True, exist_ok=True)
    built = []
    warnings = []

    # --- Build outputs-section files ---
    for out_name, ref_list in outputs_decl.items():
        components_for_output = []
        for ref in ref_list:
            comp_type, name = ref.split(":", 1)
            if name not in resolved.get(comp_type, {}):
                sys.exit(f"ERROR: outputs references undeclared component: {comp_type}/{name}")
            path = resolved[comp_type][name]
            components_for_output.append((comp_type, name, path))
            referenced[comp_type].add(name)

        out_path = output_dir / f"{out_name}.md"
        if len(components_for_output) == 1:
            comp_type, name, path = components_for_output[0]
            content = assemble_single(comp_type, name, path)
        else:
            content = assemble_multi(components_for_output, separator)

        out_path.write_text(content + "\n", encoding="utf-8")
        source_labels = [f"{p.relative_to(root)}" for _, _, p in components_for_output]
        built.append((out_name + ".md", source_labels))

    # --- Build standalone files for unreferenced components ---
    for comp_type in COMPONENT_TYPES:
        for name, path in resolved[comp_type].items():
            if name in referenced[comp_type]:
                continue
            if comp_type == "shared-blocks":
                warnings.append(f"shared-block '{name}' declared but not referenced in outputs - skipped")
                continue
            out_path = output_dir / f"{name}.md"
            content = assemble_single(comp_type, name, path)
            out_path.write_text(content + "\n", encoding="utf-8")
            built.append((f"{name}.md", [str(path.relative_to(root))]))

    # --- Report ---
    print(f"\nBuilt {len(built)} file(s) to {output_dir.relative_to(root)}/")
    for filename, sources in built:
        if len(sources) == 1:
            override_tag = "  [override]" if "platforms" in sources[0] and "/skills/" in sources[0] or "/personas/" in sources[0] else ""
            # Check if any source is a platform override (not core/)
            is_override = not sources[0].startswith("core")
            tag = "  [override]" if is_override else ""
            print(f"  {filename:<40} ({sources[0]}){tag}")
        else:
            print(f"  {filename}")
            for s in sources:
                is_override = not s.startswith("core")
                tag = "  [override]" if is_override else ""
                print(f"    ← {s}{tag}")

    for w in warnings:
        print(f"WARN: {w}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Assemble platform prompt files from blueprint.yaml")
    parser.add_argument("--platform", required=True, help="Platform name (e.g. claude)")
    parser.add_argument("--output-dir", help="Output directory (default: platforms/<platform>/dist/)")
    parser.add_argument("--validate", action="store_true", help="Validate blueprint against blueprint.schema.json")
    parser.add_argument("--separator", choices=["hr", "none"], default="none",
                        help="Separator between components in multi-component files (default: none)")
    args = parser.parse_args()

    root = find_repo_root()

    blueprint = load_blueprint(root, args.platform)
    if args.validate:
        validate_blueprint(root, blueprint)

    output_dir = Path(args.output_dir) if args.output_dir else root / "platforms" / args.platform / "dist"
    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir

    build(root, args.platform, output_dir, args.separator)


if __name__ == "__main__":
    main()
