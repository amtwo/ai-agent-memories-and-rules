#!/usr/bin/env python3
"""Create a private metadata inventory from a WordPress WXR XML export.

This local-only helper does not import content, contact a server, or write post
bodies, comment text, author names/emails, or credentials to the report.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import re
import sys
import xml.etree.ElementTree as ET
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
CONTENT_SUFFIXES = {".md", ".markdown", ".html", ".htm", ".txt"}
UPLOAD_RE = re.compile(r"wp-content/uploads/[^\"'\s<>)]*", re.IGNORECASE)
ROOT_RE = re.compile(rb"<(?:[A-Za-z_][\w.-]*:)?rss(?:\s|>)", re.IGNORECASE)
DTD_RE = re.compile(rb"<!\s*(?:DOCTYPE|ENTITY)\b", re.IGNORECASE)


def open_export(path: Path):
    return gzip.open(path, "rb") if path.suffix.lower() == ".gz" else path.open("rb")


def reject_dtd(path: Path) -> None:
    """Reject DTD/entity declarations before the WXR document root."""
    with open_export(path) as stream:
        prefix = bytearray()
        while len(prefix) < 1_048_576:
            chunk = stream.read(16_384)
            if not chunk:
                break
            prefix.extend(chunk)
            match = ROOT_RE.search(prefix)
            if match:
                if DTD_RE.search(prefix[:match.start()]):
                    raise ValueError("WXR DTD/entity declarations are not accepted")
                return
        raise ValueError("Could not find a WXR rss root element near the start of the export")


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

    reject_dtd(source)
    totals: Counter[str] = Counter()
    row_count = 0
    with open_export(source) as stream, output.open("w", newline="", encoding="utf-8-sig") as report:
        writer = csv.DictWriter(report, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        try:
            for _, element in ET.iterparse(stream, events=("end",)):
                if local_name(element.tag) != "item":
                    continue
                record = item_metadata(element)
                if record is not None:
                    writer.writerow(record)
                    totals[record["content_type"]] += 1
                    row_count += 1
                element.clear()
        except ET.ParseError as exc:
            output.unlink(missing_ok=True)
            raise ValueError("The input is not a readable WordPress WXR export") from exc

    if row_count == 0:
        output.unlink(missing_ok=True)
        raise ValueError("No WordPress content records were found in the WXR export")

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
