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

import os
import logging
import tempfile
from io import BytesIO
import re
import shutil
from typing import Union, IO

import telectron
from telectron.utils import randstr

log = logging.getLogger(__name__)


class HandleDownload:
    async def handle_download(self, packet) -> Union[BytesIO, IO, IO[bytes], IO[str], str]:
        file_id, directory, file_name, in_memory, file_size, progress, progress_args = packet
        file = BytesIO() if in_memory else tempfile.NamedTemporaryFile("wb", delete=False)

        try:
            async for chunk in self.get_file(file_id, file_size, 0, 0, progress, progress_args):
                file.write(chunk)
        except telectron.StopTransmission:
            if not in_memory:
                file.close()
                os.remove(file.name)

            return None
        else:
            if in_memory:
                file.name = file_name
                return file
            else:
                file_path = os.path.abspath(re.sub("\\\\", "/", os.path.join(directory, file_name)))
                os.makedirs(directory, exist_ok=True)
                file.close()
                shutil.move(file.name, file_path)
                return file_path
