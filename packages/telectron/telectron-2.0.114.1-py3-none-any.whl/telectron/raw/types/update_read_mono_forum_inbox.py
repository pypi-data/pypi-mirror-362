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


class UpdateReadMonoForumInbox(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.Update`.

    Details:
        - Layer: ``206``
        - ID: ``77B0E372``

    Parameters:
        channel_id (``int`` ``64-bit``):
            N/A

        saved_peer_id (:obj:`Peer <telectron.raw.base.Peer>`):
            N/A

        read_max_id (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["channel_id", "saved_peer_id", "read_max_id"]

    ID = 0x77b0e372
    QUALNAME = "types.UpdateReadMonoForumInbox"

    def __init__(self, *, channel_id: int, saved_peer_id: "raw.base.Peer", read_max_id: int) -> None:
        self.channel_id = channel_id  # long
        self.saved_peer_id = saved_peer_id  # Peer
        self.read_max_id = read_max_id  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateReadMonoForumInbox":
        # No flags
        
        channel_id = Long.read(b)
        
        saved_peer_id = TLObject.read(b)
        
        read_max_id = Int.read(b)
        
        return UpdateReadMonoForumInbox(channel_id=channel_id, saved_peer_id=saved_peer_id, read_max_id=read_max_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.channel_id))
        
        b.write(self.saved_peer_id.write())
        
        b.write(Int(self.read_max_id))
        
        return b.getvalue()
