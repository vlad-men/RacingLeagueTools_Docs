# Invite the bot

You need the **Manage Server** permission on the Discord server you are adding the bot to.

RLT Desktop shows the invite link next to the pairing code, so the usual flow is to open both at
the same time. Opening the link takes you to Discord's authorization screen, where you pick the
server and confirm.

!!! tip
    Generate the pairing code and invite the bot in one sitting. The code expires after 60 minutes.

## What the invite asks for

Two scopes, both required — without `applications.commands` the slash commands are never
registered and the bot appears to do nothing:

* `bot`
* `applications.commands`

Four permissions, and nothing else:

| Permission | Why it is needed |
|---|---|
| View Channel | To see the channel a command was used in |
| Send Messages | To reply to commands |
| Embed Links | Every data command replies with an embed |
| Attach Files | The `/render-…` commands upload PNG images |

## What the bot deliberately does not ask for

No Administrator, no Manage Messages, no Read Message History, no Mention Everyone, no voice
permissions, and no privileged intents. It cannot read your channel history, cannot see members'
messages, and cannot touch roles or nicknames.

The bot is purely reactive: it responds to slash commands and never posts on its own.

## After inviting

The commands are registered globally for the bot, so they normally show up right away. If the
autocomplete list looks empty or a command is missing, give Discord a few minutes and reload your
client (**Ctrl+R** on desktop) — command lists are cached client-side.

Next step: [link the server to your league](linking.md).

!!! note
    Data commands stay unavailable until the server is linked. Until then they answer with
    *"This server is not linked to an RLT league yet."*
