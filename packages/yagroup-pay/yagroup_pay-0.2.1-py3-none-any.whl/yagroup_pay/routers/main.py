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


from .base import Router
from .currency import CurrencyRouter
from .direction import DirectionRouter
from .exchanger import ExchangerRouter
from .kyc import KYCRouter
from .method import MethodRouter
from .order import OrderRouter
from .payment import PaymentRouter
from .rate import RateRouter
from .rate_source import RateSourceRouter
from .request import RequestRouter
from .user import UserRouter


class MainRouter(Router):
    currency: CurrencyRouter
    direction: DirectionRouter
    exchanger: ExchangerRouter
    kyc: KYCRouter
    method: MethodRouter
    order: OrderRouter
    payment: PaymentRouter
    rate: RateRouter
    rate_source: RateSourceRouter
    request: RequestRouter
    user: UserRouter
