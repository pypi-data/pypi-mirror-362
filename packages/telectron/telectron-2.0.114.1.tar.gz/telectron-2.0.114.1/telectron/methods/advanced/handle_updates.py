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

import logging
import time
import asyncio
from typing import Dict, List
from itertools import chain

from telectron import raw, utils
from telectron.raw.types.updates import (
    DifferenceEmpty, ChannelDifferenceEmpty, DifferenceTooLong, ChannelDifferenceTooLong,
    Difference, DifferenceSlice, ChannelDifference
)
from telectron.errors import ChannelPrivate, ChannelInvalid, PeerIdInvalid, InternalServerError

log = logging.getLogger(__name__)

NO_SEQ = 0
BOT_CHANNEL_DIFF_LIMIT = 100000
USER_CHANNEL_DIFF_LIMIT = 100
POSSIBLE_GAP_TIMEOUT = 0.5
NO_UPDATES_TIMEOUT = 15 * 60


class HandleUpdates:

    async def handle_difference(self, difference, only_store_pts: bool = False):
        if (isinstance(difference, DifferenceEmpty) or
                isinstance(difference, ChannelDifferenceEmpty)):
            return
        elif isinstance(difference, DifferenceTooLong):
            # TODO
            return
        elif isinstance(difference, ChannelDifferenceTooLong):
            async with self.sequences.lock:
                self.sequences.set_pts(difference.dialog.pts,
                                       utils.get_channel_id(difference.dialog.peer.channel_id))
            return
        elif (isinstance(difference, Difference) or
                isinstance(difference, DifferenceSlice) or
                isinstance(difference, ChannelDifference)):
            new_pts = (difference.state.pts if isinstance(difference, Difference)
                       else difference.intermediate_state.pts if isinstance(difference, DifferenceSlice)
                       else difference.pts)
            users = {u.id: u for u in difference.users}
            chats = {c.id: c for c in difference.chats}
            if difference.new_messages:
                for m in difference.new_messages:
                    self.sequences.set_pts_checking(new_pts, m.peer_id)
                    if not only_store_pts:
                        self.put_update(
                            raw.types.UpdateNewMessage(
                                message=m,
                                pts=0,
                                pts_count=0
                            ),
                            users,
                            chats
                        )
            if difference.other_updates:
                for upd in difference.other_updates:
                    if not only_store_pts:
                        self.put_update(upd, users, chats)

    async def check_channels_difference(self, channel_ids: List[int], sec_per_channel: float = 0):
        limit = BOT_CHANNEL_DIFF_LIMIT if self.me.is_bot else USER_CHANNEL_DIFF_LIMIT
        for channel_id in channel_ids:
            start_time = time.time()
            async with self.sequences.lock:
                local_pts = self.sequences.get_pts(channel_id)
            try:
                diff = await self.invoke(
                    raw.functions.updates.GetChannelDifference(
                        force=True,
                        channel=await self.resolve_peer(channel_id),
                        filter=raw.types.ChannelMessagesFilterEmpty(),
                        pts=local_pts,
                        limit=limit
                    )
                )
            except (ChannelPrivate, ChannelInvalid, PeerIdInvalid):
                async with self.sequences.lock:
                    self.sequences.delete_pts(channel_id)
                await self.requesting_chats.delete_requesting_chat(channel_id)
            except InternalServerError:
                pass
            else:
                await self.handle_difference(diff, only_store_pts=(local_pts == 1))
            delay = sec_per_channel - (time.time() - start_time)
            if delay > 0:
                await asyncio.sleep(delay)

    async def check_difference(self):
        limit = BOT_CHANNEL_DIFF_LIMIT if self.me.is_bot else USER_CHANNEL_DIFF_LIMIT
        # TODO

    async def handle_updates(self, updates):
        # handle update containers
        # https://core.telegram.org/api/updates
        await self.requesting_chats.renew_last_update()
        if isinstance(updates, (raw.types.Updates, raw.types.UpdatesCombined)):
            await self.fetch_peers(updates.users)
            await self.fetch_peers(updates.chats)

            users = {u.id: u for u in updates.users}
            chats = {c.id: c for c in updates.chats}

            await self.update_min_users_and_chats(updates, users, chats)

            for update in updates.updates:
                if isinstance(update, raw.types.UpdateChannelTooLong):
                    log.warning(update)

                await self.check_and_apply_update(update, users, chats)
        elif isinstance(updates, (raw.types.UpdateShortMessage, raw.types.UpdateShortChatMessage)):
            diff = await self.invoke(
                raw.functions.updates.GetDifference(
                    pts=updates.pts - updates.pts_count,
                    date=updates.date,
                    qts=-1
                )
            )

            await self.handle_difference(diff)
        elif isinstance(updates, raw.types.UpdateShort):
            await self.check_and_apply_update(updates.update, {}, {})
        elif isinstance(updates, raw.types.UpdatesTooLong):
            log.info(updates)

    async def check_and_apply_update(self, update, users, chats):
        channel_id = self.get_channel_id(update)
        pts = getattr(update, "pts", None)
        pts_count = getattr(update, "pts_count", 0)
        if not (pts and channel_id):
            self.put_update(update, users, chats)
            return
        async with self.sequences.lock:
            channel_id = utils.get_channel_id(channel_id)
            local_pts = self.sequences.get_pts(channel_id)
            if local_pts is None:
                self.sequences.set_pts(pts, channel_id)
                self.put_update(update, users, chats)
            elif local_pts + pts_count == pts:
                self.sequences.set_pts(pts, channel_id)
                self.put_update(update, users, chats)
            elif local_pts + pts_count > pts:
                # TODO: Reject such updates
                self.put_update(update, users, chats)
            elif local_pts + pts_count < pts:
                # TODO: recover possible gap
                self.sequences.set_pts(pts, channel_id)
                self.put_update(update, users, chats)

    def put_update(self, update, users: Dict, chats: Dict):
        self.dispatcher.updates_queue.put_nowait((update, users, chats))

    @staticmethod
    def get_channel_id(update) -> int:
        return (
            getattr(
                getattr(
                    getattr(
                        update, "message", None
                    ), "peer_id", None
                ), "channel_id", None
            ) or getattr(update, "channel_id", None)
        )

    async def update_min_users_and_chats(self, updates, users: Dict, chats: Dict):
        # https://core.telegram.org/api/min
        for update in updates.updates:
            is_min = False
            for peer in chain(users.values(), chats.values()):
                if getattr(peer, "min", False):
                    is_min = True
                    continue
            pts = getattr(update, "pts", None)
            pts_count = getattr(update, "pts_count", None)
            channel_id = self.get_channel_id(update)
            if isinstance(update, raw.types.UpdateNewChannelMessage) and is_min:
                message = update.message
                if not isinstance(message, raw.types.MessageEmpty):
                    for _ in range(3):
                        try:
                            diff = await self.invoke(
                                raw.functions.updates.GetChannelDifference(
                                    channel=await self.resolve_peer(
                                        utils.get_channel_id(channel_id)),
                                    filter=raw.types.ChannelMessagesFilter(
                                        ranges=[raw.types.MessageRange(
                                            min_id=update.message.id,
                                            max_id=update.message.id
                                        )]
                                    ),
                                    pts=pts - pts_count,
                                    limit=pts_count
                                )
                            )
                        except ChannelPrivate:
                            break
                        except InternalServerError:
                            continue
                        else:
                            if not isinstance(diff, raw.types.updates.ChannelDifferenceEmpty):
                                users.update({u.id: u for u in diff.users})
                                chats.update({c.id: c for c in diff.chats})
                            break
