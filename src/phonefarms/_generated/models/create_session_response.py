from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.create_session_response_proxy_type_0 import (
        CreateSessionResponseProxyType0,
    )


T = TypeVar("T", bound="CreateSessionResponse")


@_attrs_define
class CreateSessionResponse:
    """
    Attributes:
        session_id (str):
        phone_id (str):
        proxy (CreateSessionResponseProxyType0 | None | Unset):
    """

    session_id: str
    phone_id: str
    proxy: CreateSessionResponseProxyType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_session_response_proxy_type_0 import (
            CreateSessionResponseProxyType0,
        )

        session_id = self.session_id

        phone_id = self.phone_id

        proxy: dict[str, Any] | None | Unset
        if isinstance(self.proxy, Unset):
            proxy = UNSET
        elif isinstance(self.proxy, CreateSessionResponseProxyType0):
            proxy = self.proxy.to_dict()
        else:
            proxy = self.proxy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "session_id": session_id,
                "phone_id": phone_id,
            }
        )
        if proxy is not UNSET:
            field_dict["proxy"] = proxy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_session_response_proxy_type_0 import (
            CreateSessionResponseProxyType0,
        )

        d = dict(src_dict)
        session_id = d.pop("session_id")

        phone_id = d.pop("phone_id")

        def _parse_proxy(
            data: object,
        ) -> CreateSessionResponseProxyType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                proxy_type_0 = CreateSessionResponseProxyType0.from_dict(data)

                return proxy_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CreateSessionResponseProxyType0 | None | Unset, data)

        proxy = _parse_proxy(d.pop("proxy", UNSET))

        create_session_response = cls(
            session_id=session_id,
            phone_id=phone_id,
            proxy=proxy,
        )

        create_session_response.additional_properties = d
        return create_session_response

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
