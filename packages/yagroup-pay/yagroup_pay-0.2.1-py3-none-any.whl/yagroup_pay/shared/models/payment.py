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

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from .base import BaseDbModel
from sqlmodel import Field, Relationship

from .user import User
from .method import Method
from .tg_message import TGMessage
from ..enums.payment_state import PaymentState
from .order import Order


class Payment(BaseDbModel, table=True):
    __tablename__ = 'payments'

    state: PaymentState

    order_id: Optional[int] = Field(foreign_key='orders.id')
    order: Optional[Order] = Relationship(sa_relationship_kwargs={'lazy': 'joined'})

    payer_id: int = Field(foreign_key='users.id')
    payer: User = Relationship(sa_relationship_kwargs={
        'foreign_keys': '[Payment.payer_id]',
        'lazy': 'joined',
    })

    payee_id: int = Field(foreign_key='users.id')
    payee: User = Relationship(sa_relationship_kwargs={
        'foreign_keys': '[Payment.payee_id]',
        'lazy': 'joined',
    })
    method_id: int = Field(foreign_key='methods.id')
    method: Method = Relationship(sa_relationship_kwargs={'lazy': 'joined'})

    amount: float
    photo: Optional[str] = Field(sa_column=Column(MEDIUMTEXT))

    tg_message_id: Optional[int] = Field(foreign_key='tg_messages.id')
    tg_message: Optional[TGMessage] = Relationship(sa_relationship_kwargs={'lazy': 'joined'})
