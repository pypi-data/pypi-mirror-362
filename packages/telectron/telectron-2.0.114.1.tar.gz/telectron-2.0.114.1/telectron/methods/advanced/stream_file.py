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

from typing import Callable
import asyncio
import logging
import math
from hashlib import md5
from typing import BinaryIO

from telectron import StopTransmission
from telectron import raw
from telectron.session import Session

log = logging.getLogger(__name__)


class StreamFile:
    async def stream_file(
        self,
        file_iterator: Callable,
        file_id: int = None,
        file_part: int = None,
        progress: callable = None,
        progress_args: tuple = (),
    ):
        """Upload a file onto Telegram servers, without actually invokeing the message to anyone.
        Useful whenever an InputFile type is required.

        .. note::

            This is a utility method intended to be used **only** when working with raw
            :obj:`functions <telectron.api.functions>` (i.e: a Telegram API method you wish to use which is not
            available yet in the Client class as an easy-to-use method).

        Parameters:
            path (``str`` | ``BinaryIO``):
                The path of the file you want to upload that exists on your local machine or a binary file-like object
                with its attribute ".name" set for in-memory uploads.

            file_id (``int``, *optional*):
                In case a file part expired, pass the file_id and the file_part to retry uploading that specific chunk.

            file_part (``int``, *optional*):
                In case a file part expired, pass the file_id and the file_part to retry uploading that specific chunk.

            progress (``callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            ``InputFile``: On success, the uploaded file is returned in form of an InputFile object.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if file_iterator is None:
            return None

        part_size = 512 * 1024

        iterator = file_iterator(part_size)

        file_name, file_size = await iterator.__anext__()

        if file_size == 0:
            raise ValueError("File size equals to 0 B")

        file_size_limit_mib = 4000 if self.me.is_premium else 2000

        if file_size > file_size_limit_mib * 1024 * 1024:
            raise ValueError(f"Can't upload files bigger than {file_size_limit_mib} MiB")

        file_total_parts = int(math.ceil(file_size / part_size))
        is_big = file_size > 10 * 1024 * 1024
        pool_size = 3 if is_big else 1
        workers_count = 4 if is_big else 1
        is_missing_part = file_id is not None
        file_id = file_id or self.rnd_id()
        md5_sum = md5() if not is_big and not is_missing_part else None
        queue = asyncio.Queue(16)
        pool = [
            Session(
                self, await self.storage.dc_id(), await self.storage.auth_key(),
                await self.storage.test_mode(), is_media=True
            ) for _ in range(pool_size)
        ]
        workers = [self.loop.create_task(_worker(queue, self, session))
                   for session in pool
                   for _ in range(workers_count)]

        try:
            for session in pool:
                await session.start()
            current_file_part = 0
            buffer = b''
            next_buffer = b''
            while True:
                try:
                    if len(buffer) > part_size:
                        next_buffer = buffer[part_size:]
                        buffer = buffer[:part_size]
                    if len(buffer) < part_size:
                        chunk = await iterator.__anext__()
                        buffer += chunk
                    if len(buffer) < part_size or len(buffer) > part_size:
                        continue
                    if file_part is None or file_part == current_file_part:
                        await _store_part(is_big,
                                          file_id,
                                          current_file_part,
                                          file_total_parts,
                                          buffer,
                                          queue)

                    if file_part == current_file_part:
                        return

                    if md5_sum is not None:
                        md5_sum.update(buffer)

                    current_file_part += 1
                    buffer = next_buffer
                    next_buffer = b''

                    if progress:
                        await self.handle_progress(current_file_part * part_size,
                                                   file_size,
                                                   progress,
                                                   progress_args)
                except StopAsyncIteration:
                    if buffer:
                        await _store_part(is_big,
                                          file_id,
                                          current_file_part,
                                          file_total_parts,
                                          buffer,
                                          queue)

                        if md5_sum is not None:
                            md5_sum.update(buffer)
                    break
            if md5_sum is not None:
                md5_sum = "".join([hex(i)[2:].zfill(2) for i in md5_sum.digest()])
        except StopTransmission:
            raise
        except Exception as e:
            log.error(e, exc_info=True)
            raise
        else:
            if is_big:
                return raw.types.InputFileBig(
                    id=file_id,
                    parts=file_total_parts,
                    name=file_name,

                )
            else:
                return raw.types.InputFile(
                    id=file_id,
                    parts=file_total_parts,
                    name=file_name,
                    md5_checksum=md5_sum
                )
        finally:
            for _ in workers:
                await queue.put(None)

            await asyncio.gather(*workers)

            for session in pool:
                await session.stop()


async def _store_part(is_big: bool,
                      file_id: int,
                      file_part: int,
                      file_total_parts: int,
                      buffer: bytes,
                      queue: asyncio.Queue):
    if is_big:
        rpc = raw.functions.upload.SaveBigFilePart(
            file_id=file_id,
            file_part=file_part,
            file_total_parts=file_total_parts,
            bytes=buffer
        )
    else:
        rpc = raw.functions.upload.SaveFilePart(
            file_id=file_id,
            file_part=file_part,
            bytes=buffer
        )

    await queue.put(rpc)


async def _worker(queue: asyncio.Queue, client: StreamFile, session: Session):
    while True:
        data = await queue.get()

        if data is None:
            return

        try:
            await client.loop.create_task(session.invoke(data))
        except Exception as e:
            log.error(e)


'''
Example:

import aiohttp
async def test_iterator(read_bytes_size: int):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://google.com') as response:
            yield response.url.name, int(response.headers['content-length'])
            while True:
                chunk = await response.content.read(read_bytes_size)
                if not chunk:
                    break
                yield chunk
                if response.content.at_eof():
                    break
test_iterator.name = ''
'''
