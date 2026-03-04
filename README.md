# Disclipy

A full-featured Discord client that runs entirely in your terminal, built with Python.

```
____  _          _ _
|  _ \(_)___  ___| (_)_ __  _   _
| | | | / __|/ __| | | '_ \| | | |
| |_| | \__ \ (__| | | |_) | |_| |
|____/|_|___/\___|_|_| .__/ \__, |
                      |_|    |___/
```

## Features

- **Full-screen TUI** — split layout with a chat panel and a channel sidebar
- **Channel sidebar** — shows all channels in the current server with unread message counts highlighted
- **Rich message rendering** — author colors, timestamps, embeds, attachments, and syntax-highlighted code blocks
- **Slash command typeahead** — type `/` to get an autocomplete popup with descriptions for every command
- **Discord app command integration** — the bot's registered slash commands appear in the typeahead alongside local CLI commands
- **Autocomplete everywhere** — `#channels`, `@mentions`, and `:emoji:` (both default Unicode and server custom emoji)
- **Unread notifications** — channels with unread messages are highlighted in the sidebar with a count
- **Mention alerts** — get a notification panel when you're pinged in another channel
- **Keyboard shortcuts** for fast channel navigation
- **Token persistence** — your bot token is saved to `config.ini` so you only enter it once

## Requirements

- Python 3.8+
- A Discord bot token ([create one here](https://discord.com/developers/applications))

## Setup

```bash
git clone https://github.com/your-username/Disclipy.git
cd Disclipy
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python3 Disclipy.py
```

On first run you'll be prompted for your bot token. After that it's saved to `config.ini` and you'll be logged in automatically.

## Commands

| Command | Description |
|---|---|
| `/help` | Show help and keyboard shortcuts |
| `/list_servers` | List joinable servers |
| `/join_server <index>` | Switch to a server by its index |
| `/list_channels` | List channels in the current server |
| `/join_channel #name` | Join a channel by name |
| `/show_pins` | Show pinned messages in the current channel |

All commands show descriptions in the autocomplete popup as you type.

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `Alt+Left` | Switch to previous channel |
| `Alt+Up` | Previous channel in list |
| `Alt+Down` | Next channel in list |
| `Alt+U` | Jump to next unread channel |
| `Ctrl+C` / `Ctrl+D` | Exit |

## Dependencies

- [discord.py](https://discordpy.readthedocs.io/) — Discord API wrapper
- [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/) — TUI input, layout, and completions
- [Rich](https://rich.readthedocs.io/) — terminal text formatting, tables, panels, and syntax highlighting

## Running Tests

```bash
python3 -m unittest tests/test_commands.py
python3 -m unittest tests/test_default_emojis.py
```
