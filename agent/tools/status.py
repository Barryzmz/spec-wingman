import re
from pathlib import Path

from tools.utils import validate_project_path

STEPS = [
    ("00-inputs", "Step 0: Inputs"),
    ("01-discovery", "Step 1: Discovery"),
    ("02-requirements", "Step 2: Requirements"),
    ("03-analysis", "Step 3: Analysis"),
    ("04-design-ready", "Step 4: Design Ready"),
    ("05-versions", "Step 5: Versions"),
]

_PLACEHOLDER_VALUES = frozenset({
    "",
    "-",
    "n/a",
    "na",
    "none",
    "open",
    "pending",
    "tbd",
    "todo",
    "yes",
    "no",
})
_ID_PATTERN = re.compile(r"^[A-Z]+-\d+$")
_VERSION_TBD = re.compile(r"^\d+\.\d+\.\d+\s*/\s*TBD$", re.IGNORECASE)
_TABLE_SEPARATOR = re.compile(r"^\|[\s\-:|]+\|$")
_LABEL_PLACEHOLDER = re.compile(
    r"^(?:[-*]\s*)?[^:|]+[:|]\s*(?:TBD|TODO|Pending|Open|N/A|-)?$",
    re.IGNORECASE,
)
_USER_STORY_PLACEHOLDER = re.compile(
    r"^As a TBD,?\s*I want TBD,?\s*so that TBD\.?$",
    re.IGNORECASE,
)
_TEMPLATE_HINTS = (
    "template",
    "fill in",
    "replace this",
    "example:",
    "placeholder",
)


def _cell_has_real_content(cell: str) -> bool:
    value = cell.strip()
    lowered = value.lower()
    return not (
        lowered in _PLACEHOLDER_VALUES
        or _ID_PATTERN.match(value)
        or _VERSION_TBD.match(value)
        or _USER_STORY_PLACEHOLDER.match(value)
        or _LABEL_PLACEHOLDER.match(value)
    )


def _has_substantive_content(filepath: Path) -> bool:
    """Return True when the file contains real data beyond template placeholders."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError:
        return False

    previous_line_was_table_separator = False

    for raw_line in text.splitlines():
        stripped = raw_line.strip()

        if not stripped:
            previous_line_was_table_separator = False
            continue

        if stripped.startswith("#") or stripped.startswith(">"):
            previous_line_was_table_separator = False
            continue

        if _TABLE_SEPARATOR.match(stripped):
            previous_line_was_table_separator = True
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [cell.strip() for cell in stripped.split("|")[1:-1]]
            if previous_line_was_table_separator:
                real_cells = [cell for cell in cells if _cell_has_real_content(cell)]
                if len(real_cells) >= 2:
                    return True
            continue

        previous_line_was_table_separator = False
        content = stripped.lstrip("-* ").strip()
        lowered = content.lower()

        if (
            not content
            or lowered in _PLACEHOLDER_VALUES
            or any(hint in lowered for hint in _TEMPLATE_HINTS)
            or _ID_PATTERN.match(content)
            or _VERSION_TBD.match(content)
            or _LABEL_PLACEHOLDER.match(content)
            or _USER_STORY_PLACEHOLDER.match(content)
        ):
            continue

        return True

    return False


def swm_status_tool(project_path: str) -> str:
    root = validate_project_path(project_path)
    specs_dir = root / "specs"
    lines = ["# SpecWingman Workflow Status", ""]

    for dir_name, label in STEPS:
        step_dir = specs_dir / dir_name
        if not step_dir.exists():
            lines.append(f"[missing] {label} (directory missing)")
            continue

        files = sorted(f for f in step_dir.iterdir() if f.is_file())
        if not files:
            lines.append(f"[empty] {label} (no files)")
            continue

        file_status = {f: _has_substantive_content(f) for f in files}
        content_count = sum(1 for has_content in file_status.values() if has_content)

        if content_count > 0:
            lines.append(f"[content] {label} ({content_count}/{len(files)} with content)")
        else:
            lines.append(f"[template] {label} ({len(files)} files, all template)")

        for file_path in files:
            marker = "[ok]" if file_status[file_path] else "[template]"
            lines.append(f"  {marker} {file_path.name}")

    return "\n".join(lines)
