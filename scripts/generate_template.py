import argparse
import sys
from pathlib import Path
import yaml

# Valid component types for the --type argument
VALID_TYPES = ["persona", "skill", "shared-block", "output-template"]

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a component .md template from its YAML schema."
    )
    parser.add_argument("--type", required=True, choices=VALID_TYPES,
                        help="Component type (e.g. persona, skill)")
    parser.add_argument("--name", required=True,
                        help="Component name, used in front matter")
    parser.add_argument("--output",
                        help="Output file path. If omitted, prints to stdout.")
    parser.add_argument("--lang", default="en",
                        help="Language field value (default: en)")
    return parser.parse_args()


def load_schema(component_type: str) -> dict:
    # Project root is one level up from the script's location (scripts/)
    repo_root = Path(__file__).parent.parent
    schema_path = repo_root / "core" / "schemas" / f"{component_type}.yaml"

    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(1)

    with open(schema_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_front_matter(schema: dict, name: str, lang: str) -> str:
    properties = schema.get("properties", {})
    lines = ["---"]

    for prop_name, prop_def in properties.items():
        if "const" in prop_def:
            value = prop_def["const"]
        elif prop_name == "name":
            value = name
        elif prop_name == "version":
            value = '"1.0"'
        elif prop_name == "language":
            value = lang
        elif "enum" in prop_def:
            value = prop_def["enum"][0]
        elif prop_def.get("type") == "array":
            value = "[]"
        else:
            value = '""'

        lines.append(f"{prop_name}: {value}")

    lines.append("---")
    return "\n".join(lines)


def generate_required_sections(schema: dict) -> str:
    sections = schema.get("x-sections", [])
    blocks = []

    for section in sections:
        if section.get("required", False):
            name = section["name"]
            description = section.get("description", "").strip()
            blocks.append(f"# {name}\n\n> {description}")

    return "\n\n".join(blocks)


def generate_optional_sections(schema: dict) -> str:
    sections = schema.get("x-sections", [])
    blocks = []

    for section in sections:
        if not section.get("required", False):
            name = section["name"]
            description = section.get("description", "").strip()
            blocks.append(f"# {name}\n\n> {description}")

    if not blocks:
        return ""

    inner = "\n\n".join(blocks)
    return f"<!-- Optional sections - uncomment if needed:\n\n{inner}\n\n-->"


def main():
    args = parse_args()
    schema = load_schema(args.type)
    front_matter = generate_front_matter(schema, args.name, args.lang)
    required = generate_required_sections(schema)
    optional = generate_optional_sections(schema)

    parts = [front_matter, required]
    if optional:
        parts.append(optional)

    output = "\n\n".join(parts) + "\n"

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"Generated: {out_path}", file=sys.stderr)
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()