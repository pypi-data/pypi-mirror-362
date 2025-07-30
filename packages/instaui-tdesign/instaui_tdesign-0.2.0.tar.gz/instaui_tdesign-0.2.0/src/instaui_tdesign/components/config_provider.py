from typing import Any, Dict, Optional
from instaui.components.element import Element


class ConfigProvider(Element):
    def __init__(
        self,
        *,
        globalConfig: Optional[Dict[str, Any]] = None,
    ):
        super().__init__("t-config-provider")
        self.props({"globalConfig": globalConfig})
