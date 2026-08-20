# Troubleshooting

The bot tries to say exactly what went wrong and who can fix it. This page groups the messages you
are most likely to meet.

## The commands don't appear in Discord

Command lists are cached by the Discord client. Reload it (**Ctrl+R** on desktop) and give it a few
minutes after inviting the bot. If `/setup` in particular is missing, check that you have the
**Manage Server** permission — `/setup` and `/setlang` are hidden from members who don't.

## "This server is not linked to an RLT league yet"

Nobody has paired this server yet. An admin needs to run `/setup link` with a pairing code from RLT
Desktop — see [Link your league](linking.md).

## "The official bot is off for this league"

The server is linked, but Racing League Tools reports that the official bot is not enabled. The
message names the reason:

| Reason | What it means | What to do |
|---|---|---|
| the league is not on Pro Plus | The Public API works on Pro, but the official bot needs **Pro Plus** | Upgrade the league's plan |
| the league API key is inactive | The key exists but is switched off | Re-activate it in Racing League Tools |
| the league API key has expired | The key is past its validity | Issue a new key, then re-link with a fresh pairing code |
| the league's storage is banned | The league's storage was blocked | Contact Racing League Tools support |
| the Public API is disabled for this league | API access is off for the league | Enable it in Racing League Tools |

After fixing it, run `/setup status` to apply the change straight away. Otherwise the bot picks it up
on its own within a few hours.

## Pairing problems

| Message | Meaning | What to do |
|---|---|---|
| RLT rejected that pairing code | Mistyped, already used, or older than 60 minutes | Generate a new code in RLT Desktop |
| RLT refused the pairing | The league doesn't qualify — the reason is named | See the table above |
| Couldn't reach RLT while pairing | The pairing request never got an answer | Run `/setup status` **first**. If the server is linked, you're done; if not, get a new code |
| Pairing failed (RLT HTTP …) | RLT returned an error | The code may be used up — generate a new one before retrying |
| RLT rejected this bot's service key | A problem on the bot operator's side | Nothing you can do; contact the bot operator |
| Server misconfiguration: encryption key missing | The bot instance is not fully configured | Contact the bot operator |

!!! warning
    A pairing code is single use, so the bot never silently retries pairing. If pairing didn't clearly
    succeed, always check `/setup status` before generating another code.

## "RLT rejected the stored league key (401)"

The key the bot holds for this server is no longer accepted — usually because it was rotated or
revoked. An admin should re-link the server with a fresh pairing code.

## Data commands come back empty or fail

| Message | Meaning |
|---|---|
| Couldn't reach the RLT API — it may be down right now | Racing League Tools didn't respond. Try again in a moment |
| Couldn't fetch data (HTTP …) | RLT returned an error for this request |
| Couldn't determine the season | The bot couldn't work out which season to use — pass `season` explicitly |
| This season has no standings yet | No rounds have been classified yet |
| This season has no rounds yet | The calendar is empty |
| This season is finished — no upcoming rounds | Nothing left to count down to in `view:Upcoming` |
| Couldn't find a race / qualifying session for this round | That round has no session of the kind the command handles |
| This is a … session — `/…` only handles … sessions | You pointed a race command at a qualifying session, or vice versa. Practice sessions aren't supported by any command |

Some errors add a small second line with the season, round and session the command was actually
working on. That is the quickest way to see whether the defaults picked what you expected.

## "This session has no live telemetry"

`/render-race-highlights` and `/render-race-strategy` are built from telemetry. The session you asked
for had its results entered by hand, so those cards can't be drawn — use `/render-race-results`, which
works for both kinds. See [Live sessions versus manually entered results](image-cards.md#live-sessions-versus-manually-entered-results).

## Driver and head-to-head messages

| Message | What to do |
|---|---|
| Choose a driver from the suggestions | Pick the driver from the autocomplete list rather than typing a free-form name |
| This driver didn't compete in season … | Choose a different season, or drop `season` for career statistics |
| Ratings are available only with the `season` option | Add `season` — telemetry ratings exist per season |
| No telemetry data for this season | That season's results were entered manually, so there are no ratings |
| Pick **either** a team, **or** driver1 + driver2 | `/head2head` takes a team *or* two drivers, never both and never just one |
| Need two drivers to compare | That team has fewer than two drivers in the season |
| Pick two different drivers | `driver1` and `driver2` are the same person |

## "⏳ Still loading — type again in a second"

Discord gives autocomplete a hard three-second budget, which is not always enough the first time the
bot looks at a season it hasn't touched yet. The data keeps loading in the background — type again a
second later and the full list is there.

If you accept that placeholder instead of a real choice, the command treats the option as if you had
left it empty and falls back to its default.
