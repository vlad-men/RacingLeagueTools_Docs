# Program Help Center

This repository contains an MkDocs project that delivers the end-user help site for the Program application. The site is meant to be easy to maintain and publish, while providing clear guidance for non-technical users.

## Getting started

1. **Install Python 3.8+** if it is not already on your system.
2. **Create and activate a virtual environment (recommended):**
   ```cmd
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
   After you change or upgrade your system Python, delete `.venv` and rerun the commands with the new interpreter so the helper script can bootstrap itself without errors.
3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```
4. **Start the live-reload preview server:**
   ```cmd
   serve-docs.bat
   ```
   The script now auto-rebuilds `.venv` (using the currently installed Python via the `py` launcher or `python`) and installs requirements if they are missing, keeping the workflow smooth after Python upgrades.
5. Open your browser to http://127.0.0.1:8000/ to see the documentation.

## Project layout

```
mkdocs.yml        # Site configuration
serve-docs.bat    # Helper script to serve the site locally (Windows)
requirements.txt  # Python dependencies
/docs              # Markdown content
```

## Next steps

- Update the placeholder pages in `docs/` with real help content.
- Add new pages by creating Markdown files and referencing them in `mkdocs.yml` under the `nav` section.
- Customize the theme or add MkDocs plugins as needed.

