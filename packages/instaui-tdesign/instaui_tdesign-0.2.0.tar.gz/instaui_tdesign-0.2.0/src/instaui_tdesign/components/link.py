from __future__ import annotations
import typing
from instaui.components.element import Element
from instaui.event.event_mixin import EventMixin
from typing_extensions import TypedDict, Unpack
from ._utils import handle_props, handle_event_from_props

if typing.TYPE_CHECKING:
    from instaui.vars.types import TMaybeRef


class Link(Element):
    def __init__(
        self,
        *,
        href: typing.Optional[TMaybeRef[str]] = None,
        content: typing.Optional[TMaybeRef[str]] = None,
        **kwargs: Unpack[TLinkProps],
    ):
        super().__init__("t-link")
        self.props({"content": content, "href": href})

        self.props(handle_props(kwargs))  # type: ignore
        handle_event_from_props(self, kwargs)  # type: ignore

    def on_click(
        self,
        handler: EventMixin,
        *,
        extends: typing.Optional[typing.List] = None,
    ):
        self.on(
            "click",
            handler,
            extends=extends,
        )
        return self


class TLinkProps(TypedDict, total=False):
    disabled: TMaybeRef[bool]
    download: TMaybeRef[typing.Union[bool, str]]
    hover: TMaybeRef[typing.Literal["color", "underline"]]
    prefix_icon: TMaybeRef[str]
    size: TMaybeRef[typing.Literal["small", "medium", "large"]]
    suffix_icon: TMaybeRef[str]
    target: TMaybeRef[str]
    theme: TMaybeRef[
        typing.Literal["default", "primary", "danger", "warning", "success"]
    ]
    underline: TMaybeRef[bool]
    on_click: EventMixin
