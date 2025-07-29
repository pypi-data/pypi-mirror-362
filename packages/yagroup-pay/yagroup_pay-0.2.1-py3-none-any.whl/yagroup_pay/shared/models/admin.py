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

from .user import User


class Admin(BaseDbModel, table=True):
    __tablename__ = 'admins'

    user_id: int = Field(foreign_key='users.id')
    user: User = Relationship(sa_relationship_kwargs={'lazy': 'joined'})

    can_verify_kyc: bool = Field(default=False)
    can_create_requests: bool = Field(default=False)
    can_change_requisite_balance: bool = Field(default=False)
    can_change_requisite_position: bool = Field(default=False)
