from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="SlotDetail")


@_attrs_define
class SlotDetail:
    """
    Attributes:
        id (str):
        phone_id (str):
        phone_name (None | str):
        phone_serial (str):
        phone_status (str):
        status (str):
        setup_name (str):
        cluster_id (str):
        cluster_name (None | str):
        owner (str):
        has_active_session (bool):
        tunnel_url (None | str):
        created_at (str):
        updated_at (str):
    """

    id: str
    phone_id: str
    phone_name: None | str
    phone_serial: str
    phone_status: str
    status: str
    setup_name: str
    cluster_id: str
    cluster_name: None | str
    owner: str
    has_active_session: bool
    tunnel_url: None | str
    created_at: str
    updated_at: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        phone_id = self.phone_id

        phone_name: None | str
        phone_name = self.phone_name

        phone_serial = self.phone_serial

        phone_status = self.phone_status

        status = self.status

        setup_name = self.setup_name

        cluster_id = self.cluster_id

        cluster_name: None | str
        cluster_name = self.cluster_name

        owner = self.owner

        has_active_session = self.has_active_session

        tunnel_url: None | str
        tunnel_url = self.tunnel_url

        created_at = self.created_at

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "phone_id": phone_id,
                "phone_name": phone_name,
                "phone_serial": phone_serial,
                "phone_status": phone_status,
                "status": status,
                "setup_name": setup_name,
                "cluster_id": cluster_id,
                "cluster_name": cluster_name,
                "owner": owner,
                "has_active_session": has_active_session,
                "tunnel_url": tunnel_url,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        phone_id = d.pop("phone_id")

        def _parse_phone_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_name = _parse_phone_name(d.pop("phone_name"))

        phone_serial = d.pop("phone_serial")

        phone_status = d.pop("phone_status")

        status = d.pop("status")

        setup_name = d.pop("setup_name")

        cluster_id = d.pop("cluster_id")

        def _parse_cluster_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        cluster_name = _parse_cluster_name(d.pop("cluster_name"))

        owner = d.pop("owner")

        has_active_session = d.pop("has_active_session")

        def _parse_tunnel_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        tunnel_url = _parse_tunnel_url(d.pop("tunnel_url"))

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        slot_detail = cls(
            id=id,
            phone_id=phone_id,
            phone_name=phone_name,
            phone_serial=phone_serial,
            phone_status=phone_status,
            status=status,
            setup_name=setup_name,
            cluster_id=cluster_id,
            cluster_name=cluster_name,
            owner=owner,
            has_active_session=has_active_session,
            tunnel_url=tunnel_url,
            created_at=created_at,
            updated_at=updated_at,
        )

        slot_detail.additional_properties = d
        return slot_detail

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
