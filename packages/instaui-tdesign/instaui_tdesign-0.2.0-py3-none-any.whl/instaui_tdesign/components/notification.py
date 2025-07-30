from __future__ import annotations
import typing
from instaui.components.element import Element
from instaui.event.event_mixin import EventMixin
from typing_extensions import TypedDict, Unpack
from ._utils import handle_props, handle_event_from_props

if typing.TYPE_CHECKING:
    from instaui.vars.types import TMaybeRef


class Notification(Element):
    def __init__(
        self,
        content: typing.Optional[TMaybeRef[str]],
        *,
        title: typing.Optional[TMaybeRef[str]] = None,
        **kwargs: Unpack[TNotificationProps],
    ):
        super().__init__("t-notification")
        self.props({"content": content, "title": title})
        self.props(handle_props(kwargs))  # type: ignore
        handle_event_from_props(self, kwargs)  # type: ignore

    def on_close_btn_click(
        self,
        handler: EventMixin,
        *,
        extends: typing.Optional[typing.List] = None,
    ):
        self.on(
            "close_btn_click",
            handler,
            extends=extends,
        )
        return self

    def on_duration_end(
        self,
        handler: EventMixin,
        *,
        extends: typing.Optional[typing.List] = None,
    ):
        self.on(
            "duration_end",
            handler,
            extends=extends,
        )
        return self


class TNotificationProps(TypedDict, total=False):
    close_btn: TMaybeRef[typing.Union[str, bool]]
    duration: TMaybeRef[float]
    footer: TMaybeRef[str]
    icon: TMaybeRef[typing.Union[str, bool]]
    theme: TMaybeRef[typing.Literal["info", "success", "warning", "error"]]
    on_close_btn_click: EventMixin
    on_duration_end: EventMixin
