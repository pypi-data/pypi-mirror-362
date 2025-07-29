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


from nexium_api import route, BaseAuth

from .. import CreateOrderRequestData, CreateOrderResponseData, UpdateOrdersResponseData, UpdateOrdersRequestData, \
    CancelOrderRequestData, CancelOrderResponseData, GetOrderRequestData, GetOrderResponseData
from .base import Router


class OrderRouter(Router):
    facade_service = 'OrderFacadeService'
    prefix = '/orders'

    @route(
        path='/get',
        request_data=GetOrderRequestData,
        response_data=GetOrderResponseData,
    )
    async def get(self):
        pass

    @route(
        path='/create',
        request_data=CreateOrderRequestData,
        response_data=CreateOrderResponseData,
    )
    async def create(self):
        pass

    @route(
        path='/update',
        request_data=UpdateOrdersRequestData,
        response_data=UpdateOrdersResponseData,
        auth=BaseAuth,
    )
    async def update(self):
        pass

    @route(
        path='/cancel',
        request_data=CancelOrderRequestData,
        response_data=CancelOrderResponseData,
        response_field='order',
    )
    async def cancel(self):
        pass
