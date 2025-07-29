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

from sqlmodel import Relationship, Field

from .base import BaseDbModel
from .payment import Payment
from .tg_message import TGMessage
from .user import User
from ..enums import PaymentConfirmationState


class PaymentConfirmation(BaseDbModel, table=True):
    __tablename__ = 'payments_confirmations'

    payment_id: int = Field(foreign_key='payments.id')
    payment: Payment = Relationship(sa_relationship_kwargs={'lazy': 'joined'})

    user_id: Optional[int] = Field(foreign_key='users.id')
    user: Optional[User] = Relationship(sa_relationship_kwargs={'lazy': 'joined'})

    state: PaymentConfirmationState

    tg_message_id: Optional[int] = Field(foreign_key='tg_messages.id')
    tg_message: Optional[TGMessage] = Relationship(sa_relationship_kwargs={'lazy': 'joined'})
