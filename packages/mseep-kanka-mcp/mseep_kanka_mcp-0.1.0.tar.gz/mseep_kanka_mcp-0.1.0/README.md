# Kanka MCP - Model Context Protocol Server for Kanka API

This project provides an MCP (Model Context Protocol) server for interacting with the [Kanka](https://kanka.io) API. It allows AI assistants to manage campaigns, characters, locations, posts, notes, and journals in your Kanka worldbuilding projects.

## Features

The server provides tools for working with:
- Campaigns: List all user campaigns
- Characters: List, retrieve, create, update, and delete characters
- Locations: List, retrieve, create, update, and delete locations 
- Posts: List, retrieve, create, update, and delete posts for any entity
- Notes: List, retrieve, create, update, and delete notes
- Journals: List, retrieve, create, update, and delete journals

All create and update operations properly handle HTML content for description fields and support privacy settings.

## Installation

### Prerequisites

- Python 3.10+

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/kanka_mcp.git
   cd kanka_mcp
   ```

2. Install dependencies:
   ```
   pip install requests mcp[cli]
   ```

   Or if you have a pyproject.toml file:
   ```
   pip install .
   ```

### Configuration

You need to set the `KANKA_API_KEY` environment variable with your Kanka API key:

```bash
export KANKA_API_KEY=your_kanka_api_key
```

To get your Kanka API key:
1. Log in to your Kanka account
2. Go to "Account Settings"
3. Navigate to the "API" section
4. Create or copy your API token

## Usage

### Running the MCP Server

Run the server directly with:

```bash
python kanka_mcp.py
```

### Adding to MCP Server Configuration

Add the following to your MCP server configuration:

```json
"kanka": {
    "command": "python",
    "args": [
        "FULL_PATH_TO_SCRIPT_FOLDER/kanka_mcp.py"
    ],
    "env": {
        "KANKA_API_KEY": "YOUR_KANKA_API_KEY"
    }
}
```

Replace `FULL_PATH_TO_SCRIPT_FOLDER` with the absolute path to the directory containing the `kanka_mcp.py` script, and `YOUR_KANKA_API_KEY` with your actual Kanka API key.

## Available Tools

### Campaigns

- `show_campaigns()`: List all campaigns the user has access to.

### Characters

- `list_characters(campaign_id)`: List all characters in a campaign.
- `get_character(campaign_id, character_id)`: Get a specific character by ID.
- `create_character(campaign_id, name, ...)`: Create a new character.
- `update_character(campaign_id, character_id, ...)`: Update an existing character.
- `delete_character(campaign_id, character_id)`: Delete a character.

### Locations

- `list_locations(campaign_id)`: List all locations in a campaign.
- `get_location(campaign_id, location_id)`: Get a specific location by ID.
- `create_location(campaign_id, name, ...)`: Create a new location.
- `update_location(campaign_id, location_id, ...)`: Update an existing location.
- `delete_location(campaign_id, location_id)`: Delete a location.

### Posts

- `list_posts(campaign_id, entity_id)`: List all posts for an entity.
- `get_post(campaign_id, entity_id, post_id)`: Get a specific post by ID.
- `create_post(campaign_id, entity_id, name, ...)`: Create a new post.
- `update_post(campaign_id, entity_id, post_id, ...)`: Update an existing post.
- `delete_post(campaign_id, entity_id, post_id)`: Delete a post.

### Notes

- `list_notes(campaign_id)`: List all notes in a campaign.
- `get_note(campaign_id, note_id)`: Get a specific note by ID.
- `create_note(campaign_id, name, ...)`: Create a new note.
- `update_note(campaign_id, note_id, ...)`: Update an existing note.
- `delete_note(campaign_id, note_id)`: Delete a note.

### Journals

- `list_journals(campaign_id)`: List all journals in a campaign.
- `get_journal(campaign_id, journal_id)`: Get a specific journal by ID.
- `create_journal(campaign_id, name, ...)`: Create a new journal.
- `update_journal(campaign_id, journal_id, ...)`: Update an existing journal.
- `delete_journal(campaign_id, journal_id)`: Delete a journal.

## License

This project is licensed under the terms specified in the LICENSE file.
