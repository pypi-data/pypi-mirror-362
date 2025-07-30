from __future__ import annotations
import typing
from instaui.components.element import Element


class InputAdornment(Element):
    def __init__(
        self,
        *,
        append: typing.Optional[str] = None,
        prepend: typing.Optional[str] = None,
    ):
        super().__init__("t-input-adornment")
        self.props({"append": append, "prepend": prepend})
