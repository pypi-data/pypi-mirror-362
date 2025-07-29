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

from typing import Callable, Optional

import Badmunda


class OnStart:
    def on_start(self: Optional["OnStart"] = None) -> Callable:
        """Decorator for handling client start.

        This does the same thing as :meth:`~Badmunda.Client.add_handler` using the
        :obj:`~Badmunda.handlers.StartHandler`.

        .. include:: /_includes/usable-by/users-bots.rst
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, Badmunda.Client):
                self.add_handler(Badmunda.handlers.StartHandler(func))
            else:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append((Badmunda.handlers.StartHandler(func), 0))

            return func

        return decorator
