#!/usr/bin/env python3
"""Generate a static resume portfolio site from the bundled template.

The script intentionally stays simple: it copies the HTML/CSS/JS template,
applies literal text replacements, and swaps assets. For larger design changes,
edit the generated site after running this script.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


TEXT_EXTENSIONS = {".html", ".css", ".js", ".json", ".toml", ".md", ".txt"}


def load_profile(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def copy_template(template_dir: Path, output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    shutil.copytree(template_dir, output_dir)


def apply_replacements(output_dir: Path, replacements: dict[str, str]) -> None:
    if not replacements:
        return

    for file_path in output_dir.rglob("*"):
        if not file_path.is_file() or file_path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        text = file_path.read_text(encoding="utf-8")
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(str(old), str(new))

        if updated != text:
            file_path.write_text(updated, encoding="utf-8")


def replace_asset_references(output_dir: Path, old_relative: str, new_relative: str) -> None:
    if old_relative == new_relative:
        return

    old_name = Path(old_relative).name
    new_name = Path(new_relative).name
    for file_path in output_dir.rglob("*"):
        if not file_path.is_file() or file_path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        text = file_path.read_text(encoding="utf-8")
        updated = text.replace(old_relative, new_relative).replace(old_name, new_name)
        if updated != text:
            file_path.write_text(updated, encoding="utf-8")


def copy_assets(output_dir: Path, assets: dict[str, str]) -> None:
    for relative_target, source in assets.items():
        if not source or str(source).startswith("/absolute/path/"):
            continue

        source_path = Path(source).expanduser()
        if not source_path.exists():
            raise FileNotFoundError(f"Asset does not exist: {source_path}")

        target_path = output_dir / relative_target
        if source_path.suffix and source_path.suffix.lower() != target_path.suffix.lower():
            target_path = target_path.with_suffix(source_path.suffix.lower())
            replace_asset_references(output_dir, relative_target, str(Path(relative_target).with_suffix(source_path.suffix.lower())))
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a resume portfolio static site.")
    parser.add_argument("--profile", required=True, type=Path, help="Path to profile JSON.")
    parser.add_argument("--output", required=True, type=Path, help="Output directory.")
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "site-template",
        help="Template directory. Defaults to the bundled template.",
    )
    args = parser.parse_args()

    profile = load_profile(args.profile)
    copy_template(args.template, args.output)
    apply_replacements(args.output, profile.get("replacements", {}))
    copy_assets(args.output, profile.get("assets", {}))

    print(f"Generated site: {args.output.resolve()}")
    print("Open index.html locally or deploy the output directory to GitHub Pages / Netlify.")


if __name__ == "__main__":
    main()
