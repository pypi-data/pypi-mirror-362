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
from enum import Enum
##### EndExtImports


##### Script
class IfPredPartType(Enum):
    """
    Enum for the possible types for an :class:`IfPredPart`
    """

    If = "if"
    """
    The part contains the staring keyword 'if'
    """

    Else = "else"
    """
    The part contains the staring keyword 'else'
    """

    Elif = "elif"
    """
    The part contains the starting keyword 'elif'
    """

    EndIf = "endif"
    """
    The part contains the staring keyword 'endif'
    """

    @classmethod
    def getType(cls, rawPredPart: str):
        """
        Retrieves the type for an :class:`IfPredPart`

        Parameters
        ----------
        rawPredPart: :class:`str`
            The predicate string for the :class:`IfPredPart`

        Returns
        -------
        Optional[:class:`IfPredPartType`]
            The type found based off 'rawPredPart'
        """

        cleanedRawPart = rawPredPart.strip().lower()

        if (cleanedRawPart.startswith(cls.If.value)):
            return cls.If
        elif (cleanedRawPart.startswith(cls.EndIf.value)):
            return cls.EndIf
        elif (cleanedRawPart.startswith(cls.Elif.value)):
            return cls.Elif
        elif (not cleanedRawPart.startswith(cls.Else.value)):
            return None
        
        cleanedRawPart = cleanedRawPart[len(cls.Else.value):].lstrip()
        if (cleanedRawPart.startswith(cls.If.value)):
            return cls.Elif
        return cls.Else
##### EndScript