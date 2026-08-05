# Commands

Every command is a Discord slash command: type `/`, pick the command, fill in the options. Anyone on
the server can use the data commands. Only members with **Manage Server** can use `/setup` and
`/setlang`.

Almost every option can be left empty — the bot then picks the sensible default (current season,
latest round, drivers classification). Options like `season`, `round`, `session`, `driver` and `team`
offer **autocomplete**: you start typing a name and pick from the list, so you never deal with IDs.

## Text embeds or image cards

The commands split into two families, and the name always tells you which reply you will get:

* **`/render-…`** uploads a **PNG image card**. Documented on its own page: [Image cards](image-cards.md).
* **everything else** replies with a **text embed** — a normal Discord message with selectable text.

This page is the reference for the embed commands; the image cards get their own page because reading
a card is a visual matter. The options are shared, so the section on
[choosing season, round and session](#how-season-round-and-session-are-chosen) below applies to both
families.

### Data commands — text embeds

| Command | What it shows |
|---|---|
| `/standings` | Championship standings for a season — drivers or constructors |
| `/race-results` | Race results — podium, top 10, fastest lap |
| `/qual-results` | Qualifying results — pole position, top 10, best laps |
| `/driver` | Driver profile — career, one season, or a group of seasons |
| `/head2head` | Two drivers, or a team's pairing, compared over a season |
| `/season` | Season calendar with round statuses, or upcoming rounds with countdowns |
| `/league` | The linked league — season counts and the most recent seasons |

### Data commands — image cards

| Command | What it renders |
|---|---|
| `/render-race-results` | Race result table |
| `/render-qual-results` | Qualifying result table |
| `/render-race-highlights` | Session highlights — stat tiles |
| `/render-race-strategy` | Tyre strategy — stint chart |

### Utility and admin commands

| Command | What it does | Reply |
|---|---|---|
| `/ping` | Whether the bot is alive, and its latency | plain text |
| `/setlang` | [Response language](settings.md#response-language) for this server | plain text, private |
| `/setup` | [Linking](linking.md) and [server settings](settings.md) | plain text, private |

!!! tip "Same session, either form"
    `/race-results` and `/render-race-results` (likewise `/qual-results` and `/render-qual-results`)
    look at exactly the same session and accept the same options. Swapping the command is all it
    takes to get the other form.

## How season, round and session are chosen

These three options work the same way in every results and image command, and all three are optional.

| You provide | What the bot uses |
|---|---|
| nothing | The current season, its latest round that actually has a session of the right kind, and the newest such session |
| `season` only | That season's latest round with a matching session |
| `season` + `round` | The newest matching session in that round |
| `session` as well | Exactly that session |

The command name decides the session kind: `/race-results` and `/render-race-*` look at races,
`/qual-results` and `/render-qual-results` at qualifying. The autocomplete lists only rounds and
sessions of the matching kind.

!!! note "Sprint weekends"
    A sprint and a feature race are both *race* sessions in the same round. When you leave `session`
    empty, the bot picks the **feature race**. To get the sprint, choose it explicitly from the
    `session` list. The same applies to a round with two qualifying sessions — empty `session` gives
    the later one (`Qual 2`).

!!! tip
    Practice sessions are not supported by any command. If you point a command at one, it replies
    that the session is of the wrong kind.

## `/standings`

Championship standings for a season.

| Option | Meaning |
|---|---|
| `season` | Season. Omitted = current. |
| `type` | `Drivers` (default) or `Constructors`. |

The table lists position, name, points and gap to the leader. The embed's colour stripe takes the
leader's team colour.

## `/race-results`

Race results for one session.

| Option | Meaning |
|---|---|
| `season` | Season. Omitted = current. |
| `round` | Round. Omitted = latest round with a race. |
| `session` | Race session in that round. Omitted = the latest one. |
| `type` | `Drivers` (default) or `Constructors`. |

Shows the fastest lap of the session above the table, then positions with time or gap and points.
`type:Constructors` sums each team's points for that race instead. The footer carries the season,
date, lap count and how many drivers retired.

For the same race as an image card, use [`/render-race-results`](image-cards.md#race-result).

## `/qual-results`

Qualifying results for one session.

| Option | Meaning |
|---|---|
| `season` | Season. Omitted = current. |
| `round` | Round. Omitted = latest round with a qualifying session. |
| `session` | Qualifying session in that round. Omitted = the latest one. |

Shows pole position above the table, then positions with gap to pole and each driver's best lap.
There is no constructors view here — qualifying awards no points.

For the same session as an image card, use [`/render-qual-results`](image-cards.md#qualifying).

## `/driver`

Driver profile and statistics. The `driver` option is required; the rest select which slice of the
driver's history you want.

| Option | Meaning |
|---|---|
| `driver` | Driver. Start typing the name and pick from the list. |
| `season` | Statistics from that season only. |
| `multiseason` | Narrow the career to a group of seasons (as defined in your league). |
| `ratings` | Show telemetry ratings. Only works together with `season`. |

Three variants:

* **Career** (no `season`, no `multiseason`) — championships, wins, podiums, poles, best finish,
  seasons and events entered, races finished, total and per-season points, clean-race and
  reliability percentages.
* **Season** (`season` set) — championship position, points and gap, team, starts, races finished,
  best and average race and qualifying positions, DNFs and penalty time. The embed takes the
  driver's team colour for that season.
* **Group of seasons** (`multiseason` set) — the career view, restricted to that group.

!!! note
    If you set both `season` and `multiseason`, `season` wins. Telemetry ratings — pace, consistency,
    attack, defense on a 0–10 scale — exist per season only, so `ratings:true` without `season` just
    says so. A season whose results were entered by hand has no telemetry and therefore no ratings.

## `/head2head`

Compares two drivers over a single season across ten metrics — position, points, wins, podiums,
poles, best finish, average race and qualifying position, fastest laps and DNFs — and tallies who
wins more of them.

| Option | Meaning |
|---|---|
| `driver1` + `driver2` | The two drivers to compare. |
| `team` | Compare a team's own two drivers. Use **instead of** `driver1`/`driver2`. |
| `season` | Season. Omitted = current. |

Pick **either** a team **or** two drivers — not both, and not just one driver. Each metric is marked
for whoever is ahead, and the result reads like *"🏆 Kowalski leads 7–3"*.

## `/season`

Season overview.

| Option | Meaning |
|---|---|
| `season` | Season. Omitted = current. |
| `view` | `Full calendar` (default) or `Upcoming`. |

The full calendar lists every round with its status — ✅ done, ⏭️ skipped, ⏳ upcoming — and its date.
`view:Upcoming` lists only rounds still to come, with Discord's live timestamps: everyone sees the
date in their own time zone plus a countdown that keeps ticking.

## `/league`

Information about the league this server is linked to: how many seasons in total, how many active,
how many archived, and the most recent seasons with their round progress.

## `/ping`

Round-trip time and Discord gateway latency. Useful to confirm the bot is up before assuming a data
command is broken.
