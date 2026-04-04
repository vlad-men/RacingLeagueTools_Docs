# Driver Features

Racing League Tools supports a driver feature system for tagging drivers with special designations — such as rookie status, skill tier, or any league-defined label. The system includes built-in feature types and a **custom extension mechanism** that allows each league to define its own feature names, override the display names and abbreviations of built-in types, or introduce entirely new ones — without any application update required.

A driver can hold **multiple features simultaneously** (for example, Rookie and a custom tier label at the same time).

---

## Built-in Driver Features

The table below lists all built-in driver features, their identifiers, default abbreviations, and display names. The abbreviation and name of any built-in feature can be overridden per league via the custom configuration described in the next section.

### Standard Features

| Identifier | Default Abbreviation | Default Display Name | Notes |
| --- | --- | --- | --- |
| `Rookie` | R | Rookie | New / inexperienced driver |
| `Amateur` | AM | Amateur | Non-professional driver |
| `Pro` | PRO | Pro | Professional driver |

### Custom Slots

Eight reserved slots are available for league-defined driver features. These are used when a custom entry uses a `Type` value that does not match any built-in identifier (see [Custom Driver Features](#custom-driver-features) below).

| Identifier | Default Abbreviation | Default Display Name |
| --- | --- | --- |
| `Custom1` | D1 | D1 |
| `Custom2` | D2 | D2 |
| `Custom3` | D3 | D3 |
| `Custom4` | D4 | D4 |
| `Custom5` | D5 | D5 |
| `Custom6` | D6 | D6 |
| `Custom7` | D7 | D7 |
| `Custom8` | D8 | D8 |

---

## Custom Driver Features

The system supports two operations:

1. **Override** the abbreviation and/or display name of any built-in driver feature.
2. **Add** entirely new feature types — up to **8** new types per league.

Both operations are performed by adding a JSON configuration entry to the league database. No application update is required.

### How to Configure

Custom driver features are stored as a JSON string in the **`LeagueSettings`** table of the league SQLite database. The recommended tool for editing the database directly is **DB Browser for SQLite**.

1. Open the league database file (`.db` or `.sqlite`) in DB Browser for SQLite.
2. Navigate to the **`LeagueSettings`** table (Browse Data tab).
3. Add a new row:
    - **Name**: `LeagueCustomDriverFeaturesJson`
    - **Type**: `String`
    - **Value**: a JSON array (see format below).
4. Save and close the database.
5. Restart Racing League Tools — the new driver features will be loaded at startup.

!!! note
    If a `LeagueCustomDriverFeaturesJson` row already exists, edit its **Value** field rather than adding a duplicate row.

### JSON Format

The value must be a **JSON array** of objects. Each object represents one driver feature entry.

```json
[
  {
    "Id": 1,
    "Type": "Crusher",
    "Abbreviation": "CR",
    "Name": "Crusher"
  },
  {
    "Id": 2,
    "Type": "Veteran",
    "Abbreviation": "V",
    "Name": "Veteran"
  }
]
```

#### Field Reference

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `Id` | `integer` | No | Controls the order in which new custom features are assigned to available slots. Entries are processed in ascending `Id` order. Defaults to `0` if omitted. |
| `Type` | `string` | Yes | Feature identifier. Must contain only basic ASCII letters and digits — no spaces, no special characters. Matched against built-in identifiers (case-sensitive). |
| `Abbreviation` | `string` | Yes | Short label shown in driver lists and graphics. Maximum **2 characters**. If empty or longer than 2 characters, the default abbreviation is used. |
| `Name` | `string` | No | Full display name used in tooltips and detailed views. If omitted or empty, the default name is used. |

### How Type Mapping Works

When the configuration is loaded, each entry's `Type` value is compared against built-in identifiers:

- **Match found** (e.g. `"Type": "Rookie"`): The entry **overrides** the abbreviation and/or name for that built-in feature.
- **No match** (e.g. `"Type": "Crusher"`): The entry is registered as a new feature type, assigned to the next available custom slot (`Custom1`–`Custom8`) in ascending `Id` order.

This means:

- Any number of built-in features can be overridden.
- At most **8 brand-new** feature types can be defined per league.

### Examples

#### Example 1 — Override Built-in Feature Labels

Rename the standard features to use league-specific terminology:

```json
[
  {
    "Type": "Rookie",
    "Abbreviation": "RK",
    "Name": "Rookie Driver"
  },
  {
    "Type": "Amateur",
    "Abbreviation": "AM",
    "Name": "Amateur Driver"
  },
  {
    "Type": "Pro",
    "Abbreviation": "PR",
    "Name": "Pro Driver"
  }
]
```

#### Example 2 — Add Entirely New Feature Types

Define custom driver tiers as new features (occupies the first two available custom slots):

```json
[
  {
    "Id": 1,
    "Type": "Crusher",
    "Abbreviation": "CR",
    "Name": "Crusher"
  },
  {
    "Id": 2,
    "Type": "Veteran",
    "Abbreviation": "V",
    "Name": "Veteran"
  }
]
```

#### Example 3 — Mix Overrides and New Types

```json
[
  {
    "Id": 0,
    "Type": "Pro",
    "Abbreviation": "PR",
    "Name": "Professional"
  },
  {
    "Id": 1,
    "Type": "Elite",
    "Abbreviation": "EL",
    "Name": "Elite Driver"
  }
]
```

Here `Pro` (a built-in feature) gets its display overridden, and `Elite` becomes a new feature type assigned to `Custom1`.

---

## Constraints and Validation

| Constraint | Value | Notes |
| --- | --- | --- |
| Maximum new custom features per league | **8** | |
| Maximum overrides of built-in features | Unlimited | Any built-in feature can have its abbreviation/name replaced |
| Multiple features per driver | Supported | A driver can have several features active at the same time |
| `Type` — allowed characters | Basic ASCII letters and digits only | No spaces, no punctuation, no Unicode |
| `Abbreviation` — max length | **2 characters** | Longer values are ignored; default abbreviation is used |
| JSON format | Must be a valid JSON array | Invalid JSON disables all custom features |
