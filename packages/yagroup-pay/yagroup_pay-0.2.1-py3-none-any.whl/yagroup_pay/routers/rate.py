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

from ..shared import UpdateRatesRequestData, UpdateRatesResponseData, GetRatesRequestData, GetRatesResponseData, \
    CalculateRateRequestData, CalculateRateResponseData
from .base import Router


class RateRouter(Router):
    facade_service = 'RateFacadeService'
    prefix = '/rates'

    @route(
        path='/update',
        request_data=UpdateRatesRequestData,
        response_data=UpdateRatesResponseData,
    )
    async def update(self):
        pass

    @route(
        path='/get',
        request_data=GetRatesRequestData,
        response_data=GetRatesResponseData,
        response_field='rates',
    )
    async def get(self):
        pass

    @route(
        path='/calculate',
        request_data=CalculateRateRequestData,
        response_data=CalculateRateResponseData,
    )
    async def calculate(self):
        pass
