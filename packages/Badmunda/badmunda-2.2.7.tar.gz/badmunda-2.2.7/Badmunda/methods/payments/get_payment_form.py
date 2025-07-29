#  Badmunda - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Badmunda.
#
#  Badmunda is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Badmunda is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Badmunda.  If not, see <http://www.gnu.org/licenses/>.

import Badmunda
from Badmunda import raw, types


class GetPaymentForm:
    async def get_payment_form(
        self: "Badmunda.Client",
        input_invoice: "types.InputInvoice"
    ) -> "types.PaymentForm":
        """Get an invoice payment form.

        This method must be called when the user presses inline button of the type InlineKeyboardButton with buy parameter,
        or wants to buy access to media in a paid media message.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            input_invoice (:obj:`~Badmunda.types.InputInvoice`):
                The invoice.

        Returns:
            :obj:`~Badmunda.types.PaymentForm`: On success, a payment form is returned.

        Example:
            .. code-block:: python

                # Get payment form from message
                await app.get_payment_form(
                    types.InputInvoiceMessage(
                        chat_id=chat_id,
                        message_id=123
                    )
                )

                # Get payment form from link
                await app.get_payment_form(
                    types.InputInvoiceName(
                        name="https://t.me/$xvbzUtt5sUlJCAAATqZrWRy9Yzk"
                    )
                )
        """
        r = await self.invoke(
            raw.functions.payments.GetPaymentForm(
                invoice=await input_invoice.write(self)
            )
        )

        return types.PaymentForm._parse(self, r)
