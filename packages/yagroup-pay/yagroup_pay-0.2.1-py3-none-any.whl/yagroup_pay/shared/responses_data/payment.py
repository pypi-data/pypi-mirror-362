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

from .. import Method
from ..models.order import Order
from ..models.currency import Currency
from ..models.payment import Payment


class GetPaymentResponseData(BaseResponseData):
    payment: Payment
    method: Method


class UpdatePaymentStateResponseData(BaseResponseData):
    payment: Payment
    order: Order
    currency_from: Currency
    currency_to: Currency


class SendPaymentForConfirmationResponseData(BaseResponseData):
    payment: Payment


class CancelPaymentResponseData(BaseResponseData):
    payment: Payment


class CreatePaymentByAdminResponseData(BaseResponseData):
    payment: Payment


class ConfirmPaymentResponseData(BaseResponseData):
    payment: Payment


# Admin

class GetPaymentsAdminResponseData(BaseResponseData):
    payments: list[Payment]
