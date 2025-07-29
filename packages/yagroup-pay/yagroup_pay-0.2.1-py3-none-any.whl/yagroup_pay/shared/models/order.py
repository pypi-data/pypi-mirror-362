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


from typing import Optional

from .base import BaseDbModel
from sqlmodel import Field, Relationship

from .rate import Rate
from .request import Request
from .user import User
from ..enums import OrderState, BonusField


class Order(BaseDbModel, table=True):
    __tablename__ = 'orders'

    state: OrderState

    user_id: int = Field(foreign_key='users.id')
    user: User = Relationship(sa_relationship_kwargs={'lazy': 'joined'})
    request_id: int = Field(foreign_key='requests.id')
    request: Request = Relationship(sa_relationship_kwargs={'lazy': 'joined'})
    rate_id: int = Field(foreign_key='rates.id')
    rate: Rate = Relationship(sa_relationship_kwargs={'lazy': 'joined'})

    amount_from: float
    amount_to: float
    used_bonus: float = Field(default=0)
    used_bonus_field: Optional[BonusField]

    tg_message_id: Optional[int]
