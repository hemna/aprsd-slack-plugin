# aprsd_slack_plugin

[![Python CI](https://github.com/hemna/aprsd-slack-plugin/workflows/python/badge.svg)](https://github.com/hemna/aprsd-slack-plugin/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)

This project is a Python plugin for the [APRSD server daemon](https://github.com/craigerl/aprsd) written by Craig Lamparter. The plugin provides integration with Slack, allowing APRS messages and location data to be forwarded to Slack channels.

## Features

The plugin includes three main components:

1. **Location Plugin** - Reports APRS location data to Slack channels with weather information
2. **Message Plugin** - Forwards APRS messages to Slack channels
3. **Notify Plugin** - Sends notifications when watched callsigns appear on APRS

## Requirements

- Python 3.11+
- [APRSD](https://github.com/craigerl/aprsd) - APRS daemon server
- Slack Bot Token and Signing Secret (see setup instructions below)

## Installation

Install the plugin using pip:

```bash
pip install aprsd-slack-plugin
```

Or install from source:

```bash
git clone https://github.com/hemna/aprsd-slack-plugin.git
cd aprsd-slack-plugin
pip install -e .
```

## Slack Bot Setup

Before configuring the plugin, you need to create a Slack bot application:

1. Go to [api.slack.com](https://api.slack.com/apps) and create a new app
2. A good guide for creating the app, tokens, and permissions can be found at:
   [https://api.slack.com/start/building/bolt-python](https://api.slack.com/start/building/bolt-python)

3. You will need:
   - **Signing Secret**: Found in "Basic Information" → "App Credentials"
   - **Bot User OAuth Token**: Found in "OAuth & Permissions" → "OAuth Tokens for Your Team" → "Bot User OAuth Access Token"

4. Required Bot Token Scopes:
   - `chat:write` - To post messages to channels
   - `channels:read` (optional) - To read channel information

5. Install the app/bot into your workspace

## Configuration

Add the following section to your APRSD configuration file (typically `~/.config/aprsd/aprsd.conf` or `~/.config/aprsd/aprsd.yml`):

### YAML Configuration Format

```yaml
aprsd_slack_plugin:
  signing_secret: "your_slack_signing_secret_here"
  bot_token: "xoxb-your-bot-token-here"
  channels:
    - "#general"
    - "#aprs"
    - "#hamradio"
```

### INI Configuration Format

```ini
[aprsd_slack_plugin]
signing_secret = your_slack_signing_secret_here
bot_token = xoxb-your-bot-token-here
channels = #general,#aprs,#hamradio
```

### Configuration Options

- **`signing_secret`** (required): Your Slack app's signing secret from the App Credentials page
- **`bot_token`** (required): Your Slack bot's OAuth token (starts with `xoxb-`)
- **`channels`** (required): List of Slack channel names (with or without `#` prefix) where messages will be posted

## Usage

Once configured, the plugin will automatically integrate with APRSD. The plugins respond to specific APRS message commands:

### Location Plugin

The Location Plugin responds to messages starting with `L` or `l` and reports the location of a callsign to Slack.

**Command Format:**
```
L [callsign]
```

**Examples:**

1. Get your own location:
   ```
   L
   ```

2. Get location for a specific callsign:
   ```
   L N0CALL
   ```

**Slack Output:**
The plugin will post a formatted message to your configured Slack channels with:
- Callsign with link to aprs.fi
- Location description (from weather.gov if in US)
- Map link to aprs.fi
- Altitude in feet
- Time since last update

**Example Slack Message:**
```
APRSD - Slack Location Plugin
📍 N0CALL - Location

Location: Downtown Denver, CO
Map Location: http://aprs.fi/...
Altitude: 5280 ft
Time: 2.3 h ago
```

### Message Plugin

The Message Plugin forwards APRS messages to Slack channels.

**Command Format:**
```
s <message>
slack <message>
```

**Examples:**

1. Send a simple message:
   ```
   s Hello from APRS!
   ```

2. Send a longer message:
   ```
   slack Testing the Slack integration
   ```

**Slack Output:**
The plugin will post a message showing the callsign and message content:

```
APRSD - Slack Message Plugin
📡 N0CALL says s Hello from APRS!
```

### Notify Plugin

The Notify Plugin automatically sends notifications when callsigns on your watchlist appear on APRS.

**Setup:**
Add callsigns to your APRSD watchlist configuration. When those callsigns appear on APRS, the plugin will automatically notify your Slack channels.

**Slack Output:**
```
APRSD - Slack Notification Plugin
📡 N0CALL - Is now on APRS
```

## Example Interactions

### Example 1: Checking Your Location

**APRS Message:**
```
L
```

**Slack Output:**
```
APRSD - Slack Location Plugin
📍 N0CALL - Location

Location: Mountain View, CA
Map Location: http://aprs.fi/#!mt=roadmap&z=15&lat=37.4056&lng=-122.0775
Altitude: 150 ft
Time: 0.5 h ago
```

### Example 2: Checking Another Station's Location

**APRS Message:**
```
L W1AW
```

**Slack Output:**
```
APRSD - Slack Location Plugin
📍 W1AW - Location

Location: Newington, CT
Map Location: http://aprs.fi/#!mt=roadmap&z=15&lat=41.6875&lng=-72.7278
Altitude: 200 ft
Time: 1.2 h ago
```

### Example 3: Sending a Message to Slack

**APRS Message:**
```
s Just finished a QSO on 2m!
```

**Slack Output:**
```
APRSD - Slack Message Plugin
📡 N0CALL says s Just finished a QSO on 2m!
```

### Example 4: Watchlist Notification

When a callsign on your watchlist appears on APRS, you'll automatically receive:

**Slack Output:**
```
APRSD - Slack Notification Plugin
📡 W1AW - Is now on APRS
```

## Troubleshooting

### Plugin Not Responding

1. Check that the plugin is enabled in your APRSD configuration
2. Verify your Slack credentials are correct:
   - `signing_secret` matches your app's signing secret
   - `bot_token` is valid and starts with `xoxb-`
3. Ensure the bot is installed in your Slack workspace
4. Check APRSD logs for error messages

### Messages Not Appearing in Slack

1. Verify the channel names are correct (case-sensitive)
2. Ensure the bot has been invited to the channels (if they're private)
3. Check that the bot has `chat:write` scope
4. Verify the bot token hasn't expired

### Location Plugin Not Working

1. Ensure you have an `aprs_fi.apiKey` configured in APRSD
2. Check that the callsign exists on aprs.fi
3. Verify network connectivity to aprs.fi and weather.gov

## Development

### Running Tests

```bash
tox
```

Or run specific test environments:

```bash
tox -e py311      # Run Python 3.11 tests
tox -e lint       # Run linting with ruff
tox -e type-check # Run type checking with mypy
```

### Code Style

This project uses:
- [black](https://black.readthedocs.io/) for code formatting
- [ruff](https://docs.astral.sh/ruff/) for linting
- [isort](https://pycqa.github.io/isort/) for import sorting

## License

Licensed under the Apache License, Version 2.0. See LICENSE.txt for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- GitHub Issues: [https://github.com/hemna/aprsd-slack-plugin/issues](https://github.com/hemna/aprsd-slack-plugin/issues)

## Related Projects

- [APRSD](https://github.com/craigerl/aprsd) - The APRS daemon this plugin extends
