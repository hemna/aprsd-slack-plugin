import sys
import unittest

from aprsd_slack_plugin import aprsd_slack_plugin as slack_plugin

if sys.version_info >= (3, 2):
    from unittest import mock
else:
    from unittest import mock


class TestPlugin(unittest.TestCase):
    @mock.patch.object(slack_plugin.SlackCommandPlugin, "command")
    def test_plugin(self, mock_command):
        mock_command.return_value = ""

        config = {
            "slack": {"signing_secret": "something", "bot_token": "sometoken", "channel": "hemna"},
        }

        p = slack_plugin.SlackCommandPlugin(config)
        p.command("KM6LYW", "location", 1)
