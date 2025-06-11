"""We Eat custom integration for Home Assistant."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "we_eat"
CONF_RECIPES = "recipes"

DEFAULT_RECIPES = [
    "Spaghetti",
    "Pizza",
    "Risotto",
]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the We Eat integration."""
    conf = config.get(DOMAIN, {})
    recipes = conf.get(CONF_RECIPES, DEFAULT_RECIPES)
    hass.data[DOMAIN] = {
        CONF_RECIPES: list(recipes),
    }

    async_load_platform(hass, "sensor", DOMAIN, {}, config)

    @callback
    def update_lunch(now: datetime) -> None:
        _LOGGER.debug("Updating lunch recipe")
        async_dispatcher_send(hass, "we_eat_update")

    @callback
    def update_dinner(now: datetime) -> None:
        _LOGGER.debug("Updating dinner recipe")
        async_dispatcher_send(hass, "we_eat_update")

    async_track_time_change(hass, update_lunch, hour=12, minute=0, second=0)
    async_track_time_change(hass, update_dinner, hour=19, minute=0, second=0)

    async def handle_add(call: Any) -> None:
        recipe = call.data.get("recipe")
        if recipe:
            hass.data[DOMAIN][CONF_RECIPES].append(recipe)
            async_dispatcher_send(hass, "we_eat_update")

    async def handle_remove(call: Any) -> None:
        recipe = call.data.get("recipe")
        if recipe and recipe in hass.data[DOMAIN][CONF_RECIPES]:
            hass.data[DOMAIN][CONF_RECIPES].remove(recipe)
            async_dispatcher_send(hass, "we_eat_update")

    async def handle_set(call: Any) -> None:
        recipes = call.data.get(CONF_RECIPES, [])
        if isinstance(recipes, list):
            hass.data[DOMAIN][CONF_RECIPES] = list(recipes)
            async_dispatcher_send(hass, "we_eat_update")

    hass.services.async_register(DOMAIN, "add_recipe", handle_add)
    hass.services.async_register(DOMAIN, "remove_recipe", handle_remove)
    hass.services.async_register(DOMAIN, "set_recipes", handle_set)

    return True
