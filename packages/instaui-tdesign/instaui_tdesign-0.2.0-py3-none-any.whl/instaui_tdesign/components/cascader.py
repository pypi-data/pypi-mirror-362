from __future__ import annotations
import typing
from instaui.components.element import Element
from instaui.event.event_mixin import EventMixin
from typing_extensions import TypedDict, Unpack
from ._utils import handle_props, handle_event_from_props, try_setup_vmodel

if typing.TYPE_CHECKING:
    from instaui.vars.types import TMaybeRef


class Cascader(Element):
    def __init__(
        self,
        value: typing.Optional[TMaybeRef[typing.Union[int, str]]] = None,
        **kwargs: Unpack[TCascaderProps],
    ):
        super().__init__("t-cascader")

        try_setup_vmodel(self, value)

        self.props(handle_props(kwargs))  # type: ignore
        handle_event_from_props(self, kwargs)  # type: ignore

    def on_blur(
        self,
        handler: EventMixin,
        *,
        extends: typing.Optional[typing.List] = None,
    ):
        self.on(
            "blur",
            handler,
            extends=extends,
        )
        return self

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

    def on_focus(
        self,
        handler: EventMixin,
        *,
        extends: typing.Optional[typing.List] = None,
    ):
        self.on(
            "focus",
            handler,
            extends=extends,
        )
        return self

    def on_popup_visible_change(
        self,
        handler: EventMixin,
        *,
        extends: typing.Optional[typing.List] = None,
    ):
        self.on(
            "popup_visible_change",
            handler,
            extends=extends,
        )
        return self

    def on_remove(
        self,
        handler: EventMixin,
        *,
        extends: typing.Optional[typing.List] = None,
    ):
        self.on(
            "remove",
            handler,
            extends=extends,
        )
        return self


class TCascaderProps(TypedDict, total=False):
    autofocus: TMaybeRef[bool]
    borderless: TMaybeRef[bool]
    check_props: typing.Dict
    check_strictly: TMaybeRef[bool]
    clearable: TMaybeRef[bool]
    collapsed_items: TMaybeRef[str]
    disabled: TMaybeRef[bool]
    empty: TMaybeRef[str]
    filter: TMaybeRef[str]
    filterable: TMaybeRef[bool]
    input_props: typing.Dict
    keys: typing.Dict
    label: TMaybeRef[str]
    lazy: TMaybeRef[bool]
    load: TMaybeRef[str]
    loading: TMaybeRef[bool]
    loading_text: TMaybeRef[str]
    max: TMaybeRef[float]
    min_collapsed_num: TMaybeRef[float]
    multiple: TMaybeRef[bool]
    option: TMaybeRef[str]
    options: typing.List
    panel_bottom_content: TMaybeRef[str]
    panel_top_content: TMaybeRef[str]
    placeholder: TMaybeRef[str]
    popup_props: typing.Dict
    popup_visible: TMaybeRef[bool]
    default_popup_visible: TMaybeRef[bool]
    prefix_icon: TMaybeRef[str]
    readonly: TMaybeRef[bool]
    reserve_keyword: TMaybeRef[bool]
    select_input_props: typing.Dict
    show_all_levels: TMaybeRef[bool]
    size: typing.Literal["large", "medium", "small"]
    status: typing.Literal["default", "success", "warning", "error"]
    suffix: TMaybeRef[str]
    suffix_icon: TMaybeRef[str]
    tag_input_props: typing.Dict
    tag_props: typing.Dict
    tips: TMaybeRef[str]
    trigger: TMaybeRef[typing.Literal["click", "hover"]]
    default_value: TMaybeRef[typing.Union[int, str]]
    value_display: TMaybeRef[str]
    value_mode: TMaybeRef[typing.Literal["onlyLeaf", "parentFirst", "all"]]
    value_type: TMaybeRef[typing.Literal["single", "full"]]
    on_blur: EventMixin
    on_change: EventMixin
    on_focus: EventMixin
    on_popup_visible_change: EventMixin
    on_remove: EventMixin
