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


class ResolvedBusinessChatLinks(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.account.ResolvedBusinessChatLinks`.

    Details:
        - Layer: ``206``
        - ID: ``9A23AF21``

    Parameters:
        peer (:obj:`Peer <telectron.raw.base.Peer>`):
            N/A

        message (``str``):
            N/A

        chats (List of :obj:`Chat <telectron.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <telectron.raw.base.User>`):
            N/A

        entities (List of :obj:`MessageEntity <telectron.raw.base.MessageEntity>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: telectron.raw.functions

        .. autosummary::
            :nosignatures:

            account.ResolveBusinessChatLink
    """

    __slots__: List[str] = ["peer", "message", "chats", "users", "entities"]

    ID = 0x9a23af21
    QUALNAME = "types.account.ResolvedBusinessChatLinks"

    def __init__(self, *, peer: "raw.base.Peer", message: str, chats: List["raw.base.Chat"], users: List["raw.base.User"], entities: Optional[List["raw.base.MessageEntity"]] = None) -> None:
        self.peer = peer  # Peer
        self.message = message  # string
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.entities = entities  # flags.0?Vector<MessageEntity>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ResolvedBusinessChatLinks":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        message = String.read(b)
        
        entities = TLObject.read(b) if flags & (1 << 0) else []
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ResolvedBusinessChatLinks(peer=peer, message=message, chats=chats, users=users, entities=entities)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.entities else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(String(self.message))
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
