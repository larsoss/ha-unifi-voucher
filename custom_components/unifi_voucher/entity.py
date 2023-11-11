"""UniFi Hotspot Manager entity."""
from __future__ import annotations

from homeassistant.core import callback
from homeassistant.const import (
    ATTR_CONFIGURATION_URL,
    ATTR_NAME,
    ATTR_IDENTIFIERS,
    ATTR_MANUFACTURER,
    ATTR_STATE,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import (
    DOMAIN,
    MANUFACTURER,
    ATTR_EXTRA_STATE_ATTRIBUTES,
    ATTR_AVAILABLE,
    ATTR_LAST_PULL,
)
from .coordinator import UnifiVoucherCoordinator


class UnifiVoucherEntity(CoordinatorEntity):
    """UniFi Hotspot Manager class."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: UnifiVoucherCoordinator,
        entity_type: str,
        entity_key: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)

        self._entry_id = coordinator.get_entry_id()
        self._entity_type = entity_type
        self._entity_key = entity_key

        if entity_key:
            self._unique_id = slugify(f"{self._entry_id}_{entity_key}")
        else:
            self._unique_id = slugify(f"{self._entry_id}")

        self._additional_extra_state_attributes = {}
        self.entity_id = f"{entity_type}.{self._unique_id}"

    def _update_extra_state_attributes(self) -> None:
        """Update extra attributes."""
        self._additional_extra_state_attributes = {}

    def _update_handler(self) -> None:
        """Handle updated data."""
        self._update_extra_state_attributes()

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self._unique_id

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator._available

    @property
    def device_info(self):
        """Return the device info."""
        return {
            ATTR_IDENTIFIERS: {
                (DOMAIN, self._entry_id)
            },
            ATTR_NAME: self.coordinator.get_entry_title(),
            ATTR_MANUFACTURER: MANUFACTURER,
            ATTR_CONFIGURATION_URL: self.coordinator.get_configuration_url(),
        }

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return axtra attributes."""
        _extra_state_attributes = self._additional_extra_state_attributes
        _extra_state_attributes.update(
            {
                ATTR_LAST_PULL: self.coordinator._last_pull,
            }
        )
        return _extra_state_attributes

    async def async_update(self) -> None:
        """Peform async_update."""
        self._update_handler()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_handler()
        self.async_write_ha_state()
