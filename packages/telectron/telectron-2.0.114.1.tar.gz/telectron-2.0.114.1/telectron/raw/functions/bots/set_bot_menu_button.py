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


class SetBotMenuButton(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``206``
        - ID: ``4504D54F``

    Parameters:
        user_id (:obj:`InputUser <telectron.raw.base.InputUser>`):
            N/A

        button (:obj:`BotMenuButton <telectron.raw.base.BotMenuButton>`):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["user_id", "button"]

    ID = 0x4504d54f
    QUALNAME = "functions.bots.SetBotMenuButton"

    def __init__(self, *, user_id: "raw.base.InputUser", button: "raw.base.BotMenuButton") -> None:
        self.user_id = user_id  # InputUser
        self.button = button  # BotMenuButton

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetBotMenuButton":
        # No flags
        
        user_id = TLObject.read(b)
        
        button = TLObject.read(b)
        
        return SetBotMenuButton(user_id=user_id, button=button)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.user_id.write())
        
        b.write(self.button.write())
        
        return b.getvalue()
