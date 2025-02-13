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

from typing import Union

from pyrogramv1 import raw, types
from pyrogramv1.scaffold import Scaffold


class GetChatAdminsWithInviteLinks(Scaffold):
    async def get_chat_admins_with_invite_links(
        self,
        chat_id: Union[int, str],
    ):
        """Get the list of the administrators that have exported invite links in a chat.

        You must be the owner of a chat for this to work.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).

        Returns:
            List of :obj:`~pyrogramv1.types.ChatAdminWithInviteLink`: On success, the list of admins that have exported
            invite links is returned.
        """
        r = await self.send(
            raw.functions.messages.GetAdminsWithInvites(
                peer=await self.resolve_peer(chat_id)
            )
        )

        users = {i.id: i for i in r.users}

        return types.List(
            types.ChatAdminWithInviteLinks._parse(self, admin, users)
            for admin in r.admins
        )
