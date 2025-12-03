# Folders Structure

A theme stores all required files in a single folder.

![Theme Folder Structure](../images/page-04-image-01.png)

The default theme is located at `<app_root>/theme_default/`. Do not edit this folder.

Custom themes are placed in `<app_root>/user/themes/`.

## Folder structure of the theme:

- **`theme_description.json`** — required file.
- `layouts/` — required folder that contains layout folders.
- `components/` — reusable blocks.
- `styles/` — global styles (alternative: `styles.json`).
- `vars/` — JSON files that define variables.
- `triggers/` — reusable triggers.
- `fonts/` — font files.
- `globals/` — optional; may contain `global_vars.json` and `public_properties.json`.
- `images/` — main image folder. When a layer references an image, the renderer looks for it in this folder.
- `localizations/` — optional localization files; file names can be custom.

## theme_description.json

- `ThemeId` : restricted string — globally unique identifier. Allowed characters: Latin letters, numbers, `.` and `_`. Required. Use the format `<author>.<theme_name>`. Example: `"ThemeId": "me.my_theme"`.
- `Name` : string — theme name shown in the app UI. Required.
- `Author` : string — required.
- `Description` : string — optional.
- `Version` : restricted string — optional. Recommended format: `"1.0.0"`.
- `DownloadUrl` : string — optional; ZIP file link for the theme.
- `DefaultLocalizationId` : string — optional; default localization id.
- `DisableUnspecifiedLocalization` : boolean — optional; if `true`, requires a specific localization.
- `LogotypeBehaviours` : list of `LogotypeBehaviour` — optional. See [Logotype Variants](./logotypes.md#logotype-variants).
- `RequiredLogotypeVariants` : dictionary — optional. See [Logotype Variants](./logotypes.md#logotype-variants).
- `ForceLiveriesLoading` : boolean — optional.
- `Links` : list of `ThemeLink` — optional; URLs displayed in the app UI. Example:
```json
{
  "Links": [
    {
      "Url": "me.com",
      "Caption": "My site",
      "Type": "SupportAuthor"
    }
  ]
}
```

**ThemeLink** object:

- `Url` : string — required.
- `Caption` : string — required.
- `Type` : string — optional. One of: `General`, `ThemeRepository`, `ThemeIssueReport`, `ThemeDiscussion`, `SupportAuthor`. Default: `General`.
- `Order` : integer — optional; sort order. Default: `0`.
- `RenderCaption` : string — optional; layout caption shown in the app UI. If the string starts with a lowercase letter, "Render " is prefixed automatically.
- `RenderCaptions` : dictionary `<string, object>` — optional; specific captions per render type.

## Layouts example hierarchy (recommended structure)

```text
Theme/
├─ layouts/
│  ├─ calendar/                # layout folder (produces one final image, any name is allowed)
│  │  ├─ layer0-bg.json
│  │  ├─ layer1-main.json
│  │  └─ layout-description.json
│  ├─ race-results/
│  │  ├─ layer0-bg.json
│  │  ├─ layer1-main.json
│  │  └─ layout-description.json
├─ styles.json     # theme-level styles (or styles/ folder)
└─ components/     # optional reusable blocks/components
```

## Short explanation

- Theme — a folder with layout folders, theme-level styles, and optional components.
- Layout folder — contains all JSON files for a single output image (one layout = one final image).
  - `layout-description.json` — layout metadata and layer order.
  - `layer-*.json` — one JSON file per layer. Each layer file starts with `BlockRoot`.
  

  Layer file structure:  


  - The top-level block in a layer file is `BlockRoot` (a container block).
  - `BlockRoot` contains child blocks. Child blocks can be containers with further nesting.