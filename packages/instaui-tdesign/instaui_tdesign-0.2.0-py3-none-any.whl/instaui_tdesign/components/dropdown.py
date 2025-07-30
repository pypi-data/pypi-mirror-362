from __future__ import annotations
import typing
from instaui.components.element import Element
from instaui.event.event_mixin import EventMixin
from typing_extensions import TypedDict, Unpack, Required
from ._utils import handle_props, handle_event_from_props

if typing.TYPE_CHECKING:
    from instaui.vars.types import TMaybeRef


class Dropdown(Element):
    def __init__(
        self,
        options: TMaybeRef[typing.List[DropdownOptionItem]],
        **kwargs: Unpack[TDropdownProps],
    ):
        super().__init__("t-dropdown")
        self.props({"options": options})

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


class DropdownItem(Element):
    def __init__(
        self,
        content: typing.Optional[str] = None,
        **kwargs: Unpack[TDropdownItemProps],
    ):
        super().__init__("t-dropdown-item")
        self.props({"content": content})

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


class DropdownOptionItem(TypedDict, total=False):
    active: bool
    content: Required[str]
    disabled: bool
    divider: bool
    prefix_icon: str
    theme: typing.Literal["default", "success", "warning", "error"]
    value: Required[int]
    childred: typing.Optional[typing.List[DropdownOptionItem]]


class TDropdownProps(TypedDict, total=False):
    direction: TMaybeRef[typing.Literal["left", "right"]]
    disabled: TMaybeRef[bool]
    hide_after_item_click: TMaybeRef[bool]
    max_column_width: TMaybeRef[typing.Union[float, str]]
    max_height: TMaybeRef[float]
    min_column_width: TMaybeRef[typing.Union[float, str]]
    panel_bottom_content: TMaybeRef[str]
    panel_top_content: TMaybeRef[str]
    placement: TMaybeRef[
        typing.Literal[
            "top",
            "left",
            "right",
            "bottom",
            "top-left",
            "top-right",
            "bottom-left",
            "bottom-right",
            "left-top",
            "left-bottom",
            "right-top",
            "right-bottom",
        ]
    ]
    popup_props: typing.Dict
    trigger: TMaybeRef[typing.Literal["hover", "click", "focus", "context-menu"]]
    on_click: EventMixin


class TDropdownItemProps(TypedDict, total=False):
    active: TMaybeRef[bool]
    disabled: TMaybeRef[bool]
    divider: TMaybeRef[bool]
    prefix_icon: TMaybeRef[str]
    theme: TMaybeRef[typing.Literal["default", "success", "warning", "error"]]
    value: TMaybeRef[int]
    on_click: EventMixin
