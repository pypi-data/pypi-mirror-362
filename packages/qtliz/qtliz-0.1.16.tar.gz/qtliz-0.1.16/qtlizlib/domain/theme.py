from dataclasses import dataclass, field

from PySide6.QtGui import QColor
from pylizlib.data import datautils
from pylizlib.domain.os import OsTheme


@dataclass
class UiTheme:
    id: str = datautils.gen_random_string(10)
    mode: OsTheme | None = None
    primary_color_light: QColor | None = None
    primary_color_dark: QColor | None = None
    primary_color: QColor | None = None


    def get_primary_color(self) -> QColor | None:
        if self.mode is None:
            return self.primary_color
        else:
            return self.primary_color_light if self.mode == OsTheme.LIGHT else self.primary_color_dark


@dataclass
class AppTheme:
    ui: UiTheme = field(default_factory=UiTheme)
    system_ui_mode: OsTheme = OsTheme.UNKNOWN
