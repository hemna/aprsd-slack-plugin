import logging

from aprsd import messaging, plugin

import aprsd_slack_plugin
from aprsd_slack_plugin import base_plugin

LOG = logging.getLogger("APRSD")


class SlackNotifyPlugin(
    base_plugin.SlackPluginBase,
    plugin.APRSDNotificationPluginBase,
):
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

    def notify(self, packet):
        LOG.info("SlackCommandPlugin")

        fromcall = packet["from"]
        # message = packet["message_text"]

        is_setup = self.setup_slack()
        if not is_setup:
            return

        # get last location of a callsign, get descriptive name from weather service

        callsign_url = "<http://aprs.fi/info/a/{}|{}>".format(fromcall, fromcall)

        message = {}
        message["username"] = "APRSD - Slack Notification Plugin"
        message["icon_emoji"] = ":satellite_antenna:"
        message["attachments"] = [{}]
        message["text"] = "{} - Is now on APRS".format(callsign_url)
        message["channel"] = "#hemna"

        LOG.debug(message)

        # self.swc.chat_postMessage(**message)
        for channel in self.slack_channels:
            message["channel"] = channel
            self.swc.chat_postMessage(**message)

        # Don't have aprsd try and send a reply
        return messaging.NULL_MESSAGE
