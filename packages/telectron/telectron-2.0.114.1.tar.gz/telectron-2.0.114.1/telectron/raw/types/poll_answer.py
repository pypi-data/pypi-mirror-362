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


class PollAnswer(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.PollAnswer`.

    Details:
        - Layer: ``206``
        - ID: ``FF16E2CA``

    Parameters:
        text (:obj:`TextWithEntities <telectron.raw.base.TextWithEntities>`):
            N/A

        option (``bytes``):
            N/A

    """

    __slots__: List[str] = ["text", "option"]

    ID = 0xff16e2ca
    QUALNAME = "types.PollAnswer"

    def __init__(self, *, text: "raw.base.TextWithEntities", option: bytes) -> None:
        self.text = text  # TextWithEntities
        self.option = option  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PollAnswer":
        # No flags
        
        text = TLObject.read(b)
        
        option = Bytes.read(b)
        
        return PollAnswer(text=text, option=option)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.text.write())
        
        b.write(Bytes(self.option))
        
        return b.getvalue()
