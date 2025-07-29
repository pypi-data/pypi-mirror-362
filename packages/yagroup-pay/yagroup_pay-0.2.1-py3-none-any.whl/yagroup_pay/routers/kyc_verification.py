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

from ..shared import CreateKycVerificationResponseData, CreateKycVerificationRequestData, \
    ConfirmKycVerificationRequestData, ConfirmKycVerificationResponseData, RejectKycVerificationResponseData, \
    RejectKycVerificationRequestData, GetKycVerificationRequestData, GetKycVerificationResponseData
from .base import Router


class KYCVerificationRouter(Router):
    facade_service = 'KycVerificationFacadeService'
    prefix = '/kyc'

    @route(
        path='/get',
        request_data=GetKycVerificationRequestData,
        response_data=GetKycVerificationResponseData,
        response_field='kyc_verification',
    )
    async def get(self):
        pass

    @route(
        path='/create',
        request_data=CreateKycVerificationRequestData,
        response_data=CreateKycVerificationResponseData,
        response_field='kyc_verification',
    )
    async def create(self):
        pass

    @route(
        path='/confirm',
        request_data=ConfirmKycVerificationRequestData,
        response_data=ConfirmKycVerificationResponseData,
    )
    async def confirm(self):
        pass

    @route(
        path='/reject',
        request_data=RejectKycVerificationRequestData,
        response_data=RejectKycVerificationResponseData,
    )
    async def reject(self):
        pass
