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


class GetFileHashes(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``206``
        - ID: ``9156982A``

    Parameters:
        location (:obj:`InputFileLocation <telectron.raw.base.InputFileLocation>`):
            N/A

        offset (``int`` ``64-bit``):
            N/A

    Returns:
        List of :obj:`FileHash <telectron.raw.base.FileHash>`
    """

    __slots__: List[str] = ["location", "offset"]

    ID = 0x9156982a
    QUALNAME = "functions.upload.GetFileHashes"

    def __init__(self, *, location: "raw.base.InputFileLocation", offset: int) -> None:
        self.location = location  # InputFileLocation
        self.offset = offset  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetFileHashes":
        # No flags
        
        location = TLObject.read(b)
        
        offset = Long.read(b)
        
        return GetFileHashes(location=location, offset=offset)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.location.write())
        
        b.write(Long(self.offset))
        
        return b.getvalue()
