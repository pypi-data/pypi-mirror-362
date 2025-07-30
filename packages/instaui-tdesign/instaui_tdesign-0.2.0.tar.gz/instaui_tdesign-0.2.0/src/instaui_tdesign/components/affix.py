from __future__ import annotations
import typing
from instaui.components.element import Element
from instaui.components.content import Content
from instaui.event.event_mixin import EventMixin
from typing_extensions import TypedDict, Unpack
from ._utils import handle_props, handle_event_from_props

if typing.TYPE_CHECKING:
    from instaui.vars.types import TMaybeRef


class Affix(Element):
    def __init__(
        self,
        content: typing.Optional[TMaybeRef[str]] = None,
        **kwargs: Unpack[TAffixProps],
    ):
        super().__init__("t-affix")

        if content is not None:
            with self:
                Content(content)

        self.props(handle_props(kwargs))  # type: ignore
        handle_event_from_props(self, kwargs)  # type: ignore

    def on_fixed_change(
        self,
        handler: EventMixin,
        *,
        extends: typing.Optional[typing.List] = None,
    ):
        self.on(
            "fixed_change",
            handler,
            extends=extends,
        )
        return self


class TAffixProps(TypedDict, total=False):
    container: TMaybeRef[str]
    offset_bottom: TMaybeRef[float]
    offset_top: TMaybeRef[float]
    z_index: TMaybeRef[int]
    on_fixed_change: EventMixin
