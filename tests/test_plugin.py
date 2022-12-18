import sys
import unittest

from aprsd_slack_plugin import location_plugin


if sys.version_info >= (3, 2):
    from unittest import mock
else:
    from unittest import mock


class TestPlugin(unittest.TestCase):
    @mock.patch.object(location_plugin.SlackLocationPlugin, "filter")
    def test_plugin(self, mock_command):
        mock_command.return_value = ""

        config = {
            "slack": {"signing_secret": "something", "bot_token": "sometoken", "channel": "hemna"},
        }

        p = location_plugin.SlackLocationPlugin(config)
        packet = {"from": "WB4BOR", "message_text": "location"}
        p.filter(packet)
