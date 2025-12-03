from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

import fitz

PDF_SOURCE = Path(r"c:/Projects/racing_league_tools_randerer_API/FlexRenderer_Manual_Documentation.pdf")
OUTPUT_DIR = Path("docs/flex-renderer/manual")
IMAGES_DIR = Path("docs/flex-renderer/images")
LEGACY_SINGLE_PAGE = Path("docs/flex-renderer/manual.md")

PRIMARY_HEADING_SIZE = 15.5
SECONDARY_HEADING_SIZE = 13.0
LEFT_MARGIN_THRESHOLD = 80.0
LINE_GAP_FACTOR = 0.65
LINE_GAP_MIN = 6.0


@dataclass
class PdfTextLine:
    text: str
    top: float
    bottom: float
    left: float
    size: float
    page_index: int


@dataclass
class PdfImageEvent:
    filename: str
    caption: str
    top: float
    bottom: float
    left: float
    page_index: int


@dataclass
class Section:
    title: str
    slug: str
    lines: List[str] = field(default_factory=list)


@dataclass
class ManualContent:
    preface_lines: List[str]
    sections: List[Section]


PdfEvent = Tuple[str, object]


def _normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u00ad", "").strip())


def _unique_slug(title: str, registry: Dict[str, int]) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "section"
    count = registry.get(slug, 0)
    registry[slug] = count + 1
    return slug if count == 0 else f"{slug}-{count + 1}"


def _clean_image_folder() -> None:
    if not IMAGES_DIR.exists():
        return
    for existing in IMAGES_DIR.iterdir():
        if existing.is_file():
            existing.unlink()


def _entry_sort_key(item: Tuple[str, object]) -> Tuple[float, float]:
    value = item[1]
    if isinstance(value, PdfTextLine):
        return value.top, value.left
    if isinstance(value, dict):
        return float(value.get("top", 0.0)), float(value.get("left", 0.0))
    if isinstance(value, PdfImageEvent):
        return value.top, value.left
    return 0.0, 0.0


def _iter_pdf_content(doc: fitz.Document) -> Iterator[PdfEvent]:
    total_pages = len(doc)
    for page_index in range(1, total_pages + 1):
        if page_index == 1:
            continue

        page = doc[page_index - 1]
        blocks = page.get_text("dict").get("blocks", [])
        entries: List[Tuple[str, object]] = []

        for block in blocks:
            block_type = block.get("type")
            bbox = block.get("bbox") or (0.0, 0.0, 0.0, 0.0)
            block_top = float(bbox[1])
            block_left = float(bbox[0])

            if block_type == 0:
                for line in block.get("lines", []):
                    spans = line.get("spans", [])
                    raw_text = "".join(span.get("text", "") for span in spans)
                    text = _normalize_whitespace(raw_text)
                    if not text:
                        continue
                    lbbox = line.get("bbox") or bbox
                    size_values = [float(span.get("size", 0.0)) for span in spans if span.get("size")]
                    avg_size = sum(size_values) / len(size_values) if size_values else 0.0
                    entries.append(
                        (
                            "text",
                            PdfTextLine(
                                text=text,
                                top=float(lbbox[1]),
                                bottom=float(lbbox[3]),
                                left=float(lbbox[0]),
                                size=avg_size,
                                page_index=page_index,
                            ),
                        )
                    )
            elif block_type == 1:
                entries.append(
                    (
                        "image",
                        {
                            "block": block,
                            "top": block_top,
                            "bottom": float(bbox[3]),
                            "left": block_left,
                            "page_index": page_index,
                        },
                    )
                )

        entries.sort(key=_entry_sort_key)
        image_counter = 0

        for kind, data in entries:
            if kind == "text":
                yield "text", data
            else:
                block_info = data  # type: ignore[assignment]
                block = block_info["block"]  # type: ignore[index]
                raw_image = block.get("image")
                if raw_image is None:
                    continue

                ext = (block.get("ext") or "png").lower()
                if isinstance(raw_image, bytes):
                    image_bytes = raw_image
                else:
                    try:
                        image = doc.extract_image(int(raw_image))
                    except (TypeError, ValueError):
                        continue
                    image_bytes = image.get("image") or b""
                    ext = (image.get("ext") or ext or "png").lower()

                if not image_bytes:
                    continue

                image_counter += 1
                filename = f"page-{page_index:02d}-image-{image_counter:02d}.{ext}"
                target_path = IMAGES_DIR / filename
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_bytes(image_bytes)

                yield "image", PdfImageEvent(
                    filename=filename,
                    caption=f"Page {page_index:02d} Image {image_counter:02d}",
                    top=float(block_info.get("top", 0.0)),
                    bottom=float(block_info.get("bottom", 0.0)),
                    left=float(block_info.get("left", 0.0)),
                    page_index=page_index,
                )

        if page_index != total_pages:
            yield "page_break", {"page_index": page_index}


def _finalize_lines(lines: List[str]) -> List[str]:
    cleaned: List[str] = []
    for line in lines:
        if line == "" and cleaned and cleaned[-1] == "":
            continue
        cleaned.append(line)
    while cleaned and cleaned[-1] == "":
        cleaned.pop()
    return cleaned


def _write_markdown(path: Path, lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(_finalize_lines(lines)) + "\n"
    path.write_text(content, encoding="utf-8")


def normalize_text() -> ManualContent:
    preface_lines: List[str] = [
        "# Flex Renderer Manual",
        "",
        "**Version 0.9.6**",
        "",
        "> Converted from the original Flex Renderer manual (PDF) provided with the Racing League Tools application.",
        "",
    ]

    sections: List[Section] = []
    current_section: Optional[Section] = None
    slug_registry: Dict[str, int] = {}

    paragraph = ""
    bullet_stack: List[str] = []
    prev_was_blank = True
    prev_line: Optional[Dict[str, float]] = None

    def target_lines() -> List[str]:
        return preface_lines if current_section is None else current_section.lines

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            target_lines().append(paragraph)
            target_lines().append("")
            paragraph = ""

    def flush_bullets() -> None:
        if bullet_stack:
            target_lines().extend(bullet_stack)
            target_lines().append("")
            bullet_stack.clear()

    def start_section(title: str) -> None:
        nonlocal current_section, prev_was_blank, prev_line
        flush_bullets()
        flush_paragraph()
        if current_section is not None:
            current_section.lines = _finalize_lines(current_section.lines)
            sections.append(current_section)
        current_section = Section(title=title, slug=_unique_slug(title, slug_registry))
        prev_was_blank = True
        prev_line = None

    _clean_image_folder()

    with fitz.open(str(PDF_SOURCE)) as doc:
        for kind, payload in _iter_pdf_content(doc):
            if kind == "text":
                info = payload  # type: ignore[assignment]
                line_text = info.text
                if not line_text:
                    continue

                size = float(info.size)
                left = float(info.left)

                if prev_line and info.page_index == prev_line["page_index"]:
                    gap = info.top - prev_line["bottom"]
                    threshold = max(LINE_GAP_MIN, max(size, prev_line.get("size", 0.0)) * LINE_GAP_FACTOR)
                    if gap > threshold:
                        flush_bullets()
                        flush_paragraph()
                        prev_was_blank = True

                if size >= PRIMARY_HEADING_SIZE and left <= LEFT_MARGIN_THRESHOLD:
                    start_section(line_text)
                    prev_was_blank = True
                    continue

                if size >= SECONDARY_HEADING_SIZE and left <= LEFT_MARGIN_THRESHOLD:
                    flush_bullets()
                    flush_paragraph()
                    target_lines().append(f"## {line_text}")
                    target_lines().append("")
                    prev_was_blank = True
                    prev_line = None
                    continue

                bullet_match = re.match(r"^[\u2022\-]\s*(.+)", line_text)
                if bullet_match:
                    flush_paragraph()
                    bullet_text = bullet_match.group(1)
                    if bullet_text:
                        bullet_stack.append(f"- {bullet_text}")
                    prev_was_blank = False
                    prev_line = {
                        "page_index": info.page_index,
                        "bottom": info.bottom,
                        "size": size,
                    }
                    continue

                numbered_match = re.match(r"^(\d+\.?)(\s+)(.+)", line_text)
                if numbered_match and not paragraph:
                    flush_bullets()
                    marker, _, content = numbered_match.groups()
                    prefix = marker if marker.endswith(".") else f"{marker}."
                    bullet_stack.append(f"{prefix} {content}")
                    prev_was_blank = False
                    prev_line = {
                        "page_index": info.page_index,
                        "bottom": info.bottom,
                        "size": size,
                    }
                    continue

                if bullet_stack:
                    bullet_stack[-1] += f" {line_text}"
                    prev_was_blank = False
                    prev_line = {
                        "page_index": info.page_index,
                        "bottom": info.bottom,
                        "size": size,
                    }
                    continue

                if paragraph:
                    if paragraph.endswith(("-", "–")):
                        paragraph = paragraph[:-1] + line_text
                    else:
                        paragraph += " " + line_text
                else:
                    paragraph = line_text

                prev_was_blank = False
                prev_line = {
                    "page_index": info.page_index,
                    "bottom": info.bottom,
                    "size": size,
                }

            elif kind == "image":
                image_info: PdfImageEvent = payload  # type: ignore[assignment]
                flush_bullets()
                flush_paragraph()
                target_lines().append(f"![{image_info.caption}](../images/{image_info.filename})")
                target_lines().append("")
                prev_was_blank = True
                prev_line = None

            elif kind == "page_break":
                flush_bullets()
                flush_paragraph()
                prev_was_blank = True
                prev_line = None

    flush_bullets()
    flush_paragraph()

    if current_section is not None:
        current_section.lines = _finalize_lines(current_section.lines)
        sections.append(current_section)

    preface_lines_final = _finalize_lines(preface_lines)

    return ManualContent(preface_lines=preface_lines_final, sections=sections)


def main() -> None:
    manual = normalize_text()

    if OUTPUT_DIR.exists():
        for existing in OUTPUT_DIR.glob("*.md"):
            existing.unlink()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if LEGACY_SINGLE_PAGE.exists():
        LEGACY_SINGLE_PAGE.unlink()

    index_lines = manual.preface_lines[:]
    if manual.sections:
        index_lines.append("## Contents")
        index_lines.append("")
        for section in manual.sections:
            index_lines.append(f"- [{section.title}](./{section.slug}.md)")
        index_lines.append("")

    _write_markdown(OUTPUT_DIR / "index.md", index_lines)

    for section in manual.sections:
        section_lines = [f"# {section.title}", ""] + section.lines
        _write_markdown(OUTPUT_DIR / f"{section.slug}.md", section_lines)


if __name__ == "__main__":
    main()
