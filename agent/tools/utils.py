from pathlib import Path


def _read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _read_dir(dir_path: Path) -> str:
    if not dir_path.exists():
        return "(no files found)"
    parts = []
    for f in sorted(dir_path.iterdir()):
        if f.is_file():
            parts.append(f"### {f.name}\n\n{f.read_text(encoding='utf-8')}")
    return "\n\n---\n\n".join(parts) if parts else "(no files found)"
