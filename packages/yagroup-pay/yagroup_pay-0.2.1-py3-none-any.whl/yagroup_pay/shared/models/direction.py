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

from .exchanger import Exchanger
from .currency import Currency


class Direction(BaseDbModel, table=True):
    __tablename__ = 'directions'

    exchanger_id: int = Field(foreign_key='exchangers.id')
    exchanger: Exchanger = Relationship(sa_relationship_kwargs={'lazy': 'joined'})

    description: Optional[str]

    currency_from_id: int = Field(foreign_key='currencies.id')
    currency_from: Currency = Relationship(sa_relationship_kwargs={
        'foreign_keys': '[Direction.currency_from_id]',
        'lazy': 'joined',
    })
    currency_to_id: int = Field(foreign_key='currencies.id')
    currency_to: Currency = Relationship(sa_relationship_kwargs={
        'foreign_keys': '[Direction.currency_to_id]',
        'lazy': 'joined',
    })

    primary_currency_id: int = Field(foreign_key='currencies.id')
    primary_currency: Currency = Relationship(sa_relationship_kwargs={
        'foreign_keys': '[Direction.primary_currency_id]',
        'lazy': 'joined',
    })
    secondary_currency_id: int = Field(foreign_key='currencies.id')
    secondary_currency: Currency = Relationship(sa_relationship_kwargs={
        'foreign_keys': '[Direction.secondary_currency_id]',
        'lazy': 'joined',
    })

