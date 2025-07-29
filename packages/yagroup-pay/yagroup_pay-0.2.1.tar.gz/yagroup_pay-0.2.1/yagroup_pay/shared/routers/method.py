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


from nexium_api import route

from .base import Router
from .. import CreateMethodRequestData, CreateMethodResponseData, GetMethodsRequestData, GetMethodsResponseData, \
    GetMethodRequestData, GetMethodResponseData, UpdateBalanceMethodRequestData, UpdateBalanceMethodResponseData, \
    AddToMethodBalanceRequestData, AddToMethodBalanceResponseData, DeleteMethodRequestData, DeleteMethodResponseData, \
    UpdateMethodRequestData, UpdateMethodResponseData


class MethodRouter(Router):
    facade_service = 'MethodFacadeService'
    prefix = '/methods'

    @route(
        path='/create',
        request_data=CreateMethodRequestData,
        response_data=CreateMethodResponseData,
        response_field='method',
    )
    async def create(self):
        pass

    @route(
        path='/get-all',
        request_data=GetMethodsRequestData,
        response_data=GetMethodsResponseData,
        response_field='methods',
    )
    async def get_all(self):
        pass

    @route(
        path='/get',
        request_data=GetMethodRequestData,
        response_data=GetMethodResponseData,
        response_field='method',
    )
    async def get(self):
        pass

    @route(
        path='/update-balance',
        request_data=UpdateBalanceMethodRequestData,
        response_data=UpdateBalanceMethodResponseData,
        response_field='method',
    )
    async def update_balance(self):
        pass

    @route(
        path='/add-to-balance',
        request_data=AddToMethodBalanceRequestData,
        response_data=AddToMethodBalanceResponseData,
    )
    async def add_to_balance(self):
        pass

    @route(
        path='/delete',
        request_data=DeleteMethodRequestData,
        response_data=DeleteMethodResponseData,
        response_field='method',
    )
    async def delete(self):
        pass

    @route(
        path='/start-payment',
        request_data=UpdateMethodRequestData,
        response_data=UpdateMethodResponseData,
        response_field='method',
    )
    async def start_payment(self):
        pass

    @route(
        path='/stop-payment',
        request_data=UpdateMethodRequestData,
        response_data=UpdateMethodResponseData,
        response_field='method',
    )
    async def stop_payment(self):
        pass

    @route(
        path='/start-pause',
        request_data=UpdateMethodRequestData,
        response_data=UpdateMethodResponseData,
        response_field='method',
    )
    async def start_pause(self):
        pass

    @route(
        path='/stop-pause',
        request_data=UpdateMethodRequestData,
        response_data=UpdateMethodResponseData,
        response_field='method',
    )
    async def stop_pause(self):
        pass
