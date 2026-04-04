# Tyre Types

Racing League Tools supports a wide range of built-in tyre compound types covering all major motorsport categories (Formula 1, endurance racing, rally, karting, and more). Each league can also customise compound display names, abbreviations, or introduce entirely new compound types — without any application update required.

---

## Built-in Tyre Types

The tables below list all built-in tyre types, their identifiers, default abbreviations, and display names. The abbreviation and name of any built-in type can be overridden per league via the custom configuration described in the next section.

### Standard Compounds

| Identifier | Default Abbreviation | Default Display Name | Notes |
| --- | --- | --- | --- |
| `Soft` | S | Soft | Standard F1-style soft tyre |
| `Medium` | M | Medium | |
| `Hard` | H | Hard | |
| `Intermediate` | I | Intermediate | Bridging wet/dry compound |
| `Wet` | W | Wet | Full wet weather tyre |

### Soft Variants

| Identifier | Default Abbreviation | Default Display Name |
| --- | --- | --- |
| `SuperSoft` | SS | Super Soft |
| `UltraSoft` | US | Ultra Soft |
| `HyperSoft` | HS | Hyper Soft |

### Pirelli C-Compounds (2019+ Formula 1)

| Identifier | Default Abbreviation | Default Display Name |
| --- | --- | --- |
| `C1` | C1 | C1 |
| `C2` | C2 | C2 |
| `C3` | C3 | C3 |
| `C4` | C4 | C4 |
| `C5` | C5 | C5 |
| `C6` | C6 | C6 |

### Generic / Alternative Compounds

| Identifier | Default Abbreviation | Default Display Name | Notes |
| --- | --- | --- | --- |
| `Option` | O | Option | Alternative compound |
| `Prime` | P | Prime | Primary compound |
| `Qualifying` | Q | Qualifying | Special qualifying-only tyre |

### Surface-Specific Tyres

| Identifier | Default Abbreviation | Default Display Name | Notes |
| --- | --- | --- | --- |
| `Slick` | SL | Slick | Dry weather racing tyre |
| `Rain` | R | Rain | Wet surface tyre |
| `Snow` | SN | Snow | Snow / ice conditions |
| `Gravel` | G | Gravel | Gravel surfaces |
| `Mud` | MU | Mud | Muddy conditions |
| `Sand` | SA | Sand | Sandy terrain |
| `AllTerrain` | AT | All Terrain | |

### Street / Mixed Surface Tyres

| Identifier | Default Abbreviation | Default Display Name |
| --- | --- | --- |
| `SemiSlick` | SM | Semi Slick |
| `Street` | ST | Street |
| `StreetVintage` | SV | Street Vintage |

### All-Weather

| Identifier | Default Abbreviation | Default Display Name | Notes |
| --- | --- | --- | --- |
| `AllWeather` | AW | All Weather | Used in Formula E and similar |

### Custom Slots

Nine reserved slots are available for league-defined tyre types. These are used when a custom entry uses a `Type` value that does not match any built-in identifier (see [Custom Tyre Types](#custom-tyre-types) below).

| Identifier | Default Abbreviation | Default Display Name |
| --- | --- | --- |
| `Custom1` | U1 | Custom 1 |
| `Custom2` | U2 | Custom 2 |
| `Custom3` | U3 | Custom 3 |
| `Custom4` | U4 | Custom 4 |
| `Custom5` | U5 | Custom 5 |
| `Custom6` | U6 | Custom 6 |
| `Custom7` | U7 | Custom 7 |
| `Custom8` | U8 | Custom 8 |
| `Custom9` | U9 | Custom 9 |

---

## Custom Tyre Types

The system supports two operations:

1. **Override** the display metadata (abbreviation and/or name) of any built-in tyre type.
2. **Add** entirely new compound types — up to **9** new types per league.

Both operations are performed by adding a JSON configuration entry to the league database. No recompilation or application update is required.

### How to Configure

Custom tyre types are stored as a JSON string in the **`LeagueSettings`** table of the league SQLite database. The recommended tool for editing the database directly is **DB Browser for SQLite**.

1. Open the league database file (`.db` or `.sqlite`) in DB Browser for SQLite.
2. Navigate to the **`LeagueSettings`** table (Browse Data tab).
3. Add a new row:
    - **Name**: `LeagueCustomTyreTypesJson`
    - **Type**: `String`
    - **Value**: a JSON array (see format below).
4. Save and close the database.
5. Restart Racing League Tools — the new tyre types will be loaded at startup.

!!! note
    If a `LeagueCustomTyreTypesJson` row already exists, edit its **Value** field rather than adding a duplicate row.

### JSON Format

The value must be a **JSON array** of objects. Each object represents one tyre type entry.

```json
[
  {
    "Id": 1,
    "Type": "Pirelli",
    "Abbreviation": "P",
    "Name": "Pirelli Tyres"
  },
  {
    "Id": 2,
    "Type": "Bridgestone",
    "Abbreviation": "BS"
  }
]
```

#### Field Reference

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `Id` | `integer` | No | Controls sort order when assigning custom slots. Entries are processed in ascending `Id` order. Defaults to `0` if omitted. |
| `Type` | `string` | Yes | Compound identifier. Must contain only basic ASCII letters and digits — no spaces, no special characters. Case-sensitive match against built-in enum names. |
| `Abbreviation` | `string` | Yes | Short label shown in race result tables, standings, and graphics. Maximum **2 characters**. If empty or longer than 2 characters, the default abbreviation is used instead. |
| `Name` | `string` | No | Full display name used in tooltips and detailed views. If omitted or empty, the default name is used. |

### How Type Mapping Works

When the configuration is loaded, each entry's `Type` value is compared against built-in identifiers:

- **Match found** (e.g. `"Type": "Soft"`): The entry **overrides** the abbreviation and/or name for that built-in type.
- **No match** (e.g. `"Type": "Pirelli"`): The entry is registered as a new compound type, assigned to the next available custom slot (`Custom1`–`Custom9`) in ascending `Id` order.

This means:

- Any number of built-in types can be overridden.
- At most **9 brand-new** compound names can be defined per league.

### Examples

#### Example 1 — Override Built-in Type Labels

Rename the standard compounds to use manufacturer-specific names:

```json
[
  {
    "Type": "Soft",
    "Abbreviation": "S",
    "Name": "Pirelli P Zero Soft"
  },
  {
    "Type": "Medium",
    "Abbreviation": "M",
    "Name": "Pirelli P Zero Medium"
  },
  {
    "Type": "Hard",
    "Abbreviation": "H",
    "Name": "Pirelli P Zero Hard"
  },
  {
    "Type": "Intermediate",
    "Abbreviation": "I",
    "Name": "Pirelli Cinturato Intermediate"
  },
  {
    "Type": "Wet",
    "Abbreviation": "W",
    "Name": "Pirelli Cinturato Wet"
  }
]
```

#### Example 2 — Add Entirely New Compound Types

Define custom tyre brands as new compounds (occupies the first two available custom slots):

```json
[
  {
    "Id": 1,
    "Type": "Pirelli",
    "Abbreviation": "P",
    "Name": "Pirelli Tyres"
  },
  {
    "Id": 2,
    "Type": "Bridgestone",
    "Abbreviation": "BS",
    "Name": "Bridgestone Tyres"
  }
]
```

#### Example 3 — Mix Overrides and New Types

```json
[
  {
    "Id": 0,
    "Type": "Option",
    "Abbreviation": "OP",
    "Name": "Option Compound"
  },
  {
    "Id": 1,
    "Type": "MyCoolTyre",
    "Abbreviation": "CT",
    "Name": "My Custom Tyre"
  }
]
```

Here `Option` (a built-in type) gets its display overridden, and `MyCoolTyre` becomes a new compound type assigned to `Custom1`.

---

## UI Behaviour

### Tyre Icons

The following built-in types have dedicated graphical icons: Soft, Medium, Hard, Intermediate, Wet, Super Soft, Ultra Soft, and Hyper Soft. All other types — including all custom types — display the **abbreviation text** as a badge instead.

### Tyre Colour Coding

The UI applies colour-coded backgrounds to tyre type indicators following standard Formula 1 visual conventions:

| Tyre Type(s) | Colour | Value |
| --- | --- | --- |
| Soft | Red | `rgb(255, 55, 55)` |
| Medium | Yellow / Gold | `rgb(255, 215, 0)` |
| Hard | White | `rgb(255, 255, 255)` |
| Intermediate | Green | `rgb(0, 180, 0)` |
| Wet / Rain | Blue | `rgb(0, 150, 255)` |
| Super Soft | Light Red | `rgb(255, 100, 100)` |
| Ultra Soft | Purple | `rgb(180, 50, 200)` |
| Hyper Soft | Pink | `rgb(255, 150, 200)` |
| C1 / C2 | White | `rgb(255, 255, 255)` |
| C3 | Yellow | `rgb(255, 215, 0)` |
| C4 / C5 | Red | `rgb(255, 55, 55)` |
| All Weather | Green | `rgb(0, 180, 0)` |
| Custom / All others | Grey | `rgb(128, 128, 128)` |

Custom tyre types and all unrecognised types display with a neutral grey colour.

---

## Constraints and Validation

| Constraint | Value | Notes |
| --- | --- | --- |
| Maximum new custom types per league | **9** | |
| Maximum overrides of built-in types | Unlimited | Any built-in type can have its abbreviation/name replaced |
| `Type` — allowed characters | Basic ASCII letters and digits only | No spaces, no punctuation, no Unicode |
| `Abbreviation` — max length | **2 characters** | Longer values are ignored; default abbreviation is used |
| JSON format | Must be a valid JSON array | Invalid JSON disables all custom types |


