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

from sqlmodel import SQLModel

from .base import BaseDbModel
from sqlalchemy import JSON
from sqlmodel import Field, Relationship

from ..enums.text import Text
from ..enums.method_type import MethodType
from .user import User


class Method(BaseDbModel, table=True):
    __tablename__ = 'methods'

    user_id: int = Field(foreign_key='users.id')
    user: User = Relationship(sa_relationship_kwargs={'lazy': 'joined'})

    type: MethodType
    data: dict = Field(default={}, sa_type=JSON)
    balance: float
    position: int = Field(default=0)
    tg_message_id: Optional[int]
    on_payment: bool = Field(default=False)
    on_pause: bool = Field(default=False)
    is_fast_deal: bool = Field(default=False)
    is_slow_deal: bool = Field(default=False)

    def get_data(self):
        if self.type == MethodType.RUSSIAN_BANK:
            return RussianBankMethodData(**self.data)
        elif self.type == MethodType.ZELLE:
            return ZelleMethodData(**self.data)
        elif self.type == MethodType.USDT_TRC20:
            return USDTMethodData(**self.data)

    def get_channel_text(self):
        # FIXME
        if self.is_fast_deal:
            deal_info = '⚡️ БЫСТРАЯ СДЕЛКА (< 1ч)\n\n'
        elif self.is_slow_deal:
            deal_info = '📈 ВЫГОДНАЯ СДЕЛКА (<24ч)\n\n'
        else:
            deal_info = ''

        return Text.METHOD_TG_CHANNEL.format(
            deal_info=deal_info,
            id=self.id,
            balance=self.balance,
            method_data=self.get_data(),
            pause_info=Text.METHOD_ON_PAUSE[self.on_pause],
            payment_info=Text.METHOD_ON_PAYMENT[self.on_payment],
        )


class RussianBankMethodData(SQLModel):
    bank_name: str
    fullname: str
    sbp: Optional[int]
    card: Optional[str] = Field(default=None)

    def __str__(self):
        return (f'🏦 Название банка: {self.bank_name}\n'
                f'🛂 ФИО получателя: {self.fullname}\n'
                f'📱 Система быстрых платежей: {self.sbp if self.sbp else 'Не указано'}\n'
                f'💳 Номер карты: {self.card if self.card else 'Не указано'}')


class USDTMethodData(SQLModel):
    address: str

    def __str__(self):
        return (f'🏦 Сеть: TRC20\n'
                f'🔐 Адрес кошелька: {self.address}')


class ZelleMethodData(SQLModel):
    value: str
    fullname: str

    def __str__(self):
        return (f'🛂 Имя получателя: {self.fullname}\n'
                f'🏦 Email или телефон: {self.value}')


METHODS = {
    MethodType.RUSSIAN_BANK: RussianBankMethodData,
    MethodType.ZELLE: ZelleMethodData,
    MethodType.USDT_TRC20: USDTMethodData,
}
