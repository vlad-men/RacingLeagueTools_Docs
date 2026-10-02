# Liveries

Liveries are image files associated with a specific team or car.

## File Locations

Livery files must be located in one of the following folders:

- `<app_root>/images/liveries` - Default liveries.
- `<app_root>/user/images/liveries` - User liveries.
- `<theme_folder>/images/liveries` - Theme liveries.

The internal folder hierarchy can be defined freely. Liveries located in the theme folder have the highest priority. Only `.png` images are supported.

## Naming Convention

The livery filename must match the unique Team ID or Car ID.

Examples:

- `red.bull.2023.png`
- `bmw.m4gt3.png`

### Team and Car Pair

A livery can be bound to a team and a car together. The filename format is:

```text
{teamName}__{carUniqueName}.png
```

Example: `alfa__ferrari.499p.png`.

For `{teamName}`, the application tries these values in order: team `UniqueName`, then `Name`, then `Origin` (the same priority as team logos). Teams that share a name or origin and use the same car pick up the same file. Added in 0.9.9.

When both a team and a car are known, the application resolves liveries in this order: team-and-car pair, then the team set, then the car set.

### Variants

Additional livery variants for the same team, car, or team-and-car pair are supported. To add a variant, use the following naming format:

```text
{id}.{prefix}.png
```

Examples:

- `red.bull.2023.v2.png`
- `alfa__ferrari.499p.wet.png`

Specific livery variants can be selected for a driver on the application's line-ups page. A manual selection on the line-ups page overrides the automatic choice inside the resolved set.

## Data Integration

Render data objects automatically provide the path to the livery file. Supported objects include:

- `TeamRenderData`
- `CarRenderData`
- `DriverSessionRenderData`
- `DriverSeasonRenderData`

## Configuration

To load and display liveries in the UI, the **Enable liveries support** option must be enabled in the application settings. This option is disabled by default.

If a theme uses liveries in its code, the `ForceLiveriesLoading` option must be set to `true` in the `theme_description.json` file.
