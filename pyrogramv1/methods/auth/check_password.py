#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import logging

from pyrogramv1 import raw
from pyrogramv1 import types
from pyrogramv1.scaffold import Scaffold
from pyrogramv1.utils import compute_password_check

log = logging.getLogger(__name__)


class CheckPassword(Scaffold):
    async def check_password(self, password: str) -> "types.User":
        """Check your Two-Step Verification password and log in.

        Parameters:
            password (``str``):
                Your Two-Step Verification password.

        Returns:
            :obj:`~pyrogramv1.types.User`: On success, the authorized user is returned.

        Raises:
            BadRequest: In case the password is invalid.
        """
        r = await self.send(
            raw.functions.auth.CheckPassword(
                password=compute_password_check(
                    await self.send(raw.functions.account.GetPassword()),
                    password
                )
            )
        )

        await self.storage.user_id(r.user.id)
        await self.storage.is_bot(False)

        return types.User._parse(self, r.user)
