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


class SendPaymentForm:
    async def send_payment_form(
        self: "Badmunda.Client",
        payment_form_id: int,
        input_invoice: "types.InputInvoice",
        credentials: "types.InputCredentials" = None
    ) -> "types.PaymentResult":
        """Send a filled-out payment form to the bot for final verification.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            payment_form_id (``int``):
                Payment form identifier returned by :meth:`~Badmunda.Client.get_payment_form`.

            input_invoice (:obj:`~Badmunda.types.InputInvoice`):
                The invoice.

            credentials (:obj:`~Badmunda.types.InputCredentials`, *optional*):
                The credentials chosen by user for payment.
                Pass None for a payment in Telegram Stars.

        Returns:
            :obj:`~Badmunda.types.PaymentResult`: On success, the payment result is returned.

        Example:
            .. code-block:: python

                # Pay regular invoice from message
                invoice = types.InputInvoiceMessage(
                    chat_id=chat_id,
                    message_id=123
                )

                form = await app.get_payment_form(invoice)

                await app.send_payment_form(
                    payment_form_id=form.id,
                    input_invoice=invoice,
                    credentials=types.InputCredentialsNew(
                        data=json.dumps({"token": "...", "type": "card"}), # Pass the token received from the payment provider
                    )
                )

                # Pay star invoice from message
                invoice = types.InputInvoiceMessage(
                    chat_id=chat_id,
                    message_id=123
                )

                form = await app.get_payment_form(invoice)

                await app.send_payment_form(
                    payment_form_id=form.id,
                    input_invoice=invoice
                )
        """
        if credentials is None:
            r = await self.invoke(
                raw.functions.payments.SendStarsForm(
                    form_id=payment_form_id,
                    invoice=await input_invoice.write(self),
                )
            )
        else:
            r = await self.invoke(
                raw.functions.payments.SendPaymentForm(
                    form_id=payment_form_id,
                    invoice=await input_invoice.write(self),
                    credentials=await credentials.write(self)
                )
            )

        return types.PaymentResult._parse(r)
