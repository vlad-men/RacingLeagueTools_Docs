# Color

Colors can be defined using hexadecimal strings or numeric RGB/RGBA values.

## Hexadecimal Format

The hexadecimal format is represented as a string, optionally starting with `#`. It can include an alpha channel for opacity.

Format: `"#AARRGGBB"` or `"#RRGGBB"`

Where:

- `#`: Optional prefix.
- `AA`: Hexadecimal value for opacity (Alpha). Optional.
- `RR`: Hexadecimal value for the Red component.
- `GG`: Hexadecimal value for the Green component.
- `BB`: Hexadecimal value for the Blue component.

Examples:

```json
{
  "Color": "#FF010203"
}
```

```json
{
  "Color": "D0A0C0"
}
```

## Numeric Format (RGB/RGBA)

Colors can also be defined using comma-separated decimal numbers (0-255) representing Red, Green, Blue, and optionally Alpha.

Format: `"R, G, B"` or `"R, G, B, A"`

Examples:

```json
{
  "Color": "255, 0, 0"
}
```

```json
{
  "Color": "10, 15, 20, 200"
}
```
