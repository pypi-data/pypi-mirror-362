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


class TextUrl(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.RichText`.

    Details:
        - Layer: ``206``
        - ID: ``3C2884C1``

    Parameters:
        text (:obj:`RichText <telectron.raw.base.RichText>`):
            N/A

        url (``str``):
            N/A

        webpage_id (``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["text", "url", "webpage_id"]

    ID = 0x3c2884c1
    QUALNAME = "types.TextUrl"

    def __init__(self, *, text: "raw.base.RichText", url: str, webpage_id: int) -> None:
        self.text = text  # RichText
        self.url = url  # string
        self.webpage_id = webpage_id  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TextUrl":
        # No flags
        
        text = TLObject.read(b)
        
        url = String.read(b)
        
        webpage_id = Long.read(b)
        
        return TextUrl(text=text, url=url, webpage_id=webpage_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.text.write())
        
        b.write(String(self.url))
        
        b.write(Long(self.webpage_id))
        
        return b.getvalue()
