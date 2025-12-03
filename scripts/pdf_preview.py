from pathlib import Path
from pypdf import PdfReader

pdf_path = Path(r"c:/Projects/racing_league_tools_randerer_API/FlexRenderer_Manual_Documentation.pdf")
reader = PdfReader(str(pdf_path))
print(f"Total pages: {len(reader.pages)}")
for page_index in range(min(5, len(reader.pages))):
    page = reader.pages[page_index]
    print("\n" + "=" * 40)
    print(f"PAGE {page_index + 1}")
    print("=" * 40)
    text = page.extract_text() or ""
    print(text)
