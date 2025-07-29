##### Credits

# ===== Anime Game Remap (AG Remap) =====
# Authors: NK#1321, Albert Gold#2696
#
# if you used it to remap your mods pls give credit for "Nhok0169" and "Albert Gold#2696"
# Special Thanks:
#   nguen#2011 (for support)
#   SilentNightSound#7430 (for internal knowdege so wrote the blendCorrection code)
#   HazrateGolabi#1364 (for being awesome, and improving the code)

##### EndCredits

##### LocalImports
from .....constants.ColourConsts import ColourConsts
from ....textures.Colour import Colour
from .BasePixelTransform import BasePixelTransform
##### EndLocalImports


##### Script
class InvertAlpha(BasePixelTransform):
    """
    This class inherits from :class:`BasePixelTransform`

    Inverts the alpha channel of a pixel
    """

    def transform(self, pixel: Colour, x: int, y: int):
        pixel.alpha = ColourConsts.MinColourValue.value - pixel.alpha
##### EndScript