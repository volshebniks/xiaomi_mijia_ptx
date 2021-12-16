"""Support for xiaomi mijia ptx ."""
import asyncio
from functools import partial
import logging

from homeassistant.components.switch import SwitchEntity

from miio import (  # pylint: disable=import-error
    Device,
    DeviceException,
)
import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchDevice
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_HOST,
    CONF_NAME,
    CONF_TOKEN,
)
from homeassistant.exceptions import PlatformNotReady
import homeassistant.helpers.config_validation as cv

from .ptxswitch import PtxSwitch

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Xiaomi Miio PTX Switch"
DATA_KEY = "switch.xiaomi_mijia_ptx"

CONF_MODEL = "model"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_TOKEN): vol.All(cv.string, vol.Length(min=32, max=32)),
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_MODEL): vol.In(
            [
                "090615.switch.switch01",
                "090615.switch.switch02",
                "090615.switch.switch03",
                "090615.switch.xswitch01",
                "090615.switch.xswitch02",
                "090615.switch.xswitch03",
            ]
        ),
    }
)
ATTR_MODEL = "model"

SUCCESS = ["ok"]

FEATURE_FLAGS_GENERIC = 0

SERVICE_SCHEMA = vol.Schema({vol.Optional(ATTR_ENTITY_ID): cv.entity_ids})


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the switch from config."""
    if DATA_KEY not in hass.data:
        hass.data[DATA_KEY] = {}

    host = config[CONF_HOST]
    token = config[CONF_TOKEN]
    name = config[CONF_NAME]
    model = config.get(CONF_MODEL)

    _LOGGER.info("Initializing with host %s (token %s...)", host, token[:5])

    devices = []
    unique_id = None

    if model is None:
        try:
            miio_device = Device(host, token)
            device_info = await hass.async_add_executor_job(miio_device.info)
            model = device_info.model
            unique_id = f"{model}-{device_info.mac_address}"
            _LOGGER.info(
                "%s %s %s detected",
                model,
                device_info.firmware_version,
                device_info.hardware_version,
            )
        except DeviceException:
            raise PlatformNotReady

    if model in ["090615.switch.switch01","090615.switch.xswitch01"]:
        plug = PtxSwitch(host, token, model=model)
        device = XiaomiPTXSwitch(name, plug, model, unique_id, 1)
        devices.append(device)
        hass.data[DATA_KEY][host] = device
    elif model in ["090615.switch.switch02","090615.switch.xswitch02"]:
        plug = PtxSwitch(host, token, model=model)
        device = XiaomiPTXSwitch(name, plug, model, unique_id, 1)
        devices.append(device)
        hass.data[DATA_KEY][host] = device

        plug2 = PtxSwitch(host, token, model=model)
        device2 = XiaomiPTXSwitch(name, plug2, model, unique_id, 2)
        devices.append(device2)
        hass.data[DATA_KEY][host] = device2

    elif model in ["090615.switch.switch03","090615.switch.xswitch03"]:
        plug = PtxSwitch(host, token, model=model)
        device = XiaomiPTXSwitch(name, plug, model, unique_id, 1)
        devices.append(device)
        hass.data[DATA_KEY][host] = device

        plug2 = PtxSwitch(host, token, model=model)
        device2 = XiaomiPTXSwitch(name, plug2, model, unique_id, 2)
        devices.append(device2)
        hass.data[DATA_KEY][host] = device2

        plug3 = PtxSwitch(host, token, model=model)
        device3 = XiaomiPTXSwitch(name, plug3, model, unique_id, 3)
        devices.append(device3)
        hass.data[DATA_KEY][host] = device3

    else:
        _LOGGER.error(
            "Unsupported device found! Please create an issue at "
            "https://github.com/volshebniks/python-miio-ptx/issues "
            "and provide the following data: %s",
            model,
        )
        return False

    async_add_entities(devices, update_before_add=True)


class XiaomiPTXSwitch(SwitchEntity):
    """Representation of a Xiaomi Plug Generic."""

    def __init__(self, name, plug, model, unique_id, index):
        """Initialize the plug switch."""
        self._name = name
        self._plug = plug
        self._model = model
        self._unique_id = unique_id
        self._index = index

        self._icon = "mdi:power-socket"
        self._available = False
        self._state = None
        if model in ["090615.switch.switch01", "090615.switch.switch02", "090615.switch.switch03",
                        "090615.switch.xswitch01", "090615.switch.xswitch02", "090615.switch.xswitch03"]:
            self._state_attrs = {ATTR_MODEL: self._model}

        self._device_features = FEATURE_FLAGS_GENERIC
        self._skip_update = False

    @property
    def should_poll(self):
        """Poll the plug."""
        return True

    @property
    def unique_id(self):
        """Return an unique ID."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the device if any."""
        return f'{self._name}_{str(self._index)}'

    @property
    def icon(self):
        """Return the icon to use for device if any."""
        return self._icon

    @property
    def available(self):
        """Return true when state is known."""
        return self._available

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    async def _try_command(self, mask_error, func, *args, **kwargs):
        """Call a plug command handling error messages."""
        try:
            result = await self.hass.async_add_executor_job(
                partial(func, *args, **kwargs)
            )

            _LOGGER.debug("Response received from plug: %s", result)

            return result == SUCCESS
        except DeviceException as exc:
            _LOGGER.error(mask_error, exc)
            self._available = False
            return False

    async def async_turn_on(self, **kwargs):
        """Turn the plug on."""
        result = await self._try_command("Turning the plug on failed.", self._plug.turn_switch, self._index, 1)

        if result:
            self._state = True
            self._skip_update = True

    async def async_turn_off(self, **kwargs):
        """Turn the plug off."""
        result = await self._try_command("Turning the plug off failed.", self._plug.turn_switch, self._index, 0)

        if result:
            self._state = False
            self._skip_update = True

    async def async_update(self):
        """Fetch state from the device."""
        # On state change the device doesn't provide the new state immediately.
        if self._skip_update:
            self._skip_update = False
            return

        try:
            state = await self.hass.async_add_executor_job(self._plug.status)
            _LOGGER.debug("Got new state: %s", state)

            self._available = True
            if self._index == 1:
                self._state = state.is_on_1
            elif self._index == 2:
                self._state = state.is_on_2
            elif self._index == 3:
                self._state = state.is_on_3
            else:
                self._state = state.is_on

        except DeviceException as ex:
            self._available = False
            _LOGGER.error("Got exception while fetching the state: %s", ex)
