# Link your league

Linking tells the bot which league a Discord server belongs to. One bot serves many leagues, so
every server is linked separately, and each one only ever sees its own data.

All `/setup` subcommands require the **Manage Server** permission, and every reply is private
(only you see it).

## Link the server

1. Generate a **pairing code** in RLT Desktop (Pro Plus league).
2. In your Discord server, run:

```
/setup link code:ABCD1234
```

On success:

> ✅ Linked to **My League**. The bot now serves RLT data for this server.

From this moment on, every data command in that server works against your league.

!!! warning
    A pairing code is **single use** and expires after **60 minutes**. If pairing fails, generate a
    fresh code in RLT Desktop rather than retrying the old one — see
    [Troubleshooting](troubleshooting.md).

### About the league key

Behind the scenes the code is exchanged for your league's API key. The key is stored encrypted and
is **never shown in Discord** — not to you, not to anyone else. You never have to copy or paste a
key yourself.

## Check the link

```
/setup status
```

It re-checks with Racing League Tools and tells you both things that matter: whether the server is
linked, and whether the official bot is enabled for your league.

> ✅ Linked to **My League** — official bot enabled.

If the official bot has been turned off — for example because the league is no longer on Pro Plus —
the reply says so and names the reason. Fix it in Racing League Tools, then run `/setup status`
again to pick up the change immediately.

!!! note
    The bot also re-checks on its own every few hours, so a change on the RLT side is picked up
    eventually even without `/setup status`. Running the command is just the fast path.

## Re-link the server

Generate a new pairing code and run `/setup link` again. This replaces the previous binding for
that server — useful after your league key is rotated, or when the bot reports that the stored key
was rejected.

## Unlink the server

```
/setup remove
```

> 🗑️ Unlinked. The stored key is deleted and the bot no longer has RLT access here.

The stored key is deleted and data commands stop working in that server. Nothing is removed on the
Racing League Tools side, and no league data is affected. To connect again you need a new pairing
code.
