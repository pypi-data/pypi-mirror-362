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


from nexium_api import BaseResponseData

from ..models.currency import Currency
from ..models.method import Method


class CreateMethodResponseData(BaseResponseData):
    method: Method


class GetMethodsResponseData(BaseResponseData):
    methods: list[Method]


class GetMethodResponseData(BaseResponseData):
    method: Method


class UpdateBalanceMethodResponseData(BaseResponseData):
    method: Method


class AddToMethodBalanceResponseData(BaseResponseData):
    method: Method
    currency: Currency


class UpdatePositionMethodResponseData(BaseResponseData):
    method: Method


class DeleteMethodResponseData(BaseResponseData):
    method: Method


class UpdateMethodResponseData(BaseResponseData):
    method: Method


# Admin

class GetMethodsAdminResponseData(BaseResponseData):
    methods: list[Method]


class UpdatePositionMethodAdminResponseData(BaseResponseData):
    method: Method
