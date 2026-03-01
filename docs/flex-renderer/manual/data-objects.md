# Data Objects

Data objects provide access to the underlying data model during rendering. Each render type exposes a specific set of root data objects that can be used in [Expressions](expressions.md). Full API documentation is available in the [Appendix](appendix.md).

## Root Data Objects by Render Type

The `LayoutInfo` and `Season` objects are available globally in every render type. The table below lists the additional root data objects specific to each render type.

| RenderType | Root Data Objects |
| --- | --- |
| `RaceResults` | `Session`, `Event` |
| `QualResults` | `Session`, `Event` |
| `CombinedQualResults` | `Session`, `Event` |
| `DriverStandings` | `Standings` |
| `TeamStandings` | `Standings` |
| `Lineups` | `Lineups` |
| `Calendar` | `Events` |
| `DriverSessionStatistics` | `Statistics`, `Session`, `Event` |
| `DriverSeasonStatistics` | `Statistics` |
| `DriverSession` | `DriverInfo`, `Session`, `Event` |
| `DriverInfo` | `DriverInfo` |
| `PenaltyItem` | `Penalty` |
| `PenaltyItems` | `Penalties` |
| `PenaltySeasonStatistics` | `Penalties` |
| `DeepRatingsSeason` | `DeepRatings` |
| `Teammates` | `Teammates` |
| `TeamStandingsMultiseason` | `TeamStandingsMultiseason` |
| `DriverStatistics` | `DriverStatistics` |
| `DriversStatistics` | `DriversStatistics` |
| `TrackStatistics` | `TrackStatistics` |
| `TracksStatistics` | `TracksStatistics` |

## Mapping Root Objects to API Classes

The table below shows how each template variable maps to an API class.

| Root Data Object | API Class | Notes |
| --- | --- | --- |
| `LayoutInfo` | `LayoutInfo` | Available in all render types |
| `Season` | `SeasonRenderData` | Available in all render types |
| `Session` | `SessionRenderData` | |
| `Event` | `EventRenderData` | |
| `Standings` | `StandingsSeasonRenderData` | |
| `Events` | `EventsSeasonRenderData` | |
| `Lineups` | `LineupsSeasonRenderData` | |
| `Statistics` | `StatisticsRenderHost` | |
| `DriverInfo` | `DriverSessionRenderHost` | In `DriverSession` context |
| `DriverInfo` | `DriverRenderHost` | In `DriverInfo` context |
| `Penalty` | `PenaltyItemRenderData` or `PenaltyActionRenderData` | Actual type depends on invocation source |
| `Penalties` | `EventPenaltiesRenderHost` | In `PenaltyItems` context |
| `Penalties` | `SeasonPenaltiesRenderHost` | In `PenaltySeasonStatistics` context |
| `DeepRatings` | `DeepRatingsSeasonRenderData` | |
| `Teammates` | `TeammatesSeasonRenderData` | |
| `TeamStandingsMultiseason` | `TeamStandingsMultiseasonRenderData` | |
| `DriverStatistics` | `DriverStatisticsMultiseasonRenderData` | |
| `DriversStatistics` | `DriversStatisticsMultiseasonRenderData` | |
| `TrackStatistics` | `TrackStatisticsMultiseasonRenderData` | |
| `TracksStatistics` | `TracksStatisticsMultiseasonRenderData` | |

Some render objects contain `Name` and `LogoPath` properties (which can be null) if the corresponding class inherits from `NamedRenderData`. Objects of type `byte[]` can be referenced as image paths for database-stored images.

## Important Notes

- **`DriverInfo`** is a single template variable, but its actual class depends on the render type: `DriverSessionRenderHost` for `DriverSession` and `DriverRenderHost` for `DriverInfo`.
- **`Penalty`** can hold either `PenaltyItemRenderData` or `PenaltyActionRenderData`, depending on the invocation source.
- **`DriverSeasonRenderData.Events`** contains **all** season events, including those the driver did not attend (with empty data). Events are ordered by position.
- **`TeammatesSeasonRenderData.Drivers`** always contains at least 4 elements; missing entries are filled with `IsExist = false`.
- **Pro/Advanced features**: certain fields in rating and race-details objects are only populated when the corresponding access level is available; otherwise they contain default (empty) values.
