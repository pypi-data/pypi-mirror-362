import re
import click
from pathlib import Path

SENSITIVE_KEYWORDS = ["KEY", "SECRET", "TOKEN", "PASSWORD", "URL"]

def is_sensitive_key(key: str) -> bool:
    return any(keyword in key.upper() for keyword in SENSITIVE_KEYWORDS)

def redact_line(line: str) -> str:
    if line.strip().startswith("#") or "=" not in line:
        return line
    key, value = line.split("=", 1)
    if is_sensitive_key(key.strip()):
        return f"{key}=***REDACTED***\n"
    return line

@click.command()
@click.argument("input_file", default=".env")
@click.argument("output_file", default=".env.redacted")
def redact_env(input_file, output_file):
    """Redacts secrets in a .env file."""
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        click.echo(f"❌ File not found: {input_path}")
        return

    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    redacted_lines = [redact_line(line) for line in lines]

    with output_path.open("w", encoding="utf-8") as f:
        f.writelines(redacted_lines)

    click.echo(f"✅ Redacted file written to {output_path}")
