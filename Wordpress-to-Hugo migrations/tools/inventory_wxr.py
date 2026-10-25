#!/usr/bin/env python3
"""Create a private metadata inventory from a WordPress WXR XML export.

This local-only helper does not import content, contact a server, or write post
bodies, comment text, author names/emails, or credentials to the report.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from xml.parsers import expat
from collections import Counter
from pathlib import Path

COLUMNS = [
    "wordpress_id",
    "content_type",
    "status",
    "title",
    "slug",
    "source_url",
    "published_at",
    "modified_at",
    "parent_id",
    "featured_media_id",
    "attached_file",
    "upload_reference_count",
    "comment_count",
]
UPLOAD_RE = re.compile(r"wp-content/uploads/[^\"'\s<>)]*", re.IGNORECASE)
ROOT_RE = re.compile(rb"<(?:[A-Za-z_][\w.-]*:)?rss(?:\s|>)", re.IGNORECASE)
DTD_RE = re.compile(rb"<!\s*(?:DOCTYPE|ENTITY)\b", re.IGNORECASE)


def open_export(path: Path):
    return gzip.open(path, "rb") if path.suffix.lower() == ".gz" else path.open("rb")


def validate_wxr(path: Path) -> None:
    """Reject DTDs and verify the XML document has an rss root."""
    parser = expat.ParserCreate()
    root_seen = False

    def check_root(name: str, _attrs: dict[str, str]) -> None:
        nonlocal root_seen
        if not root_seen:
            root_seen = True
            if name.rsplit(":", 1)[-1].lower() != "rss":
                raise ValueError("The XML document root is not a WXR rss element")

    def reject_doctype(*_args: object) -> None:
        raise ValueError("WXR DTD/entity declarations are not accepted")

    parser.StartElementHandler = check_root
    parser.StartDoctypeDeclHandler = reject_doctype
    parser.EntityDeclHandler = reject_doctype
    parser.ExternalEntityRefHandler = lambda *_args: 0

    try:
        with open_export(path) as stream:
            parser.ParseFile(stream)
    except expat.ExpatError as exc:
        raise ValueError("The input is not a well-formed WordPress WXR XML export") from exc

    if not root_seen:
        raise ValueError("The XML document has no root element")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].split(":")[-1]


def child_text(item: ET.Element, name: str) -> str:
    for element in item.iter():
        if local_name(element.tag) == name:
            return (element.text or "").strip()
    return ""


def item_metadata(item: ET.Element) -> dict[str, str] | None:
    post_type = child_text(item, "post_type")
    if not post_type or post_type in {"revision", "nav_menu_item"}:
        return None

    encoded_content = child_text(item, "encoded")
    uploads = set(UPLOAD_RE.findall(encoded_content))
    comments = sum(1 for element in item.iter() if local_name(element.tag) == "comment")

    return {
        "wordpress_id": child_text(item, "post_id"),
        "content_type": post_type,
        "status": child_text(item, "status"),
        "title": child_text(item, "title"),
        "slug": child_text(item, "post_name"),
        "source_url": child_text(item, "link"),
        "published_at": child_text(item, "post_date"),
        "modified_at": child_text(item, "post_modified"),
        "parent_id": child_text(item, "post_parent"),
        "featured_media_id": child_text(item, "_thumbnail_id"),
        "attached_file": child_text(item, "_wp_attached_file"),
        "upload_reference_count": str(len(uploads)),
        "comment_count": str(comments),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path, help="Local WordPress WXR .xml or .xml.gz export")
    parser.add_argument("output", type=Path, help="Private CSV output path; do not commit or upload it")
    parser.add_argument("--force", action="store_true", help="Allow replacing an existing output CSV")
    args = parser.parse_args()

    source = args.export.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not source.is_file():
        raise ValueError("Input export file does not exist")
    if source == output:
        raise ValueError("Input and output paths must be different")
    if output.exists() and not args.force:
        raise ValueError("Output already exists; choose another path or pass --force")
    output.parent.mkdir(parents=True, exist_ok=True)

    validate_wxr(source)
    totals: Counter[str] = Counter()
    row_count = 0
    temporary_output: Path | None = None
    try:
        with open_export(source) as stream:
            with tempfile.NamedTemporaryFile(
                mode="w",
                newline="",
                encoding="utf-8-sig",
                dir=output.parent,
                prefix=f".{output.name}.",
                suffix=".tmp",
                delete=False,
            ) as report:
                temporary_output = Path(report.name)
                writer = csv.DictWriter(report, fieldnames=COLUMNS, extrasaction="ignore")
                writer.writeheader()
                for _, element in ET.iterparse(stream, events=("end",)):
                    if local_name(element.tag) != "item":
                        continue
                    record = item_metadata(element)
                    if record is not None:
                        writer.writerow(record)
                        totals[record["content_type"]] += 1
                        row_count += 1
                    element.clear()
    except BaseException as exc:
        if temporary_output is not None:
            temporary_output.unlink(missing_ok=True)
        if isinstance(exc, ET.ParseError):
            raise ValueError("The input is not a readable WordPress WXR export") from exc
        raise

    if row_count == 0:
        if temporary_output is not None:
            temporary_output.unlink(missing_ok=True)
        raise ValueError("No WordPress content records were found in the WXR export")

    if temporary_output is None:
        raise ValueError("The inventory report could not be created")
    try:
        os.replace(temporary_output, output)
    finally:
        temporary_output.unlink(missing_ok=True)

    summary = ", ".join(f"{kind}={count}" for kind, count in sorted(totals.items()))
    print(f"Wrote {row_count} metadata rows ({summary}) to {output.name}")
    print("Keep this inventory private; it may contain unpublished titles, URLs, and media paths.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        print(f"Inventory failed: {error}", file=sys.stderr)
        raise SystemExit(1)
