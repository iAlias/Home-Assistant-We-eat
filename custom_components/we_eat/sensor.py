"""Sensor platform for We Eat."""

from __future__ import annotations

import random
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from . import DOMAIN, CONF_RECIPES

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the We Eat sensor."""
    sensor = WeEatSensor(hass.data[DOMAIN][CONF_RECIPES])
    async_add_entities([sensor], True)

class WeEatSensor(SensorEntity):
    """Representation of the We Eat sensor."""

    def __init__(self, recipes: list[str]) -> None:
        self._recipes = recipes
        self._state = random.choice(recipes)
        self._attr_unique_id = "we_eat_menu"

    async def async_added_to_hass(self) -> None:
        async_dispatcher_connect(self.hass, "we_eat_update", self.pick_random_recipe)

    @property
    def name(self) -> str:
        return "We Eat Menu"

    @property
    def state(self) -> str:
        return self._state

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"recipes": self._recipes}

    def pick_random_recipe(self) -> None:
        if self._recipes:
            self._state = random.choice(self._recipes)
        self.schedule_update_ha_state()
