#  telectron - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of telectron.
#
#  telectron is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  telectron is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with telectron.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from telectron.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from telectron.raw.core import TLObject
from telectron import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class RecentMeUrlStickerSet(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.RecentMeUrl`.

    Details:
        - Layer: ``206``
        - ID: ``BC0A57DC``

    Parameters:
        url (``str``):
            N/A

        set (:obj:`StickerSetCovered <telectron.raw.base.StickerSetCovered>`):
            N/A

    """

    __slots__: List[str] = ["url", "set"]

    ID = 0xbc0a57dc
    QUALNAME = "types.RecentMeUrlStickerSet"

    def __init__(self, *, url: str, set: "raw.base.StickerSetCovered") -> None:
        self.url = url  # string
        self.set = set  # StickerSetCovered

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RecentMeUrlStickerSet":
        # No flags
        
        url = String.read(b)
        
        set = TLObject.read(b)
        
        return RecentMeUrlStickerSet(url=url, set=set)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(self.set.write())
        
        return b.getvalue()
