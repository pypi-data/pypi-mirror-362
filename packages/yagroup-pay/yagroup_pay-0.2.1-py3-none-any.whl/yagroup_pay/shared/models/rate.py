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


from .base import BaseDbModel
from sqlmodel import Field, Relationship
from typing_extensions import Optional

from .direction import Direction


class Rate(BaseDbModel, table=True):
    __tablename__ = 'rates'

    direction_id: int = Field(foreign_key='directions.id', nullable=False)
    direction: Direction = Relationship(sa_relationship_kwargs={'lazy': 'joined'})

    primary_currency_amount_min: Optional[int] = Field(nullable=True, default=None)
    primary_currency_amount_max: Optional[int] = Field(nullable=True, default=None)

    formula: str
    additional_commission: Optional[int] = Field(nullable=False, default=0)
    rounding: int = Field(default=0, nullable=False)

    value: Optional[float] = Field(nullable=True, default=None)
