"""Tests for the Wemo standalone/non-bridge light entity."""

import pytest

from homeassistant.components.homeassistant import (
    DOMAIN as HA_DOMAIN,
    SERVICE_UPDATE_ENTITY,
)
from homeassistant.const import ATTR_ENTITY_ID, STATE_OFF, STATE_ON
from homeassistant.setup import async_setup_component


@pytest.fixture
def pywemo_model():
    """Pywemo Dimmer models use the light platform (WemoDimmer class)."""
    return "Dimmer"


async def test_light_registry_state_callback(
    hass, pywemo_registry, pywemo_device, wemo_entity
):
    """Verify that the light receives state updates from the registry."""
    # On state.
    pywemo_device.get_state.return_value = 1
    pywemo_registry.callbacks[pywemo_device.name](pywemo_device, "", "")
    await hass.async_block_till_done()
    assert hass.states.get(wemo_entity.entity_id).state == STATE_ON

    # Off state.
    pywemo_device.get_state.return_value = 0
    pywemo_registry.callbacks[pywemo_device.name](pywemo_device, "", "")
    await hass.async_block_till_done()
    assert hass.states.get(wemo_entity.entity_id).state == STATE_OFF


async def test_light_update_entity(hass, pywemo_registry, pywemo_device, wemo_entity):
    """Verify that the light performs state updates."""
    await async_setup_component(hass, HA_DOMAIN, {})

    # On state.
    pywemo_device.get_state.return_value = 1
    await hass.services.async_call(
        HA_DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {ATTR_ENTITY_ID: [wemo_entity.entity_id]},
        blocking=True,
    )
    assert hass.states.get(wemo_entity.entity_id).state == STATE_ON

    # Off state.
    pywemo_device.get_state.return_value = 0
    await hass.services.async_call(
        HA_DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {ATTR_ENTITY_ID: [wemo_entity.entity_id]},
        blocking=True,
    )
    assert hass.states.get(wemo_entity.entity_id).state == STATE_OFF
