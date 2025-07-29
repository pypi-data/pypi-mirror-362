##### Credits

# ===== Anime Game Remap (AG Remap) =====
# Authors: Albert Gold#2696, NK#1321
#
# if you used it to remap your mods pls give credit for "Albert Gold#2696" and "Nhok0169"
# Special Thanks:
#   nguen#2011 (for support)
#   SilentNightSound#7430 (for internal knowdege so wrote the blendCorrection code)
#   HazrateGolabi#1364 (for being awesome, and improving the code)

##### EndCredits


##### ExtImports
from typing import Dict, Optional, Union
##### EndExtImports

##### LocalImports
from ...constants.GenericTypes import VersionType
from ...data.VertexCountData import VertexCountData
from .ModDictAssets import ModDictAssets
##### EndLocalImports


##### Script
class VertexCounts(ModDictAssets[int]):
    """
    This class inherits from :class:`ModDictAssets`
    
    Class for managing vertex counts of a mod

    Parameters
    ----------
    repo: Optional[Dict[Union[:class:`str`, :class:`float`, `packaging.version.Version`_], Dict[:class:`str`, :class:`int`]]]
        The original source for the vertex counts:`<br />` :raw-html:`<br />`

        * The outer key is the game version number for the assets
        * The inner key is the name of the asset :raw-html:`<br />` :raw-html:`<br />`

        If this value is ``None``, will use the default vertex counts provided by the software :raw-html:`<br />` :raw-html:`<br />`

        **Default**: ``None``
    """

    def __init__(self, repo: Optional[Dict[Union[str, float, VersionType], Dict[str, int]]] = None):
        if (repo is None):
            repo = VertexCountData

        super().__init__(repo)
##### EndScript
