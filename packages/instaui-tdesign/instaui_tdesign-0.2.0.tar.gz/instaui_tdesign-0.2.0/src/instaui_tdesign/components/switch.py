from __future__ import annotations
import typing
from instaui.components.element import Element
from instaui.event.event_mixin import EventMixin
from typing_extensions import TypedDict, Unpack

from ._utils import handle_props, handle_event_from_props, try_setup_vmodel


class Switch(Element):
    def __init__(
        self,
        value: typing.Optional[bool] = None,
        *,
        model_value: typing.Optional[bool] = None,
        **kwargs: Unpack[TSwitchProps],
    ):
        super().__init__("t-switch")

        try_setup_vmodel(self, value)

        self.props(handle_props(kwargs, model_value=model_value))  # type: ignore
        handle_event_from_props(self, kwargs)  # type: ignore

    def on_change(
        self,
        handler: EventMixin,
        *,
        extends: typing.Optional[typing.List] = None,
    ):
        self.on(
            "change",
            handler,
            extends=extends,
        )
        return self


class TSwitchProps(TypedDict, total=False):
    before_change: str
    custom_value: typing.List
    disabled: bool
    label: typing.Union[str, typing.List]
    loading: bool
    size: typing.Literal["small", "medium", "large"]
    default_value: typing.Literal["number"]
    on_change: EventMixin
