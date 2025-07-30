"""hammad.cli.styles.types"""

from typing import Literal, Union
from typing_extensions import TypeAliasType

__all__ = (
    "CLIStyleError",
    "CLIStyleVerticalOverflowMethod",
    "CLIStyleJustifyMethod",
    "CLIStyleOverflowMethod",
    "CLIStyleColorName",
    "CLIStyleStyleName",
    "CLIStyleBoxName",
    "CLIStyleType",
    "CLIStyleBackgroundType",
)


class CLIStyleError(Exception):
    """Exception raised for any errors related to the
    rich styling of some rendered content."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


CLIStyleVerticalOverflowMethod = TypeAliasType(
    "CLIStyleVerticalOverflowMethod",
    Literal[
        "crop",
        "ellipsis",
        "visible",
    ],
)
"""Literal helper alias providing type hinting for the various compatible
vertical overflow methods within the `rich` library."""


CLIStyleJustifyMethod = TypeAliasType(
    "CLIStyleJustifyMethod",
    Literal[
        "left",
        "center",
        "right",
    ],
)
"""Literal helper alias providing type hinting for the various compatible
justify methods within the `rich` library."""


CLIStyleOverflowMethod = TypeAliasType(
    "CLIStyleOverflowMethod",
    Literal[
        "crop",
        "fold",
        "ellipsis",
        "ignore",
    ],
)
"""Literal helper alias providing type hinting for the various compatible
overflow methods within the `rich` library."""


CLIStyleColorName = TypeAliasType(
    "CLIStyleColorName",
    Literal[
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
        "bright_black",
        "bright_red",
        "bright_green",
        "bright_yellow",
        "bright_blue",
        "bright_magenta",
        "bright_cyan",
        "bright_white",
        "grey0",
        "navy_blue",
        "dark_blue",
        "blue3",
        "blue1",
        "dark_green",
        "deep_sky_blue4",
        "dodger_blue3",
        "dodger_blue2",
        "green4",
        "spring_green4",
        "turquoise4",
        "deep_sky_blue3",
        "dodger_blue1",
        "dark_cyan",
        "light_sea_green",
        "deep_sky_blue2",
        "deep_sky_blue1",
        "green3",
        "spring_green3",
        "cyan3",
        "dark_turquoise",
        "turquoise2",
        "green1",
        "spring_green2",
        "spring_green1",
        "medium_spring_green",
        "cyan2",
        "cyan1",
        "purple4",
        "purple3",
        "blue_violet",
        "grey37",
        "medium_purple4",
        "slate_blue3",
        "royal_blue1",
        "chartreuse4",
        "pale_turquoise4",
        "steel_blue",
        "steel_blue3",
        "cornflower_blue",
        "dark_sea_green4",
        "cadet_blue",
        "sky_blue3",
        "chartreuse3",
        "sea_green3",
        "aquamarine3",
        "medium_turquoise",
        "steel_blue1",
        "sea_green2",
        "sea_green1",
        "dark_slate_gray2",
        "dark_red",
        "dark_magenta",
        "orange4",
        "light_pink4",
        "plum4",
        "medium_purple3",
        "slate_blue1",
        "wheat4",
        "grey53",
        "light_slate_grey",
        "medium_purple",
        "light_slate_blue",
        "yellow4",
        "dark_sea_green",
        "light_sky_blue3",
        "sky_blue2",
        "chartreuse2",
        "pale_green3",
        "dark_slate_gray3",
        "sky_blue1",
        "chartreuse1",
        "light_green",
        "aquamarine1",
        "dark_slate_gray1",
        "deep_pink4",
        "medium_violet_red",
        "dark_violet",
        "purple",
        "medium_orchid3",
        "medium_orchid",
        "dark_goldenrod",
        "rosy_brown",
        "grey63",
        "medium_purple2",
        "medium_purple1",
        "dark_khaki",
        "navajo_white3",
        "grey69",
        "light_steel_blue3",
        "light_steel_blue",
        "dark_olive_green3",
        "dark_sea_green3",
        "light_cyan3",
        "light_sky_blue1",
        "green_yellow",
        "dark_olive_green2",
        "pale_green1",
        "dark_sea_green2",
        "pale_turquoise1",
        "red3",
        "deep_pink3",
        "magenta3",
        "dark_orange3",
        "indian_red",
        "hot_pink3",
        "hot_pink2",
        "orchid",
        "orange3",
        "light_salmon3",
        "light_pink3",
        "pink3",
        "plum3",
        "violet",
        "gold3",
        "light_goldenrod3",
        "tan",
        "misty_rose3",
        "thistle3",
        "plum2",
        "yellow3",
        "khaki3",
        "light_yellow3",
        "grey84",
        "light_steel_blue1",
        "yellow2",
        "dark_olive_green1",
        "dark_sea_green1",
        "honeydew2",
        "light_cyan1",
        "red1",
        "deep_pink2",
        "deep_pink1",
        "magenta2",
        "magenta1",
        "orange_red1",
        "indian_red1",
        "hot_pink",
        "medium_orchid1",
        "dark_orange",
        "salmon1",
        "light_coral",
        "pale_violet_red1",
        "orchid2",
        "orchid1",
        "orange1",
        "sandy_brown",
        "light_salmon1",
        "light_pink1",
        "pink1",
        "plum1",
        "gold1",
        "light_goldenrod2",
        "navajo_white1",
        "misty_rose1",
        "thistle1",
        "yellow1",
        "light_goldenrod1",
        "khaki1",
        "wheat1",
        "cornsilk1",
        "grey100",
        "grey3",
        "grey7",
        "grey11",
        "grey15",
        "grey19",
        "grey23",
        "grey27",
        "grey30",
        "grey35",
        "grey39",
        "grey42",
        "grey46",
        "grey50",
        "grey54",
        "grey58",
        "grey62",
        "grey66",
        "grey70",
        "grey74",
        "grey78",
        "grey82",
        "grey85",
        "grey89",
        "grey93",
        "default",
    ],
)
"""Literal helper alias providing type hinting for the various compatible color names
within the `rich` library."""


CLIStyleStyleName = TypeAliasType(
    "CLIStyleStyleName",
    Literal[
        "dim",
        "d",
        "bold",
        "b",
        "italic",
        "i",
        "underline",
        "u",
        "blink",
        "blink2",
        "reverse",
        "r",
        "conceal",
        "c",
        "strike",
        "s",
        "underline2",
        "uu",
        "frame",
        "encircle",
        "overline",
        "o",
        "on",
        "not",
        "link",
        "none",
    ],
)
"""Literal helper alias providing type hinting for the various compatible
style names within the `rich` library."""


CLIStyleBoxName = TypeAliasType(
    "StyleBoxName",
    Literal[
        "ascii",
        "ascii2",
        "ascii_double_head",
        "square",
        "square_double_head",
        "minimal",
        "minimal_heavy_head",
        "minimal_double_head",
        "simple",
        "simple_head",
        "simple_heavy",
        "horizontals",
        "rounded",
        "heavy",
        "heavy_edge",
        "heavy_head",
        "double",
        "double_edge",
        "markdown",
    ],
)
"""Literal helper alias providing type hinting for the various compatible
box names within the `rich` library."""


# ------------------------------------------------------------
# 'Exported' (Hinted) Typed


CLIStyleType = TypeAliasType(
    "CLIStyleType", Union[str | CLIStyleStyleName, CLIStyleColorName]
)
"""Union helper alias for the accepted inputs within modules
that incorporate the `style` parameter within the
`hammad` package."""


CLIStyleBackgroundType = TypeAliasType(
    "CLIStyleBackgroundType", Union[str | CLIStyleBoxName, CLIStyleColorName]
)
"""Union helper alias for the accepted inputs within modules
that incorporate the `bg` parameter within the
`hammad` package."""
