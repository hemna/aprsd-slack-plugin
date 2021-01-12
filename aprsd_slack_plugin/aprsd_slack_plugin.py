import logging

from aprsd import plugin
from aprsd.plugins import location as location_plugin
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import aprsd_slack_plugin

LOG = logging.getLogger("APRSD")


class SlackCommandPlugin(plugin.APRSDPluginBase):
    """SlackCommandPlugin.

    This APRSD plugin looks for the location command comming in
    to aprsd, then fetches the caller's location, and then reports
    that location string to the configured slack channel.

    To use this:
        Create a slack bot for your workspace at api.slack.com.
        A good source of information on how to create the app
        and the tokens and permissions and install the app in your
        workspace is here:

            https://api.slack.com/start/building/bolt-python


        You will need the signing secret from the
        Basic Information -> App Credentials form.
        You will also need the Bot User OAuth Access Token from
        OAuth & Permissions -> OAuth Tokens for Your Team ->
        Bot User OAuth Access Token.

        Install the app/bot into your workspace.

        Edit your ~/.config/aprsd/aprsd.yml and add the section
        slack:
            signing_secret: <signing secret token here>
            bot_token: <Bot User OAuth Access Token here>
            channel: <channel name here>
    """

    version = aprsd_slack_plugin.__version__

    # matches any string starting with h or H
    command_regex = "^[lL]"
    command_name = "location-slack"

    def _setup_slack(self):
        """Create the slack require client from config."""

        # signing_secret = self.config["slack"]["signing_secret"]
        if "slack" not in self.config:
            LOG.error("APRSD config is missing slack section")
            return False

        bot_token = self.config["slack"].get("bot_token", None)
        if not bot_token:
            LOG.error(
                "APRSD config is missing slack: bot_token:<token>. "
                "Please install the slack app and get the "
                "Bot User OAth Access Token.",
            )
            return False

        self.swc = WebClient(token=bot_token)

        self.slack_channel = self.config["slack"].get("channel", None)
        if not self.slack_channel:
            LOG.error(
                "APRSD config is missing slack: slack_channel: <name> "
                "Please add a slack channel name to send messages.",
            )
            return False

        return True

    def command(self, fromcall, message, ack):
        LOG.info("SlackCommandPlugin")

        is_setup = self._setup_slack()
        if not is_setup:
            return

        # now call the location plugin to get the location info
        lp = location_plugin.LocationPlugin(self.config)
        location = lp.command(fromcall, message, ack)
        if location:
            reply = location

            LOG.debug("Sending '{}' to slack channel '{}'".format(reply, self.slack_channel))
            try:
                self.swc.chat_postMessage(channel=self.slack_channel, text=reply)
            except SlackApiError as e:
                LOG.error(
                    "Failed to send message to channel '{}' because '{}'".format(
                        self.slack_channel,
                        str(e),
                    ),
                )
        else:
            LOG.debug("SlackCommandPlugin couldn't get location for '{}'".format(fromcall))

        return None
