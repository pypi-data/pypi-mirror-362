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


class InputStorePaymentStarsGift(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.InputStorePaymentPurpose`.

    Details:
        - Layer: ``206``
        - ID: ``1D741EF7``

    Parameters:
        user_id (:obj:`InputUser <telectron.raw.base.InputUser>`):
            N/A

        stars (``int`` ``64-bit``):
            N/A

        currency (``str``):
            N/A

        amount (``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["user_id", "stars", "currency", "amount"]

    ID = 0x1d741ef7
    QUALNAME = "types.InputStorePaymentStarsGift"

    def __init__(self, *, user_id: "raw.base.InputUser", stars: int, currency: str, amount: int) -> None:
        self.user_id = user_id  # InputUser
        self.stars = stars  # long
        self.currency = currency  # string
        self.amount = amount  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputStorePaymentStarsGift":
        # No flags
        
        user_id = TLObject.read(b)
        
        stars = Long.read(b)
        
        currency = String.read(b)
        
        amount = Long.read(b)
        
        return InputStorePaymentStarsGift(user_id=user_id, stars=stars, currency=currency, amount=amount)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.user_id.write())
        
        b.write(Long(self.stars))
        
        b.write(String(self.currency))
        
        b.write(Long(self.amount))
        
        return b.getvalue()
