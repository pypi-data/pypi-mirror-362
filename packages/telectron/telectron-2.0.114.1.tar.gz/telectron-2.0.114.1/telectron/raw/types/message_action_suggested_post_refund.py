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


class MessageActionSuggestedPostRefund(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.MessageAction`.

    Details:
        - Layer: ``206``
        - ID: ``69F916F8``

    Parameters:
        payer_initiated (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["payer_initiated"]

    ID = 0x69f916f8
    QUALNAME = "types.MessageActionSuggestedPostRefund"

    def __init__(self, *, payer_initiated: Optional[bool] = None) -> None:
        self.payer_initiated = payer_initiated  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionSuggestedPostRefund":
        
        flags = Int.read(b)
        
        payer_initiated = True if flags & (1 << 0) else False
        return MessageActionSuggestedPostRefund(payer_initiated=payer_initiated)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.payer_initiated else 0
        b.write(Int(flags))
        
        return b.getvalue()
