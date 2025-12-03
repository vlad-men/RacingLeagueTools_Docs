from pathlib import Path

import fitz

PDF_SOURCE = Path(r"c:/Projects/racing_league_tools_randerer_API/FlexRenderer_Manual_Documentation.pdf")
TARGET_DIR = Path("docs/flex-renderer/images")


def _reset_folder() -> None:
    if not TARGET_DIR.exists():
        return
    for item in TARGET_DIR.iterdir():
        if item.is_file():
            item.unlink()


def main() -> None:
    _reset_folder()
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    saved = 0

    with fitz.open(str(PDF_SOURCE)) as doc:
        for page_index, page in enumerate(doc, start=1):
            if page_index == 1:
                continue
            blocks = page.get_text("dict").get("blocks", [])
            image_counter = 0
            for block in blocks:
                if block.get("type") != 1:
                    continue
                xref = block.get("image")
                if xref is None:
                    continue
                try:
                    image = doc.extract_image(xref)
                except ValueError:
                    continue
                data = image.get("image")
                ext = image.get("ext", "png") or "png"
                if not data:
                    continue
                image_counter += 1
                filename = f"page-{page_index:02d}-image-{image_counter:02d}.{ext}"
                (TARGET_DIR / filename).write_bytes(data)
                saved += 1

    print(f"Extracted {saved} images into {TARGET_DIR}")


if __name__ == "__main__":
    main()
