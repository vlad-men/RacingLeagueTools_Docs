# JSON Data Export

Racing League Tools can export league data to structured **JSON files** for use in third-party tools, websites, overlays, and custom integrations. The export system produces four distinct export types, each targeting a different level of data granularity:

| Export Type | Description | Root JSON Key |
| --- | --- | --- |
| **Session** | Results of a single race, qualification, or practice session | `session` |
| **Event** | All sessions of an event | `sessions[]` |
| **Season Statistics** | Full season standings, statistics, and per-event breakdowns | `seasonStatistics` |
| **Multi-Season** | Aggregated driver/team/track statistics across multiple seasons | `multiSeasonStatistics` |

All exports share the same top-level `metadata` block and follow the same conventions for data types, time formatting, and feature gating.

---

## Common Conventions

### Date and Time

| Value | Format | Example |
| --- | --- | --- |
| Date only | `yyyy-MM-dd` | `"2024-06-23"` |
| Date + time (UTC) | `yyyy-MM-ddTHH:mm:ssZ` | `"2024-06-23T14:30:00Z"` |
| Lap / sector time | `m:ss.fff` | `"1:23.456"` |
| Duration in milliseconds | `integer` | `83456` |

Time values are provided as **both** a human-readable string and a raw millisecond integer. This allows easy display without parsing and accurate arithmetic without locale issues.

```json
"fastestLapTime": "1:23.456",
"fastestLapTimeMs": 83456
```

### Points

Points values are serialised as **strings** using invariant culture formatting. This prevents locale-specific decimal separator issues (`"25.5"` never becomes `"25,5"`).

```json
"points": "25.5",
"gapToLeader": "-3.0"
```

### Ratings

Driver and team ratings use a **0–10 scale** with two decimal places.

```json
"rating": "7.85"
```

### Colours

Team and class colours are expressed as **hex strings**.

```json
"primaryColor": "#FF0000"
```

### Null and Optional Fields

- Fields that are not applicable (e.g. `gridPosition` for a qualification) are `null` or omitted entirely.
- Fields gated behind feature tiers are `null` when the league does not have access to that tier.
- Array fields with no data are `null` rather than an empty array `[]`.

---

## Feature Access Tiers

Some export fields are only populated when the league subscription includes the corresponding feature tier.

| Tier | Examples of gated data |
| --- | --- |
| **Base** (always available) | All positions, points, session results, basic participation stats, penalty totals |
| **Advanced** | Pure pace rating, consistency rating, sector ratings |
| **Pro** | Attack rating, defense rating, overtakes count, positions-lost count, top-battle details |

When a field requires a tier the league does not have, it is `null` in the output. The field is always present in the JSON structure so integrations can check for `null` rather than handling missing keys.

## Shared Building Blocks

Several objects appear in multiple export types under the same name and with the same structure.

### `metadata`

Present at the root level in all four export types.

| Field | Type | Description |
| --- | --- | --- |
| `formatVersion` | `integer` | Schema version for forward compatibility. Currently `1`. |
| `exportType` | `string` | `"Session"`, `"SeasonStatistics"`, or `"MultiSeason"`. |
| `exportedAt` | `string` | UTC timestamp when the file was created (`yyyy-MM-ddTHH:mm:ssZ`). |
| `sourceApplication` | `string` | Always `"Racing League Tools"`. |
| `leagueName` | `string\|null` | Name of the league that produced the export. |

```json
"metadata": {
  "formatVersion": 1,
  "exportType": "Session",
  "exportedAt": "2024-06-23T14:30:00Z",
  "sourceApplication": "Racing League Tools",
  "leagueName": "My Racing League"
}
```

### `season` (context block)

Used in Session and Event exports. Provides enough context to identify where the session sits within the season.

| Field | Type | Description |
| --- | --- | --- |
| `seasonName` | `string` | Season display name (e.g. `"2024 Season"`). |
| `championshipName` | `string\|null` | Championship name. |
| `totalRounds` | `integer` | Total number of rounds in the season. |
| `completedRounds` | `integer` | Number of rounds completed so far. |
| `isMulticlass` | `boolean` | Whether the season uses racing classes. |
| `multiclassDefinitions` | `array\|null` | List of `{ uniqueName, name, abbreviation?, color? }` objects. Present only when `isMulticlass` is `true`. |

### `event` (context block)

Used in Session and Event exports.

| Field | Type | Description |
| --- | --- | --- |
| `round` | `integer` | Round number within the championship (1-based). |
| `eventDate` | `string\|null` | Event date (`yyyy-MM-dd`). |
| `racesCount` | `integer` | Number of race sessions in this event. |
| `qualificationsCount` | `integer` | Number of qualification sessions in this event. |
| `track` | `object` | Track information (see below). |

**`event.track`**

| Field | Type | Description |
| --- | --- | --- |
| `trackName` | `string` | Track display name (e.g. `"Circuit de Monaco"`). |
| `country` | `string\|null` | Country of the track. |
| `turnsCount` | `integer\|null` | Number of turns on the circuit. |

### Driver Info Block (`driverInfo`)

An optional extended block attached to driver entries across all export types. Included only when additional driver data is present in the league database.

| Field | Type | Description |
| --- | --- | --- |
| `nationality` | `string\|null` | Country name. |
| `raceNumber` | `integer\|null` | Race number, if assigned. |
| `realName` | `string\|null` | Real name if different from display name. |
| `shortName` | `string\|null` | Short name or abbreviation (e.g. `"HAM"`). |
| `platform` | `string\|null` | Gaming platform: `"PC"`, `"PlayStation"`, `"Xbox"`, etc. |
| `categories` | `string[]\|null` | League category names the driver belongs to. |
| `badge` | `string\|null` | Badge text. |
| `description` | `string\|null` | Driver biography or notes. |
| `discord` | `string\|null` | Discord username or link. |
| `steam` | `string\|null` | Steam username or link. |

### Team Info Block (`teamInfo`)

An optional extended block attached to team entries. Included only when additional team data is present.

| Field | Type | Description |
| --- | --- | --- |
| `uniqueId` | `string\|null` | Stable team identifier (consistent across seasons). |
| `fullName` | `string\|null` | Official full team name. |
| `abbreviation` | `string\|null` | Short team code (e.g. `"RBR"`). |
| `primaryColor` | `string\|null` | Primary team colour (hex). |
| `secondaryColor` | `string\|null` | Secondary team colour (hex). |
| `tertiaryColor` | `string\|null` | Tertiary team colour (hex). |
| `country` | `string\|null` | Team nationality/country. |
| `car` | `string\|null` | Default car used by the team. |
| `badge` | `string\|null` | Team badge text. |

---

## Export Type 1 — Session Export

A single session (race, qualification, or practice) with full driver results.

### Root Structure

```
{
  metadata,
  season,
  event,
  session: {
    sessionInfo,
    fastestLap?,
    raceDetails?,           // race sessions only
    qualificationDetails?,  // qualification sessions only
    drivers: [ ... ],
    classes?: [ ... ]       // multiclass only
  }
}
```

### `session.sessionInfo`

| Field | Type | Description |
| --- | --- | --- |
| `sessionId` | `string` | Unique session identifier (UUID). |
| `sessionType` | `string` | `"Race"`, `"Qualification"`, or `"Practice"`. |
| `raceType` | `string\|null` | Race sub-type: `"Feature"`, `"Sprint"`, `"Endurance"`, etc. Race sessions only. |
| `qualificationType` | `string\|null` | Qualification sub-type: `"Regular"`, `"TimeAttack"`, etc. Qualification sessions only. |
| `sessionPosition` | `integer` | Position within the event (1 = first session). |
| `sessionCaption` | `string\|null` | Display caption (e.g. `"Feature Race"`, `"Sprint Qualifying"`). |
| `completedStatus` | `string` | `"Completed"`, `"InProgress"`, `"Scheduled"`, or `"Cancelled"`. |
| `sessionDate` | `string\|null` | Session date/time (ISO 8601, with timezone offset). |
| `totalLaps` | `integer\|null` | Total race laps. `null` for timed or unconfigured sessions. |
| `driversCount` | `integer` | Total number of drivers classified in the session. |

### `session.fastestLap`

Present when a fastest lap has been recorded for the session.

| Field | Type | Description |
| --- | --- | --- |
| `lapTime` | `string` | Fastest lap as string (e.g. `"1:23.456"`). |
| `lapTimeMs` | `integer\|null` | Fastest lap in milliseconds. |
| `driverName` | `string\|null` | Name of the driver who set it. |
| `lapNumber` | `integer\|null` | Lap number when it was set. |
| `tyreCompound` | `string\|null` | Tyre compound used. |

### `session.raceDetails` (race sessions only)

| Field | Type | Description |
| --- | --- | --- |
| `raceType` | `string` | Race type (e.g. `"Feature"`). |
| `isMajorRace` | `boolean` | Whether this is the main/feature race of the event. |

### `session.qualificationDetails` (qualification sessions only)

| Field | Type | Description |
| --- | --- | --- |
| `qualificationType` | `string\|null` | Qualification type. |
| `segments` | `integer` | Number of knockout segments (0 for single-segment). |
| `poleTime` | `string\|null` | Pole position lap time. |
| `poleTimeMs` | `integer\|null` | Pole time in milliseconds. |
| `duration` | `string\|null` | Total session duration. |
| `durationMs` | `integer\|null` | Total session duration in milliseconds. |

### `session.drivers[]` — Driver Result Entry

Entries are sorted by classification position (ascending), with unclassified drivers at the end.

**Core fields**

| Field | Type | Description |
| --- | --- | --- |
| `driverName` | `string` | Driver display name. |
| `driverInfo` | `object\|null` | Extended driver info block. |
| `position` | `integer` | Overall session position. |
| `classificationPosition` | `integer` | Final classification position (may differ in class-based results). |
| `gridPosition` | `integer\|null` | Starting grid position. `null` if not applicable. |
| `positionChange` | `integer\|null` | Positions gained (positive) or lost (negative). `null` if no grid was set. |
| `status` | `string\|null` | Race result status: `"Finished"`, `"DNF"`, `"DNS"`, `"DSQ"`. `null` for non-race sessions. |
| `lapsCompleted` | `integer` | Number of laps completed. |
| `driverPoints` | `string\|null` | Points scored by this driver. |
| `teamPoints` | `string\|null` | Points scored by the team for this session. |

**Timing fields**

| Field | Type | Description |
| --- | --- | --- |
| `totalTime` | `string\|null` | Total race time (race sessions only). |
| `totalTimeMs` | `integer\|null` | Total race time in milliseconds. |
| `gap` | `string\|null` | Gap to race leader (e.g. `"+5.234"`, `"+1 lap"`). |
| `gapMs` | `integer\|null` | Gap in milliseconds. `0` for the leader. |
| `interval` | `string\|null` | Gap to the driver immediately ahead. |
| `intervalMs` | `integer\|null` | Interval in milliseconds. |
| `fastestLapTime` | `string\|null` | Driver's personal fastest lap. |
| `fastestLapTimeMs` | `integer\|null` | Fastest lap in milliseconds. |
| `fastestLapNumber` | `integer\|null` | Lap number of fastest lap. |
| `fastestLapTyreCompound` | `string\|null` | Tyre compound on fastest lap. |

**Nested objects (conditional)**

| Field | Present when | Description |
| --- | --- | --- |
| `team` | Driver has a team assigned | Team name and colours. |
| `car` | Car data is available | Car name, class, and manufacturer. |
| `classInfo` | Multiclass session | Driver's racing class and class position. |
| `stints` | Race session + stint data available | Array of stint details. |
| `raceDetails` | Race session | Max speed and average speed. |
| `qualDetails` | Qualification session | Max speed. |
| `penalties` | Driver received penalties | Penalty totals and individual items. |
| `topBattles` | Race session + Pro tier | Battle statistics and detail list. |
| `ratings` | Advanced or Pro tier | Pace, consistency, attack, defense ratings. |
| `laps` | Lap data was recorded | Per-lap data array. |

**`driver.team`**

| Field | Type | Description |
| --- | --- | --- |
| `name` | `string` | Team name. |
| `uniqueId` | `string\|null` | Stable team identifier. |
| `fullName` | `string\|null` | Official full name. |
| `abbreviation` | `string\|null` | Short team code. |
| `primaryColor` | `string\|null` | Primary colour (hex). |
| `secondaryColor` | `string\|null` | Secondary colour (hex). |
| `tertiaryColor` | `string\|null` | Tertiary colour (hex). |
| `country` | `string\|null` | Team nationality. |
| `badge` | `string\|null` | Badge text. |

**`driver.car`**

| Field | Type | Description |
| --- | --- | --- |
| `carName` | `string` | Car model name. |
| `className` | `string\|null` | Car class name. |
| `classColor` | `string\|null` | Class colour (hex). |
| `manufacturer` | `string\|null` | Car manufacturer/vendor. |

**`driver.classInfo`** (multiclass sessions)

| Field | Type | Description |
| --- | --- | --- |
| `uniqueName` | `string` | Class identifier. |
| `name` | `string` | Class display name. |
| `abbreviation` | `string\|null` | Short class name. |
| `color` | `string\|null` | Class colour (hex). |
| `classPosition` | `integer` | Driver's position within the class. |
| `classDriversCount` | `integer` | Total drivers in the class. |

**`driver.stints[]`** (race sessions)

| Field | Type | Description |
| --- | --- | --- |
| `stintNumber` | `integer` | Stint number (1-based). |
| `tyreCompound` | `string` | Tyre compound used during this stint. |
| `startLap` | `integer` | First lap of the stint. |
| `endLap` | `integer` | Last lap of the stint. |
| `lapsCount` | `integer` | Total laps completed on this stint. |

**`driver.penalties`**

| Field | Type | Description |
| --- | --- | --- |
| `inGamePenaltySeconds` | `integer` | Total in-game time penalty seconds. |
| `stewardPenaltySeconds` | `integer` | Total steward-issued time penalty seconds. |
| `inGamePenaltyPositions` | `integer` | In-game position penalties. |
| `stewardPenaltyPositions` | `integer` | Steward-issued position penalties. |
| `totalPenaltyPoints` | `integer` | Total penalty points accumulated. |
| `inGamePenalties` | `array\|null` | List of individual in-game penalty items. |
| `stewardPenalties` | `array\|null` | List of individual steward penalty items. |

Each item in `inGamePenalties[]` / `stewardPenalties[]`:

| Field | Type | Description |
| --- | --- | --- |
| `offense` | `string` | Description of the infraction. |
| `action` | `string` | Penalty action name (e.g. `"Time Penalty"`). |
| `penaltySeconds` | `integer\|null` | Time penalty in seconds. |
| `penaltyPoints` | `integer\|null` | Penalty points issued. |
| `penaltyPositions` | `integer\|null` | Position penalty. |
| `lapNumber` | `integer\|null` | Lap when the penalty was given. |
| `description` | `string\|null` | Additional notes. |

**`driver.topBattles`** *(Pro tier, race sessions only)*

| Field | Type | Description |
| --- | --- | --- |
| `totalBattlesCount` | `integer` | Total number of on-track battles. |
| `battlesWon` | `integer` | Battles won. |
| `battlesLost` | `integer` | Battles lost. |
| `winPercentage` | `integer` | Win percentage (0–100). |
| `overtakes` | `integer` | Number of successful overtakes made. |
| `positionsLost` | `integer` | Positions lost to opponents. |
| `battles` | `array\|null` | Detailed battle entries (see below). |

Each battle entry:

| Field | Type | Description |
| --- | --- | --- |
| `opponentName` | `string` | Name of the opponent driver. |
| `battleType` | `string` | `"Attack"` or `"Defense"`. |
| `isWon` | `boolean` | Whether this battle was won. |
| `startLap` | `integer\|null` | Lap the battle began. |
| `endLap` | `integer\|null` | Lap the battle ended. |
| `durationLaps` | `integer` | How many laps the battle lasted. |
| `driverTyreCompound` | `string\|null` | Driver's tyre at battle start. |
| `opponentTyreCompound` | `string\|null` | Opponent's tyre at battle start. |
| `driverTyreWear` | `integer\|null` | Driver's tyre wear % at battle start. |
| `opponentTyreWear` | `integer\|null` | Opponent's tyre wear % at battle start. |

**`driver.ratings`**

All ratings use the 0–10 scale. Sub-objects are `null` when the corresponding feature tier is not available.

| Field | Tier required | Description |
| --- | --- | --- |
| `pace` | Advanced | Pure race pace rating. |
| `consistency` | Advanced | Lap consistency rating. |
| `attack` | Pro | Overtaking / attack rating. |
| `defense` | Pro | Defensive driving rating. |

`pace` and `consistency` share this structure:

| Field | Type | Description |
| --- | --- | --- |
| `rating` | `string` | Rating on the 0–10 scale. |
| `position` | `integer` | Rank among all session drivers. |
| `gapToLeader` | `string\|null` | Gap to the top-rated driver. |
| `gapToLeaderMs` | `integer\|null` | Gap in milliseconds. |
| `sectors` | `object\|null` | `{ sector1Rating, sector2Rating, sector3Rating }` — per-sector ratings. |

`pace` additionally includes:

| Field | Type | Description |
| --- | --- | --- |
| `pureLapTime` | `string\|null` | Theoretical best lap (composed from best sectors). |
| `pureLapTimeMs` | `integer\|null` | Theoretical best lap in milliseconds. |

`consistency` additionally includes:

| Field | Type | Description |
| --- | --- | --- |
| `averageDeviation` | `string\|null` | Average lap time deviation from optimal. |
| `averageDeviationMs` | `integer\|null` | Average deviation in milliseconds. |

`attack` and `defense` share this structure:

| Field | Type | Description |
| --- | --- | --- |
| `rating` | `string` | Rating on the 0–10 scale. |
| `position` | `integer` | Rank among all session drivers. |
| `overtakes` | `integer` | Successful overtakes made (attack) / positions defended (defense). |
| `battlesCount` | `integer` | Total battles engaged. |
| `winPercentage` | `integer` | Percentage of battles won. |
| `topBattles` | `array\|null` | Highlight battle entries. |

**`driver.laps[]`** — Per-Lap Data

| Field | Type | Description |
| --- | --- | --- |
| `lapNumber` | `integer` | Lap number (1-based). |
| `lapTime` | `string` | Lap time string. |
| `lapTimeMs` | `integer\|null` | Lap time in milliseconds. |
| `sector1Time` | `string\|null` | Sector 1 time. |
| `sector1TimeMs` | `integer\|null` | Sector 1 in milliseconds. |
| `sector2Time` | `string\|null` | Sector 2 time. |
| `sector2TimeMs` | `integer\|null` | Sector 2 in milliseconds. |
| `sector3Time` | `string\|null` | Sector 3 time. |
| `sector3TimeMs` | `integer\|null` | Sector 3 in milliseconds. |
| `tyreCompound` | `string\|null` | Tyre compound on this lap. |
| `isValid` | `boolean` | Whether the lap was valid (no track limit violations). |
| `isPersonalBest` | `boolean` | Whether this was the driver's personal best lap. |
| `isSessionFastest` | `boolean` | Whether this was the overall fastest lap of the session. |
| `positionAfterLap` | `integer\|null` | Race position after completing this lap. |
| `gapToLeader` | `string\|null` | Gap to race leader after this lap. |
| `gapToLeaderMs` | `integer\|null` | Gap in milliseconds. |
| `gapToAhead` | `string\|null` | Gap to driver immediately ahead. |
| `gapToAheadMs` | `integer\|null` | Gap ahead in milliseconds. |
| `deltaToPreviousLap` | `string\|null` | Delta vs. the driver's previous lap. |
| `deltaToPreviousLapMs` | `integer\|null` | Delta in milliseconds. |
| `deltaToPersonalBest` | `string\|null` | Delta vs. the driver's best lap. |
| `deltaToPersonalBestMs` | `integer\|null` | Delta in milliseconds. |

### Minimal Example

```json
{
  "metadata": {
    "formatVersion": 1,
    "exportType": "Session",
    "exportedAt": "2024-06-23T14:30:00Z",
    "sourceApplication": "Racing League Tools",
    "leagueName": "My League"
  },
  "season": {
    "seasonName": "2024 Season",
    "championshipName": "League Championship",
    "totalRounds": 12,
    "completedRounds": 3,
    "isMulticlass": false
  },
  "event": {
    "round": 3,
    "eventDate": "2024-06-23",
    "racesCount": 1,
    "qualificationsCount": 1,
    "track": {
      "trackName": "Circuit de Monaco",
      "country": "Monaco",
      "turnsCount": 19
    }
  },
  "session": {
    "sessionInfo": {
      "sessionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "sessionType": "Race",
      "raceType": "Feature",
      "sessionPosition": 1,
      "sessionCaption": "Feature Race",
      "completedStatus": "Completed",
      "totalLaps": 78,
      "driversCount": 20
    },
    "fastestLap": {
      "lapTime": "1:14.260",
      "lapTimeMs": 74260,
      "driverName": "Lewis Hamilton",
      "lapNumber": 55,
      "tyreCompound": "Soft"
    },
    "drivers": [
      {
        "driverName": "Lewis Hamilton",
        "position": 1,
        "classificationPosition": 1,
        "gridPosition": 2,
        "positionChange": 1,
        "status": "Finished",
        "lapsCompleted": 78,
        "driverPoints": "25",
        "totalTime": "1:32:15.123",
        "totalTimeMs": 5535123,
        "gap": "0",
        "gapMs": 0,
        "fastestLapTime": "1:14.260",
        "fastestLapTimeMs": 74260,
        "fastestLapNumber": 55,
        "fastestLapTyreCompound": "Soft",
        "team": {
          "name": "Mercedes",
          "primaryColor": "#00D2BE"
        },
        "stints": [
          { "stintNumber": 1, "tyreCompound": "Medium", "startLap": 1, "endLap": 30, "lapsCount": 30 },
          { "stintNumber": 2, "tyreCompound": "Soft", "startLap": 31, "endLap": 78, "lapsCount": 48 }
        ]
      }
    ]
  }
}
```

---

## Export Type 2 — Event Export

An event export bundles all sessions of an event into one file. The structure mirrors the Session export but replaces the single `session` block with a `sessions` array.

### Root Structure

```
{
  metadata,
  season,
  event,
  sessions: [
    {
      sessionInfo,
      fastestLap?,
      raceDetails?,
      qualificationDetails?,
      drivers: [ ... ],
      classes?: [ ... ]
    },
    ...
  ]
}
```

The `season`, `event`, `sessionInfo`, and `drivers` blocks are identical in structure to the Session export. Sessions are ordered chronologically within the event (qualifications first, then races).

---

## Export Type 3 — Season Statistics Export

The most detailed export type. Contains full season standings, per-driver and per-team statistics, event-by-event breakdowns, and optionally the complete standings progression after each round.

### Root Structure

```
{
  metadata,
  season,
  seasonStatistics: {
    status,
    driverStandings: [ ... ],
    teamStandings?: [ ... ],
    classes?: [ ... ]   // multiclass seasons only
  },
  seasonStatisticsHistory?  // optional
}
```

### `season` Block (Season Statistics)

This is an extended version of the season context used in Session exports.

| Field | Type | Description |
| --- | --- | --- |
| `seasonName` | `string` | Season display name. |
| `championshipName` | `string` | Championship name. |
| `totalRounds` | `integer` | Total rounds in the season. |
| `completedRounds` | `integer` | Number of completed rounds. |
| `lineupsBasedOn` | `string` | What lineups are organised around: `"Team"`, `"Car"`, etc. |
| `isMulticlass` | `boolean` | Whether the season is multiclass. |
| `seasonStartDate` | `string\|null` | First event date (`yyyy-MM-dd`). |
| `seasonEndDate` | `string\|null` | Last event date (`yyyy-MM-dd`). |

### `seasonStatistics.status`

| Field | Type | Description |
| --- | --- | --- |
| `completionPercentage` | `number` | Season completion as a percentage (0–100). |
| `statusText` | `string` | Human-readable status (e.g. `"Round 3 of 12"`). |
| `isCompleted` | `boolean` | Whether all rounds are finished. |
| `isInProgress` | `boolean` | Whether the season has started but not finished. |
| `dateRangeText` | `string` | Human-readable date range. |
| `upcomingRounds` | `integer` | Number of remaining rounds. |
| `nextRoundName` | `string\|null` | Name or track of the next upcoming round. |
| `nextRoundDate` | `string\|null` | Date of the next round (`yyyy-MM-dd`). |

### `seasonStatistics.driverStandings[]` — Driver Standings Entry

**Identification and position**

| Field | Type | Description |
| --- | --- | --- |
| `driverName` | `string` | Driver display name. |
| `driverInfo` | `object\|null` | Extended driver info block. |
| `seatType` | `string\|null` | `"Primary"` or `"Reserve"`. |
| `position` | `integer` | Current standings position. |
| `points` | `string` | Total points earned. |
| `gapToLeader` | `string\|null` | Points gap to the standings leader (e.g. `"-24.5"`). |
| `gapToAhead` | `string\|null` | Points gap to the driver immediately ahead. |
| `positionChange` | `integer` | Standings position change since last round. |
| `isNewInStandings` | `boolean` | Whether the driver is appearing in standings for the first time. |
| `teamName` | `string\|null` | Current team name. |
| `teamInfo` | `object\|null` | Extended team info block. |
| `carName` | `string\|null` | Current car name. |
| `hasMultipleTeams` | `boolean` | Whether the driver raced for more than one team. |
| `teamsCount` | `integer` | Number of distinct teams raced for. |
| `classInfo` | `object\|null` | Class identity (multiclass seasons only). |

**Championship tracking**

| Field | Type | Description |
| --- | --- | --- |
| `bestPossiblePosition` | `integer` | Best final position still mathematically achievable. |
| `canWinChampionship` | `boolean` | Whether the title is still possible. |
| `isChampionshipSecured` | `boolean` | Whether the title is already confirmed. |
| `bestChampionshipPosition` | `integer` | Best standing position reached during the season. |
| `roundsLeading` | `integer` | Number of rounds the driver led the championship. |

**Statistics sub-blocks**

| Field | Present | Description |
| --- | --- | --- |
| `participation` | Always | Event, race, and qualification participation counts and completion rates. |
| `positions` | Always | Best/worst/average positions, wins, podiums, top-5/10, poles, fastest laps, position distributions. |
| `raceDetails` | Always | Season-total race stats: laps led, pit stops, max speed, and Pro-tier overtake/positions-lost stats. |
| `events` | Always | Per-event breakdown (see below). |
| `penalties` | When penalties exist | Penalty totals split by source. |
| `discardInfo` | When discard rules are active | Discard configuration and list of dropped results. |
| `ratings` | Advanced / Pro tier | Season-aggregated pace, consistency, attack, defense ratings. |
| `liveDataCoverage` | When live data was tracked | Coverage percentage and session counts. |

**`participation` block**

| Field | Type | Description |
| --- | --- | --- |
| `eventsParticipated` | `integer` | Events (weekends) where the driver appeared. |
| `totalEvents` | `integer` | Total events in the season. |
| `eventCompletionRate` | `number` | Event participation rate (0.0–1.0). |
| `racesParticipated` | `integer` | Races started. |
| `racesFinished` | `integer` | Races finished (not DNF/DSQ). |
| `raceCompletionRate` | `number` | Race finish rate (0.0–1.0). |
| `qualificationsParticipated` | `integer` | Qualification sessions entered. |
| `qualificationsCompleted` | `integer` | Qualifications completed. |
| `sprintRacesParticipated` | `integer\|null` | Sprint race count (if applicable). |
| `featureRacesParticipated` | `integer\|null` | Feature race count (if applicable). |
| `sessionBreakdown` | `object\|null` | Counts by session type (practice, qualification, sprint, feature). |

**`positions` block**

| Field | Type | Description |
| --- | --- | --- |
| `bestRacePosition` | `integer` | Best race finish position. |
| `worstRacePosition` | `integer` | Worst race finish position. |
| `averageRacePosition` | `number` | Average race finish position. |
| `bestQualPosition` | `integer` | Best qualification position. |
| `worstQualPosition` | `integer` | Worst qualification position. |
| `averageQualPosition` | `number` | Average qualification position. |
| `averagePositionChange` | `number` | Average positions gained/lost per race. |
| `bestPositionGain` | `integer` | Best single-race position gain. |
| `worstPositionLoss` | `integer` | Worst single-race position loss. |
| `averagePointsPerRace` | `string\|null` | Average points per race entry. |
| `scoringRacesCount` | `integer` | Races where points were scored. |
| `zeroPointRacesCount` | `integer` | Races where no points were scored. |
| `wins` | `integer` | Number of race wins. |
| `podiums` | `integer` | Number of podium finishes (P1–P3). |
| `topFives` | `integer` | Top-5 finishes. |
| `topTens` | `integer` | Top-10 finishes. |
| `polePositions` | `integer` | Number of pole positions. |
| `frontRowStarts` | `integer` | Front-row starts (P1–P2 on grid). |
| `fastestLaps` | `integer` | Number of fastest laps in races. |
| `racePositionDistribution` | `object\|null` | Map of `"position" → count` for race results. |
| `qualPositionDistribution` | `object\|null` | Map of `"position" → count` for qualification results. |

**`raceDetails` block**

| Field | Tier | Description |
| --- | --- | --- |
| `bestMaxSpeed` | Base | Best top speed recorded (km/h). |
| `averageMaxSpeed` | Base | Average top speed. |
| `maxSpeedWinsCount` | Base | Races where the driver had the highest top speed. |
| `totalLeadLaps` | Base | Total laps led. |
| `totalLaps` | Base | Total laps completed across all races. |
| `totalPossibleLaps` | Base | Total race laps available if no DNFs. |
| `lapCompletionRate` | Base | Lap completion ratio (0.0–1.0). |
| `totalPitStops` | Base | Total pit stops. |
| `averagePitStopsPerRace` | Base | Average pit stops per race. |
| `fastestLapWins` | Base | Races where the driver set the overall fastest lap. |
| `totalOvertakes` | Pro | Total overtakes made across all races. |
| `bestOvertakesInRace` | Pro | Most overtakes in a single race. |
| `averageOvertakesPerRace` | Pro | Average overtakes per race. |
| `totalPositionsLost` | Pro | Total positions lost to opponents. |
| `averagePositionsLostPerRace` | Pro | Average positions lost per race. |

**`events[]` — Per-Event Breakdown**

| Field | Type | Description |
| --- | --- | --- |
| `roundNumber` | `integer` | Round number in the season (1-based). |
| `eventName` | `string` | Event/track name. |
| `trackName` | `string` | Track name. |
| `eventDate` | `string\|null` | Event date. |
| `pointsEarned` | `string\|null` | Total points earned this event. |
| `isDiscarded` | `boolean` | Whether this event's result was discarded (dropped score). |
| `races` | `array\|null` | Race session results for this driver at this event. |
| `qualifications` | `array\|null` | Qualification session results. |

Each race entry in `events[].races[]`:

| Field | Type | Description |
| --- | --- | --- |
| `sessionName` | `string` | Session name (e.g. `"Race 1"`). |
| `position` | `integer\|null` | Finish position. |
| `gridPosition` | `integer\|null` | Starting grid position. |
| `positionChange` | `integer\|null` | Positions gained/lost. |
| `pointsEarned` | `string\|null` | Points scored in this race. |
| `status` | `string\|null` | Result status (`"Finished"`, `"DNF"`, etc.). |
| `isFinished` | `boolean` | Whether the driver finished. |
| `isFastestLap` | `boolean` | Whether the driver set the session fastest lap. |

Each qualification entry in `events[].qualifications[]`:

| Field | Type | Description |
| --- | --- | --- |
| `sessionName` | `string` | Session name. |
| `position` | `integer\|null` | Qualification position. |
| `status` | `string\|null` | Result status. |
| `isCompleted` | `boolean` | Whether the driver completed the session. |

### `seasonStatistics.teamStandings[]`

Team standings entries mirror driver standings in structure with the following differences:

- `teamName` replaces `driverName`; `teamInfo` replaces `driverInfo`.
- `driverNames` (string array) lists current team drivers; `driversCount` gives the total driver count.
- `ratings` contains `overallRating`, `paceRating`, `consistencyRating`, and `ratingsDataSessionsCount`.
- The `events[]` sub-array contains team-level results with a `driverResults[]` list per session.

### `seasonStatisticsHistory` (optional)

Optional: contains one snapshot per completed round showing the full standings as they stood after that round.

```
seasonStatisticsHistory: {
  snapshots: [
    {
      metadata: { roundNumber, roundName, roundDate? },
      seasonStatistics: {
        driverStandings: [ { driverName, position, points, ... } ],
        teamStandings?: [ ... ]
      }
    },
    ...
  ]
}
```

Snapshot standings are a simplified subset — position, points, and gap fields only (no per-event breakdowns or detailed statistics).

### `seasonStatistics.classes[]` (multiclass)

For multiclass seasons, each entry contains a `classInfo` block and a `classStatistics` block that is identical in structure to the root `seasonStatistics` block (minus the nested `classes` array).

```json
{
  "classInfo": { "uniqueName": "LMH", "name": "LMH Class", "abbreviation": "LMH", "color": "#FF0000" },
  "classStatistics": {
    "status": { "driversCount": 8, "teamsCount": 4 },
    "driverStandings": [ "..." ],
    "teamStandings": [ "..." ]
  }
}
```

---

## Export Type 4 — Multi-Season Export

Aggregated statistics spanning multiple seasons. Useful for career statistics, all-time records, and cross-season comparisons.

### Root Structure

```
{
  metadata,
  multiSeasonStatistics: {
    multiSeasonInfo,
    seasons: [ ... ],
    drivers: [ ... ],
    teams?: [ ... ],
    tracks?: [ ... ]
  }
}
```

### `multiSeasonStatistics.multiSeasonInfo`

| Field | Type | Description |
| --- | --- | --- |
| `name` | `string` | Multi-season display name. |
| `seasonsCount` | `integer` | Total seasons included. |
| `completedSeasonsCount` | `integer` | Number of fully completed seasons. |
| `racingClassName` | `string\|null` | Class name if this is a class-specific export. |
| `isClassSpecific` | `boolean` | Whether only one racing class is covered. |
| `totalDrivers` | `integer` | Unique drivers across all seasons. |
| `totalTeams` | `integer\|null` | Unique teams across all seasons. |
| `totalTracks` | `integer\|null` | Unique tracks visited across all seasons. |
| `snapshot` | `object\|null` | `{ date?, roundNumber?, isLatest }` — present for historical snapshots. |

### `multiSeasonStatistics.seasons[]`

| Field | Type | Description |
| --- | --- | --- |
| `name` | `string` | Season name. |
| `championshipName` | `string\|null` | Championship name. |
| `totalRounds` | `integer` | Total rounds in the season. |
| `completedRounds` | `integer` | Completed rounds. |
| `isCompleted` | `boolean` | Whether the season is finished. |
| `isStarted` | `boolean` | Whether at least one round was completed. |
| `startDate` | `string\|null` | First event date. |
| `endDate` | `string\|null` | Last event date. |

### `multiSeasonStatistics.drivers[]`

| Field | Present | Description |
| --- | --- | --- |
| `driverId` | Always | Internal driver identifier (stable across seasons). |
| `driverName` | Always | Driver display name. |
| `driverInfo` | Optional | Extended driver info block. |
| `participation` | Always | Multi-season participation counts and completion rates. |
| `points` | Always | Total and average points statistics. |
| `racePositions` | Always | Best/average positions, wins, podiums, top-5/10. |
| `qualPositions` | Always | Poles, front rows, best/average qualifying position. |
| `standings` | Always | Championship history: titles, best/average position, per-season results. |
| `discipline` | Always | DNFs, penalties, and race incident statistics. |

**`participation` block**

| Field | Type | Description |
| --- | --- | --- |
| `seasonsParticipated` | `integer` | Number of seasons raced in. |
| `totalEvents` | `integer` | Total race weekends. |
| `totalRaces` | `integer` | Total races started. |
| `totalMajorRaces` | `integer` | Total feature/main races. |
| `totalQualifications` | `integer` | Total qualification sessions. |
| `totalRacesFinished` | `integer` | Races completed (not DNF/DSQ). |
| `eventCompletionRatePercent` | `number` | Event participation rate (0–100). |
| `raceCompletionRatePercent` | `number` | Race finish rate (0–100). |

**`points` block**

| Field | Type | Description |
| --- | --- | --- |
| `totalPoints` | `string` | Career points total. |
| `averagePerSeason` | `string` | Average points per season. |
| `averagePerMajorRace` | `string` | Average points per major race. |
| `averagePerEvent` | `string` | Average points per event (race weekend). |
| `bestSeasonPoints` | `string` | Highest points scored in a single season. |
| `bestSeasonName` | `string\|null` | Name of the season with the best points total. |
| `scoringRacesCount` | `integer` | Races where at least one point was scored. |
| `scoringRatePercent` | `number` | Percentage of races with points. |

**`racePositions` block**

| Field | Type | Description |
| --- | --- | --- |
| `bestPosition` | `integer` | Career best race finish. |
| `averagePosition` | `number` | Career average race finish. |
| `wins` | `integer` | Total wins. |
| `podiums` | `integer` | Total podiums (P1–P3). |
| `top5` | `integer` | Total top-5 finishes. |
| `top10` | `integer` | Total top-10 finishes. |
| `totalFinishes` | `integer` | Total classified finishes. |
| `averageGridPosition` | `number` | Career average starting position. |
| `averagePositionChange` | `number` | Career average positions gained/lost. |

**`qualPositions` block**

| Field | Type | Description |
| --- | --- | --- |
| `bestPosition` | `integer` | Career best qualifying position. |
| `averagePosition` | `number` | Career average qualifying position. |
| `poles` | `integer` | Total pole positions. |
| `frontRows` | `integer` | Front-row starts (P1–P2). |
| `top3` | `integer` | Top-3 qualifying finishes. |
| `top5` | `integer` | Top-5 qualifying finishes. |
| `top10` | `integer` | Top-10 qualifying finishes. |
| `totalQualifications` | `integer` | Total qualification sessions completed. |

**`standings` block**

| Field | Type | Description |
| --- | --- | --- |
| `championshipsWon` | `integer` | Number of championships won. |
| `bestPosition` | `integer` | Best final championship standing. |
| `averagePosition` | `number` | Average final championship position. |
| `runnerUps` | `integer` | Runner-up (P2) championship finishes. |
| `top3Finishes` | `integer` | Top-3 championship finishes. |
| `top5Finishes` | `integer` | Top-5 championship finishes. |
| `seasonResults` | `array\|null` | Per-season `{ seasonName, position, points? }` list. |

### `multiSeasonStatistics.teams[]`

| Field | Type | Description |
| --- | --- | --- |
| `teamId` | `integer` | Internal team identifier. |
| `teamName` | `string` | Team name. |
| `teamInfo` | `object\|null` | Extended team info block. |
| `position` | `integer` | Multi-season standings position. |
| `totalPoints` | `string` | Career total points. |
| `participation` | `object` | Seasons, events, races, and finishes counts. |
| `racePositions` | `object` | Best position, wins, podiums, top-5/10, total finishes. |

### `multiSeasonStatistics.tracks[]`

| Field | Type | Description |
| --- | --- | --- |
| `trackName` | `string` | Track display name. |
| `circuitName` | `string\|null` | Circuit name. |
| `country` | `string\|null` | Country of the track. |
| `generalStats` | `object` | Overall visit counts, dates, and absolute track record. |
| `raceStats` | `object\|null` | Race-specific records and history. `null` if no race data. |
| `qualificationStats` | `object\|null` | Qualification-specific records. `null` if no qualification data. |

**`generalStats`**

| Field | Type | Description |
| --- | --- | --- |
| `totalEvents` | `integer` | Events held at this track. |
| `totalSeasons` | `integer` | Seasons that visited this track. |
| `totalRaces` | `integer` | Total races held. |
| `totalMajorRaces` | `integer` | Feature/main races held. |
| `totalQualifications` | `integer` | Qualifications held. |
| `firstVisitDate` | `string\|null` | Date of first visit. |
| `lastVisitDate` | `string\|null` | Date of most recent visit. |
| `absoluteTrackRecord` | `object\|null` | Fastest ever lap across all session types. |

**`raceStats`**

| Field | Type | Description |
| --- | --- | --- |
| `fastestRaceLap` | `object\|null` | Fastest race lap record: `{ time, timeMs, driverName, teamName?, seasonName?, sessionType? }`. |
| `mostWinsDriver` | `object\|null` | `{ driverName, count }` |
| `mostWinsTeam` | `object\|null` | `{ teamName, count }` |
| `mostPodiumsDriver` | `object\|null` | `{ driverName, count }` |
| `mostPodiumsTeam` | `object\|null` | `{ teamName, count }` |
| `avgPitstops` | `number\|null` | Average pit stops per race. |
| `maxSpeed` | `number\|null` | Maximum recorded speed (km/h). |
| `totalSafetyCars` | `integer\|null` | Total safety car deployments. |
| `totalVirtualSafetyCars` | `integer\|null` | Total virtual safety car deployments. |
| `races` | `array\|null` | Chronological list of races with winner info. |

**`qualificationStats`**

| Field | Type | Description |
| --- | --- | --- |
| `fastestQualLap` | `object\|null` | Fastest qualification lap record. |
| `mostPolesDriver` | `object\|null` | `{ driverName, count }` |
| `mostPolesTeam` | `object\|null` | `{ teamName, count }` |
| `qualifications` | `array\|null` | Chronological list of qualifications with pole sitter info. |

Each entry in `races[]` / `qualifications[]`:

| Field | Type | Description |
| --- | --- | --- |
| `date` | `string` | Event date (ISO 8601). |
| `seasonName` | `string` | Season in which this session took place. |
| `driverName` | `string\|null` | Winner / pole sitter name. |
| `teamName` | `string\|null` | Winner / pole sitter team. |

---

## Top-Level Keys by Export Type

| Key | Session | Event | Season Statistics | Multi-Season |
| --- | --- | --- | --- | --- |
| `metadata` | Yes | Yes | Yes | Yes |
| `season` | Yes | Yes | Yes (extended) | No |
| `event` | Yes | Yes | No | No |
| `session` | Yes | No | No | No |
| `sessions` | No | Yes | No | No |
| `seasonStatistics` | No | No | Yes | No |
| `seasonStatisticsHistory` | No | No | Optional | No |
| `multiSeasonStatistics` | No | No | No | Yes |
