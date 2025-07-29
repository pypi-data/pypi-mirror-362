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

from .. import SendPaymentForConfirmationResponseData, \
    SendPaymentForConfirmationRequestData, CancelPaymentRequestData, CancelPaymentResponseData, GetPaymentRequestData, \
    GetPaymentResponseData, CreatePaymentByAdminRequestData, CreatePaymentByAdminResponseData, \
    ConfirmPaymentRequestData, ConfirmPaymentResponseData
from .base import Router


class PaymentRouter(Router):
    facade_service = 'PaymentFacadeService'
    prefix = '/payments'

    @route(
        path='/get',
        request_data=GetPaymentRequestData,
        response_data=GetPaymentResponseData,
    )
    async def get(self):
        pass

    @route(
        path='/send-for-confirmation',
        request_data=SendPaymentForConfirmationRequestData,
        response_data=SendPaymentForConfirmationResponseData,
        response_field='payment',
    )
    async def send_for_confirmation(self):
        pass

    @route(
        path='/cancel',
        request_data=CancelPaymentRequestData,
        response_data=CancelPaymentResponseData,
        response_field='payment',
    )
    async def cancel(self):
        pass

    @route(
        path='/create-by-admin',
        request_data=CreatePaymentByAdminRequestData,
        response_data=CreatePaymentByAdminResponseData,
        response_field='payment',
    )
    async def create_by_admin(self):
        pass

    @route(
        path='/confirm',
        request_data=ConfirmPaymentRequestData,
        response_data=ConfirmPaymentResponseData,
        response_field='payment',
    )
    async def confirm(self):
        pass
