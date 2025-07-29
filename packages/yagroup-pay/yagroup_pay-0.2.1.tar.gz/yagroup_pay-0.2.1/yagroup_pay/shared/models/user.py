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

from sqlalchemy import Column, BigInteger

from .base import BaseDbModel
from sqlmodel import Field, Relationship

from .kyc import KYC
from .exchanger import Exchanger


class User(BaseDbModel, table=True):
    __tablename__ = 'users'

    exchanger_id: int = Field(foreign_key='exchangers.id', default=None)
    exchanger: Exchanger = Relationship(sa_relationship_kwargs={'lazy': 'joined'})
    username: Optional[str]
    password: Optional[str]
    tg_user_id: int = Field(sa_column=Column(BigInteger()))
    tg_username: Optional[str]
    tg_business_connection_id: Optional[str]
    bonus: float = Field(default=0)
    referrer_user_id: Optional[int]
    kyc_id: Optional[int] = Field(foreign_key='kyc_verifications.id', default=None)
    kyc: KYC = Relationship(sa_relationship_kwargs={'lazy': 'joined'})

    def get_str_by_kyc(self) -> str:
        return f'{f'{self.kyc.fullname}, ' if self.kyc else ''}{'@' + self.username if self.username else f'id{self.id}'} ({self.exchanger.description})'
