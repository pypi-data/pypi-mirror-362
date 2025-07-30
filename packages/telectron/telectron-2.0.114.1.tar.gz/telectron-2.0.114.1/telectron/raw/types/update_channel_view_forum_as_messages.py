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


class UpdateChannelViewForumAsMessages(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.Update`.

    Details:
        - Layer: ``206``
        - ID: ``7B68920``

    Parameters:
        channel_id (``int`` ``64-bit``):
            N/A

        enabled (``bool``):
            N/A

    """

    __slots__: List[str] = ["channel_id", "enabled"]

    ID = 0x7b68920
    QUALNAME = "types.UpdateChannelViewForumAsMessages"

    def __init__(self, *, channel_id: int, enabled: bool) -> None:
        self.channel_id = channel_id  # long
        self.enabled = enabled  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateChannelViewForumAsMessages":
        # No flags
        
        channel_id = Long.read(b)
        
        enabled = Bool.read(b)
        
        return UpdateChannelViewForumAsMessages(channel_id=channel_id, enabled=enabled)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.channel_id))
        
        b.write(Bool(self.enabled))
        
        return b.getvalue()
