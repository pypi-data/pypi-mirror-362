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


from sqlalchemy import Column, BigInteger

from .base import BaseDbModel
from sqlmodel import Field

from ..enums.method_type import MethodType


class Currency(BaseDbModel, table=True):
    __tablename__ = 'currencies'

    id_str: str = Field(unique=True, nullable=False)
    tg_methods_channel_id: int = Field(sa_column=Column(BigInteger()))
    tg_payments_channel_id: int = Field(sa_column=Column(BigInteger()))
    method_type: MethodType
    rounding: int = Field(default=0, nullable=False)
    name: str = Field(nullable=False)
    emoji: str = Field(nullable=False)
