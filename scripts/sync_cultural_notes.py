#!/usr/bin/env python3
"""Sync Cultural Notes from an Obsidian vault into Quartz without copying tags or embeds."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

TAG_PATTERN = re.compile(r"(?<!\S)#(?!\s)[^\s#]+")
EMBED_PATTERN = re.compile(r"!\[\[[^\]]+\]\]")


def filter_content(raw: str) -> str:
    """Strip Obsidian tags (#tag) and embeds (![[...]]) while leaving other text intact."""
    filtered_lines = []
    for line in raw.splitlines():
        no_embeds = EMBED_PATTERN.sub("", line)
        no_tags = TAG_PATTERN.sub("", no_embeds)
        filtered_lines.append(no_tags)

    trailing_newline = raw.endswith("\n")
    result = "\n".join(filtered_lines)
    if trailing_newline:
        result += "\n"
    return result


def find_source(rel_path: Path, source_root: Path, target_root: Path) -> Path | None:
    """Return the matching source path if it exists; try both direct and nested folders."""
    direct = source_root / rel_path
    if direct.is_file():
        return direct

    alternative = source_root / target_root.name / rel_path
    if alternative.is_file():
        return alternative

    return None


def resolve_target_files(target_dir: Path, specific: str | None) -> list[Path]:
    """Return markdown files to sync, restricted to a specific file if provided."""
    if specific is None:
        return [p for p in target_dir.rglob("*.md") if p.is_file()]

    candidate = Path(specific)
    if not candidate.is_absolute():
        candidate = target_dir / candidate

    try:
        candidate = candidate.resolve()
    except FileNotFoundError:
        print(f"File not found: {specific}")
        return []

    try:
        candidate.relative_to(target_dir)
    except ValueError:
        print(f"Specified file is outside the target directory: {candidate}")
        return []

    if not candidate.is_file():
        print(f"File not found: {candidate}")
        return []

    if candidate.suffix.lower() != ".md":
        print(f"Not a Markdown file: {candidate}")
        return []

    return [candidate]


def main(target_dir: Path, source_dir: Path, dry_run: bool, specific_file: str | None) -> None:
    updated = 0
    skipped = 0

    target_files = resolve_target_files(target_dir, specific_file)
    if not target_files:
        print("No matching Markdown files to sync.")
        return

    for target_path in target_files:
        if not target_path.is_file():
            continue

        rel_path = target_path.relative_to(target_dir)
        source_path = find_source(rel_path, source_dir, target_dir)
        if source_path is None:
            skipped += 1
            continue

        source_text = source_path.read_text(encoding="utf-8")
        filtered = filter_content(source_text)
        current_text = target_path.read_text(encoding="utf-8")

        if filtered == current_text:
            continue

        if dry_run:
            print(f"[dry-run] would update {target_path} from {source_path}")
            continue

        target_path.write_text(filtered, encoding="utf-8")
        print(f"Updated {target_path} from {source_path}")
        updated += 1

    print(f"Done. Updated {updated} file(s); skipped {skipped} without matches.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Sync matching Markdown files from an Obsidian vault into Quartz, "
            "dropping #tags and ![[embeds]]."
        )
    )
    parser.add_argument(
        "--target-dir",
        default=(
            "/Users/xzhang/Documents/projects/obsidian/test-quartz/quartz/"
            "content/Cultural Notes"
        ),
        type=Path,
        help="Quartz directory to update (default: Cultural Notes folder).",
    )
    parser.add_argument(
        "--source-dir",
        default="/Users/xzhang/Documents/projects/obsidian/my-vault",
        type=Path,
        help="Obsidian vault root to read from.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which files would change without writing anything.",
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Specific Markdown file (relative or absolute path) under the target directory to sync.",
    )
    args = parser.parse_args()

    main(
        args.target_dir.resolve(),
        args.source_dir.resolve(),
        args.dry_run,
        args.file,
    )
