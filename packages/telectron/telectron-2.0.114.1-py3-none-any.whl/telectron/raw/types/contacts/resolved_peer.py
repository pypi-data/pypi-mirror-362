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


class ResolvedPeer(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.contacts.ResolvedPeer`.

    Details:
        - Layer: ``206``
        - ID: ``7F077AD9``

    Parameters:
        peer (:obj:`Peer <telectron.raw.base.Peer>`):
            N/A

        chats (List of :obj:`Chat <telectron.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <telectron.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: telectron.raw.functions

        .. autosummary::
            :nosignatures:

            contacts.ResolveUsername
            contacts.ResolvePhone
    """

    __slots__: List[str] = ["peer", "chats", "users"]

    ID = 0x7f077ad9
    QUALNAME = "types.contacts.ResolvedPeer"

    def __init__(self, *, peer: "raw.base.Peer", chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.peer = peer  # Peer
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ResolvedPeer":
        # No flags
        
        peer = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ResolvedPeer(peer=peer, chats=chats, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
