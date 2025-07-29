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
from typing import Union, Optional, Union, List, Dict, Set
##### EndExtImports

##### LocalImports
from ...constants.BufTypeNames import BufElementNames
from ...constants.BufElementTypes import BufElementTypes
from .BufFile import BufFile
from ..VGRemap import VGRemap
from .BufFile import BufFile
##### EndLocalImports


##### Script
class BlendFile(BufFile):
    """
    This Class inherits from :class:`BufFile`

    Used for handling blend.buf files

    .. note::
        We observe that a Blend.buf file is a binary file defined as:

        * a line corresponds to the data for a particular vertex in the mod
        * each line contains 32 bytes (256 bits)
        * each line uses little-endian mode (MSB is to the right while LSB is to the left)
        * the first 16 bytes of a line are for the blend weights, each weight is 4 bytes or 32 bits (4 weights/line)
        * the last 16 bytes of a line are for the corresponding indices for the blend weights, each index is 4 bytes or 32 bits (4 indices/line)
        * the blend weights are floating points while the blend indices are unsigned integers

    Parameters
    ----------
    src: Union[:class:`str`, :class:`bytes`]
        The source file or bytes for the blend file
    """

    def __init__(self, src: Union[str, bytes]):
        super().__init__(src, [BufElementTypes.BlendWeightFloatRGBA.value, BufElementTypes.BlendIndicesIntRGBA.value], fileType = "Blend.buf")

    @classmethod
    def getMissingIndicesRemap(cls, src: Dict[str, Union[List[int], List[float]]], vgRemap: VGRemap) -> Dict[int, int]:
        """
        Retrives the temporary remap for any missing blend indices not included in 'vgRemap'

        Parameters
        ----------
        src: Dict[:class:`str`, Union[List[:class:`int`, List[:class:`float`]]]]
            The data for the blend weights and the blend indices for a particular vertex

        vgRemap: :class:`VGRemap`
            The vertex group remap for correcting the Blend.buf file

        Returns
        -------
        Dict[:class:`int`, :class:`int`]
            The temporary remap for the missing indices. :raw-html:`<br />` :raw-html:`<br />`

            The keys are the missing indices found and the values are the temporary remapped values for these missing indices
        """

        blendWeights = src[BufElementNames.BlendWeight.value]
        blendIndices = src[BufElementNames.BlendIndices.value]
        minBlendLen = min(len(blendWeights), len(blendIndices))

        result = {}
        for i in range(minBlendLen):
            index = blendIndices[i]
            if (index not in vgRemap.remap):
                result[index] = -abs(index) - 1

        return result

    @classmethod
    def remapIndices(cls, src: Dict[str, Union[List[int], List[float]]], vgRemap: VGRemap, remapMissingIndices: bool = True) -> Dict[str, Union[List[int], List[float]]]:
        """
        Remaps the vertex group indices for a particular line (vertex)

        Parameters
        ----------
        src: Dict[:class:`str`, Union[List[:class:`int`, List[:class:`float`]]]]
            The data for the blend weights and the blend indices for a particular vertex

        vgRemap: :class:`VGRemap`
            The vertex group remap for correcting the Blend.buf file

        remapMissingIndices: :class:`bool`
            Whether to deactivate any missing blend indices that cannot be identified :raw-html:`<br />` :raw-html:`<br />`

            **Default**: ``True``

        Returns 
        -------
        Dict[:class:`str`, Union[List[:class:`int`, List[:class:`float`]]]]
            The new data for the blend weights/blend indices, with the blend indices remapped
        """

        # Remapping missing indices to some blatantly non-existent index (eg. negative indices)
        # deactivates the weight on these indices
        tempMissingIndexRemap = {} if (not remapMissingIndices) else cls.getMissingIndicesRemap(src, vgRemap)

        blendWeights = src[BufElementNames.BlendWeight.value]
        blendIndices = src[BufElementNames.BlendIndices.value]

        minBlendLen = min(len(blendWeights), len(blendIndices))
        for i in range(minBlendLen):
            weight = blendWeights[i]
            index = blendIndices[i]

            if (weight == 0):
                continue

            if (index in vgRemap.remap):
                blendIndices[i] = int(vgRemap.remap[index])
            elif (index in tempMissingIndexRemap):
                blendIndices[i] = tempMissingIndexRemap[index]

        return src

    def remap(self, vgRemap: VGRemap, fixedBlendFile: Optional[str] = None, remapMissingIndices: bool = True) -> Union[Optional[str], bytearray]:
        """
        Remaps the blend indices in a Blend.buf file

        Parameters
        ----------
        vgRemap: :class:`VGRemap`
            The vertex group remap for correcting the Blend.buf file

        fixedBlendFile: Optional[:class:`str`]
            The file path for the fixed Blend.buf file :raw-html:`<br />` :raw-html:`<br />`

            **Default**: ``None``

        remapMissingIndices: :class:`bool`
            Whether to deactivate any missing blend indices that cannot be identified :raw-html:`<br />` :raw-html:`<br />`

            **Default**: ``True``

        Raises
        ------
        :class:`BlendFileNotRecognized`
            If the original Blend.buf file provided by the parameter ``blendFile`` cannot be read

        :class:`BadBlendData`
            If the bytes passed into this function do not correspond to the format defined for a Blend.buf file

        Returns
        -------
        Union[Optional[:class:`str`], :class:`bytearray`]
            If the argument ``fixedBlendFile`` is ``None``, then will return an array of bytes for the fixed Blend.buf file :raw-html:`<br />` :raw-html:`<br />`
            Otherwise will return the filename to the fixed RemapBlend.buf file if the provided Blend.buf file got corrected
        """

        # if no correction is needed to be done
        blendFile = self.src
        blendIsFile = isinstance(blendFile, str)
        if (not vgRemap.remap and blendIsFile):
            return None
        elif (not vgRemap.remap):
            return bytearray(blendFile)

        filters = [lambda data, startInd, lineInd, lineSize: self.remapIndices(data, vgRemap, remapMissingIndices = remapMissingIndices)]
        return self.fix(fixedBlendFile, filters = filters)
##### EndScript