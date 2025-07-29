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

from ..base import Router
from ... import GetMethodsAdminRequestData, GetMethodsAdminResponseData, UpdatePositionMethodAdminRequestData, \
    UpdatePositionMethodAdminResponseData


class MethodAdminRouter(Router):
    facade_service = 'MethodAdminFacadeService'
    prefix = '/methods'

    @route(
        path='/get-all',
        request_data=GetMethodsAdminRequestData,
        response_data=GetMethodsAdminResponseData,
        response_field='methods',
    )
    async def get_all(self):
        pass

    @route(
        path='/update-position',
        request_data=UpdatePositionMethodAdminRequestData,
        response_data=UpdatePositionMethodAdminResponseData,
        response_field='method',
    )
    async def update_position(self):
        pass
