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


class InputPaymentCredentialsSaved(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.InputPaymentCredentials`.

    Details:
        - Layer: ``206``
        - ID: ``C10EB2CF``

    Parameters:
        id (``str``):
            N/A

        tmp_password (``bytes``):
            N/A

    """

    __slots__: List[str] = ["id", "tmp_password"]

    ID = 0xc10eb2cf
    QUALNAME = "types.InputPaymentCredentialsSaved"

    def __init__(self, *, id: str, tmp_password: bytes) -> None:
        self.id = id  # string
        self.tmp_password = tmp_password  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPaymentCredentialsSaved":
        # No flags
        
        id = String.read(b)
        
        tmp_password = Bytes.read(b)
        
        return InputPaymentCredentialsSaved(id=id, tmp_password=tmp_password)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.id))
        
        b.write(Bytes(self.tmp_password))
        
        return b.getvalue()
