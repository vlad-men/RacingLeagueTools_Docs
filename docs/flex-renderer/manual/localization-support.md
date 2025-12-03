# Localization Support

To include specific localizations, create JSON files in the `%theme_folder%/localizations/` folder. The filename is custom.

![Localizations folder structure](../images/page-53-image-01.png)

## Localization File Structure

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `Id` | `string` | Yes | Locale identifier. Recommended to use standard codes such as `en-US`, `fr-FR`. |
| `Name` | `string` | Yes | Localization name displayed in the UI. |
| `Strings` | `Dictionary<string, string>` | No | Key-value pairs for text substitution. |
| `Vars` | `Dictionary<string, object>` | No | Variables where object can be `string`, `number`, `bool`, or `color`. |

Example:

![Localization file example](../images/page-53-image-02.png)

## Using Localization Strings

Localization strings automatically substitute text in the markup. Any text enclosed in square brackets (`[`, `]`) is marked for localization. The renderer searches for matching text as a key in the `Strings` dictionary of the current localization file.

Source markup example:

![Source markup](../images/page-53-image-03.png)

If `german.json` is selected:

![German localization file](../images/page-53-image-04.png)

The source converts to:

![Converted result](../images/page-54-image-01.png)

If the required string is not found in the localization file, the square brackets are removed:

![Missing string behavior](../images/page-54-image-02.png)

## Localization Variables

Localization vars are added to the common list of variables using the override mechanism. See [Variables](variables.md) and [Expressions](expressions.md) for details.

## Theme Description Properties

The `theme_description.json` file can optionally define the following localization properties:

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `DefaultLocalizationId` | `string` | No | Specifies the default localization. |
| `DisableUnspecifiedLocalization` | `bool` | No | When `true`, disables the "default, not specified" option in the localization list. |

**Note:** By default, the renderer allows using a theme without selecting any localization. Set `DisableUnspecifiedLocalization` to `true` to require a localization selection.