from pathlib import Path
from typing import Union
from instaui import ui
from instaui.dependencies.plugin_dependency import register_plugin
from instaui_tdesign.types import TLocale, TCustomizeLocale
from instaui_tdesign._settings import configure

static_folder = Path(__file__).parent / "static"

tdesign_css = static_folder / "instaui-tdesign.css"
tdesign_esm_js = static_folder / "instaui-tdesign.js"


def _register_tdesign():
    register_plugin("InstauiTDesign", esm=tdesign_esm_js, css=[tdesign_css])


def use(*, locale: ui.TMaybeRef[Union[TLocale, TCustomizeLocale]] = "en-US"):
    """Use tdesign ui.

    Args:
        locale (ui.TMaybeRef[Union[TLocale, TCustomizeLocale]], optional): The locale of tdesign ui. Defaults to "en-US".

    Examples:
    .. code-block:: python
        from instaui import ui
        import instaui_tdesign as td

        td.use()

        @ui.page("/")
        def index_page():
            td.input(placeholder="input")
    """

    _register_tdesign()
    configure(locale=locale)
