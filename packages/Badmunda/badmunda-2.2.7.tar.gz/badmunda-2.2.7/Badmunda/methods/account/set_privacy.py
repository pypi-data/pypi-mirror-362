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

from typing import List, Union

import Badmunda
from Badmunda import raw, types, enums


class SetPrivacy:
    async def set_privacy(
        self: "Badmunda.Client",
        key: "enums.PrivacyKey",
        rules: List[Union[
            "types.InputPrivacyRuleAllowAll",
            "types.InputPrivacyRuleAllowBots",
            "types.InputPrivacyRuleAllowChats",
            "types.InputPrivacyRuleAllowCloseFriends",
            "types.InputPrivacyRuleAllowContacts",
            "types.InputPrivacyRuleAllowPremium",
            "types.InputPrivacyRuleAllowUsers",
            "types.InputPrivacyRuleDisallowAll",
            "types.InputPrivacyRuleDisallowBots",
            "types.InputPrivacyRuleDisallowChats",
            "types.InputPrivacyRuleDisallowContacts",
            "types.InputPrivacyRuleDisallowUsers"
        ]],
    ):
        """Set account privacy rules.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            key (:obj:`~Badmunda.enums.PrivacyKey`):
                Privacy key.

            rules (Iterable of :obj:`~Badmunda.types.InputPrivacyRule`):
                List of privacy rules.

        Returns:
            List of :obj:`~Badmunda.types.PrivacyRule`: On success, the list of privacy rules is returned.

        Example:
            .. code-block:: python

                from Badmunda import enums, types

                # Prevent everyone from seeing your phone number
                await app.set_privacy(enums.PrivacyKey.PHONE_NUMBER, [types.InputPrivacyRuleDisallowAll()])
        """
        r = await self.invoke(
            raw.functions.account.SetPrivacy(
                key=key.value(),
                rules=[await rule.write(self) for rule in rules]
            )
        )

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        return types.List(types.PrivacyRule._parse(self, rule, users, chats) for rule in r.rules)
