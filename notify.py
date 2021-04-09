"""Twilio Notify API platform for notify component."""
import logging

from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TARGET,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)

from homeassistant.components.twilio import DATA_TWILIO

_LOGGER = logging.getLogger(__name__)

CONF_NOTIFY_SID = "notify_sid"
ATTR_MEDIAURL = "media_url"
ATTR_IDENTITY = "identity"


def get_service(hass, config, discovery_info=None):
    """Get the Twilio Notify API notification service."""
    _LOGGER.info("Getting Twilio Notify API Service")
    return TwilioNotifyAPIService(
        hass.data[DATA_TWILIO], config[CONF_NOTIFY_SID]
    )


class TwilioNotifyAPIService(BaseNotificationService):
    """Implement the notification service for the Twilio Notify API service."""

    def __init__(self, twilio_client, notify_sid):
        """Initialize the service."""
        _LOGGER.info("Init Twilio Notify API Service")
        self.client = twilio_client
        self.notify_sid = notify_sid

    def send_message(self, message="", **kwargs):
        """Send SMS to specified target user cell."""
        targets = kwargs.get(ATTR_TARGET)
        data = kwargs.get(ATTR_DATA) or {}
        identities = None
        if ATTR_IDENTITY in data:
            identities = data[ATTR_IDENTITY]

        _LOGGER.info("Sending message " + message + "to Twilio Notify API Service")
        if not targets and not identities:
            _LOGGER.info("At least 1 target or 1 identity is required")
            return
        elif not identities:
            _LOGGER.debug("Sending message " + message + "to Twilio Notify API Service to tags " + ', '.join(map(str, targets)))
            self.client.notify.services(self.notify_sid).notifications.create(tag=targets, body=message)    
        elif not targets:
            _LOGGER.debug("Sending message " + message + "to Twilio Notify API Service to identites " + ', '.join(map(str, identities)))
            self.client.notify.services(self.notify_sid).notifications.create(identity=identities, body=message)    
        else:
            _LOGGER.debug("Sending message " + message + "to Twilio Notify API Service to identites " + ', '.join(map(str, identities)) + " and tags " + ', '.join(map(str, targets)))
            self.client.notify.services(self.notify_sid).notifications.create(tag=targets, identify=identities, body=message)
