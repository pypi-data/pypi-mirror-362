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

from nexium_api import BaseRequestData
from sqlmodel import Field

from ..enums.method_type import MethodType


class CreateMethodRequestData(BaseRequestData):
    user_id: int
    type_: MethodType
    balance: float = Field(default=0)
    data: dict = Field(default={})


class GetMethodsRequestData(BaseRequestData):
    user_id: int


class GetMethodRequestData(BaseRequestData):
    method_id: int


class UpdateBalanceMethodRequestData(BaseRequestData):
    user_id: int
    method_id: int
    balance: float


class AddToMethodBalanceRequestData(BaseRequestData):
    method_id: int
    amount: float


class UpdatePositionMethodRequestData(BaseRequestData):
    user_id: int
    method_id: int
    position: int


class DeleteMethodRequestData(BaseRequestData):
    user_id: int
    method_id: int


class UpdateMethodRequestData(BaseRequestData):
    method_id: int


# Admin

class GetMethodsAdminRequestData(BaseRequestData):
    type_: Optional[MethodType] = Field(default=None)


class UpdatePositionMethodAdminRequestData(BaseRequestData):
    method_id: int
    position: int
