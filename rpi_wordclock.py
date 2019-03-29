import logging
import voluptuous as vol
import requests

from homeassistant.components.light import ATTR_BRIGHTNESS, ATTR_COLOR_TEMP, Light, PLATFORM_SCHEMA, SUPPORT_BRIGHTNESS, SUPPORT_COLOR_TEMP
from homeassistant.const import CONF_HOST, CONF_NAME
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """
    Setup the rpi_wordclock platform.
    """

    # Assign configuration variables. The configuration check takes care they are present.
    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)

    # Setup connection with devices/cloud
    api_endpoint = 'http://' + host + '/api'

    # Add devices
    add_devices([RpiWordclock(name, api_endpoint)])
    _LOGGER.info("Added rpi_wordclock light at " + host)


class RpiWordclock(Light):
    """
    Representation of an raspberry pi wordclock Light.
    """

    def __init__(self, name, api_endpoint):
        """
        Initialize an raspberry pi wordclock light.
        """

        self._name = name
        self._state = None
        self._brightness = None
        self._off_brightness = 15
        self._api_endpoint = api_endpoint

    @property
    def name(self):
        """
        Return the display name of this light.
        """
        return self._name

    @property
    def brightness(self):
        """
        Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def supported_features(self):
        """
        Flag supported features.
        """
        return SUPPORT_BRIGHTNESS | SUPPORT_COLOR_TEMP

    @property
    def is_on(self):
        """
        Return true if light is on.
        """
        return self._state

    def turn_on(self, **kwargs):
        """
        Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        if ATTR_BRIGHTNESS in kwargs:
            r = requests.post(self._api_endpoint + '/brightness' , json={"brightness": kwargs[ATTR_BRIGHTNESS]})
            self.log(r)

        else:
            r = requests.post(self._api_endpoint + '/brightness' , json={"brightness": 250})
            self.log(r)

        if ATTR_COLOR_TEMP in kwargs:
            _LOGGER.info("Temp: " + str(kwargs[ATTR_COLOR_TEMP]))
            kelvin = int(1000000.0/kwargs[ATTR_COLOR_TEMP])
            r = requests.post(self._api_endpoint + '/color_temperature' , json={"color_temperature": kelvin})
            self.log(r)

    def turn_off(self, **kwargs):
        """
        Instruct the light to turn off.
        """
        r = requests.post(self._api_endpoint + '/brightness' , json={"brightness": self._off_brightness})
        self.log(r)

    def update(self):
        """
        Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        r = requests.get(self._api_endpoint + '/brightness')
        self.log(r)
        self._brightness = int(r.text)
        self._state = True if self._brightness > self._off_brightness else False

    def log(self, reply):
        _LOGGER.info("Communication with rpi_wordclock " + self._name + " succeeded.")
        _LOGGER.info(reply.text)
        if not reply.status_code == requests.codes.ok:
            _LOGGER.error("Communication with rpi_wordclock " + self._name + " failed.")
