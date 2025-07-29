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

from .. import CreateUserRequestData, CreateUserResponseData, GetUserRequestData, GetUserResponseData, \
    UpdateUserTgBusinessConnectionIdResponseData, UpdateUserTgBusinessConnectionIdRequestData, AddBonusUserRequestData, \
    AddBonusUserResponseData
from .base import Router


class UserRouter(Router):
    facade_service = 'UserFacadeService'
    prefix = '/users'

    @route(
        path='/create',
        request_data=CreateUserRequestData,
        response_data=CreateUserResponseData,
        response_field='user',
    )
    async def create(self):
        pass

    @route(
        path='/get',
        request_data=GetUserRequestData,
        response_data=GetUserResponseData,
        response_field='user',
    )
    async def get(self):
        pass

    @route(
        path='/update-tg-business-connection-id',
        request_data=UpdateUserTgBusinessConnectionIdRequestData,
        response_data=UpdateUserTgBusinessConnectionIdResponseData,
        response_field='user',
    )
    async def update_tg_business_connection_id(self):
        pass

    @route(
        path='/add-bonus',
        request_data=AddBonusUserRequestData,
        response_data=AddBonusUserResponseData,
        response_field='user',
    )
    async def add_bonus(self):
        pass
