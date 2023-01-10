import unittest
from unittest import mock

from aprsd import conf  # noqa

from aprsd_slack_plugin import conf as plugin_conf  # noqa
from aprsd_slack_plugin import location_plugin


class TestPlugin(unittest.TestCase):
    @mock.patch.object(location_plugin.SlackLocationPlugin, "filter")
    def test_plugin(self, mock_command):
        mock_command.return_value = ""

        p = location_plugin.SlackLocationPlugin()
        packet = {"from": "WB4BOR", "message_text": "location"}
        p.filter(packet)
