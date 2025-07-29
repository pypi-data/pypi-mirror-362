#
# (c) 2025, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from sqlalchemy import BigInteger, Column
from sqlmodel import Field

from .base import BaseDbModel
from ..enums import TGMessageChatType, TGMessageType


class TGMessage(BaseDbModel, table=True):
    __tablename__ = 'tg_messages'

    chat_type: TGMessageChatType
    type: TGMessageType

    chat_id: int = Field(sa_column=Column(BigInteger()))
    message_id: int = Field(sa_column=Column(BigInteger()))
    can_edit: bool = Field(default=True)
