# Theme Resources

Custom themes must not use resources from the default theme (fonts, images, and other content located in `%app_root%/theme_default`). **All required resources for a custom theme must be inside the theme folder.**

An exception is `flags`, `logos`, and `badges` that are placed in `%app_root%/images`. Access to those resources is through object properties, such as `LogotypePath`.

## Supported File Types

- Images: `png`, `jpg`, `jpeg`.
- Fonts: `ttf`, `otf`.

## Images

To link to an image:

1. Place the image in the theme images folder. It possible to use subfolders; for example, place the image at `%theme_folder%/images/bg/light_bg.png`.

2. Specify the path relative to the `%theme_folder%/images` folder. Example JSON:

```json
{
	"Path": "bg/light_bg.png"
}
```

## Fonts

To link to a font:

1. Place the font file inside `%theme_folder%/fonts`. For example: `%theme_folder%/fonts/f1font.ttf`.

2. Specify the font by file name without an extension. Example JSON:

```json
{
	"FontName": "f1font"
}
```

You can use system fonts by specifying the system font name. Example:

```json
{
	"FontName": "Arial"
}
```

## Notes

- Use simple relative paths and backticks for paths and file names in documentation.
- Keep theme assets inside the theme folder unless they are flags, logos, or badges held in `%app_root%/images`.
