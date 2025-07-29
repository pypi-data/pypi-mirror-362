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


from typing import Optional

from nexium_api import BaseRequestData

from ..enums.bonus_field import BonusField


class UpdateRatesRequestData(BaseRequestData):
    pass


class GetRatesRequestData(BaseRequestData):
    exchanger_id: int


class CalculateRateRequestData(BaseRequestData):
    direction_id: int
    amount_from: Optional[float]
    amount_to: Optional[float]
    use_bonus: Optional[float]
    use_bonus_field: Optional[BonusField]
