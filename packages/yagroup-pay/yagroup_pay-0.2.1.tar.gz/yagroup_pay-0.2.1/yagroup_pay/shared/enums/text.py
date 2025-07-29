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


from . import OrderState, PaymentState


class Text:
    REQUEST = (
        '<b>👋🏻 Номер заявки: {request_id:08d}</b>\n\n'
        'За {amount_from} {currency_from} {currency_from_emoji} вы получите '
        '{amount_to} {currency_to}{currency_to_emoji}.\n\n'
        '⏳ Вы готовы сделать перевод в течении 20 минут?'
    )
    ORDER = (
        '<b>🔄 Номер заказа: {order_id:08d}</b>\n\n'
        'Вы отдаете: {amount_from} {currency_from}{currency_from_emoji}\n'
        'Вы получаете: {amount_to} {currency_to}{currency_to_emoji}\n\n'
        '<b>{state}</b>'
    )
    PAYMENT = (
        '<b>💵 Номер платежа: {payment_id:08d}</b>\n\n'
        '<b>{state}</b>\n\n'
        'Произведите оплату по следующим реквизитам:\n'
        '💰 Сумма: {amount} {currency}{currency_emoji}\n'
        '{method_data}\n\n'
        '❗️ Оплатите ровно эту сумму. После оплаты нажмите кнопку "Я оплатил".\n\n'
        '❗️ Реквизиты действительны 20 минут, не успеваете - сообщите нам, мы предоставим новые реквизиты. '
        'Средства, отправленные на недействительные реквизиты возврату не подлежат!'
    )
    PAYMENT_EXPIRED = (
        '<b>💵 Номер платежа: {payment_id:08d}</b>\n\n'
        '<b>{state}</b>\n\n'
        '💰 Сумма: {amount} {currency}{currency_emoji}\n\n'
        '{method_data_expired}\n\n'
        '❗️ Реквизиты недействительны. Средства, отправленные на недействительные реквизиты возврату не подлежат'
    )
    PAYMENT_ADMIN = (
        '<b>💵 Номер платежа: {payment_id:08d}\n\n'
        '💰 Сумма: {amount}</b>\n\n'
        '⬆️ Отправитель: {payer_data}\n'
        '⬇️ Получатель: {payee_data}\n\n'
        'Реквизиты получателя:\n'
        '{method_data}\n\n'
        '{confirmation_data}\n\n'
        '#METHOD_{method_id:08d}\n'
        '#PAYER_{payer_id:08d}\n'
    )
    PAYMENT_ADMIN_CONFIRMATION = (
        '❗️ Оплата ожидает подтверждения. Вы можете вручную принять или отклонить её. '
        'После этого у получателя больше не будет возможности сделать это самостоятельно.'
    )
    PAYMENT_CONFIRMED_BY_ADMIN = (
        '✅👩‍💻 Оплата подтверждена Администратором в {payment_confirmation_datetime}.'
    )
    PAYMENT_CONFIRMED_BY_PAYEE = (
        '✅🧡 Оплата подтверждена Получателем в {payment_confirmation_datetime}.'
    )
    PAYMENT_CANCELED = (
        '❌ Оплата отменена'
    )
    PAYMENT_STATES = {
        PaymentState.PAYMENT: '⏳ Оплачивается',
        PaymentState.CONFIRMATION: '🕔 Подтверждаем оплату',
        PaymentState.COMPLETED: '✅ Выполнен',
        PaymentState.CANCELED: '❌ Отменен',
    }
    METHOD_TG_CHANNEL = (
        '{deal_info}'
        '🆔 ID: {id:08d}\n'
        '💸 Баланс: {balance}\n'
        '{method_data}\n\n'
        '{pause_info}\n'
        '{payment_info}'
    )
    METHOD_ON_PAYMENT = {
        True: '❗️ Реквизит оплачивается администратором',
        False: '✅ Реквизит можно оплатить',
    }
    METHOD_ON_PAUSE = {
        True: '❗️ Реквизит на паузе',
        False: '✅ Реквизит активен',
    }
    METHOD_START_PAYMENT_BUTTON = '💸 Сделать выплату'
    METHOD_START_PAUSE_BUTTON = '⏸️ На паузу'
    METHOD_STOP_PAUSE_BUTTON = '▶️ Восстановить'
    PAYMENT_PAYEE = (
        '<b>💵 Номер платежа: {payment_id:08d}\n'
        '💰 Сумма: {amount}</b>\n\n'
        'Реквизиты получателя:\n'
        '{method_data}\n\n'
        '{confirmation_data}'
    )
    PAYMENT_PAYEE_CONFIRMATION = (
        '❗️ Мы сделали выплату на ваши реквизиты. Пожалуйста, проверьте платеж и подтвердите получение средств, '
        'нажав на кнопку ниже.'
    )
    ORDER_STATES = {
        OrderState.INCOMING_WAITING: '⏳ Ожидание реквизитов',
        OrderState.INCOMING_PAYMENT: '💳 Клиент оплачивает',
        OrderState.INCOMING_CONFIRMATION: '⏳ Подтверждение оплаты',
        OrderState.OUTGOING_WAITING: '⏳ Ожидание реквизитов клиента',
        OrderState.OUTGOING_PAYMENT: '🧡 Выплата клиенту',
        OrderState.OUTGOING_CONFIRMATION: '⏳ Подтверждение получения',
        OrderState.COMPLETED: '✅ Выполнен',
        OrderState.CANCELED: '❌ Отменен',
    }
