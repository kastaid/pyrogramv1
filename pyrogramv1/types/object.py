#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import typing
from datetime import datetime
from json import dumps

import pyrogramv1


class Meta(type, metaclass=type("", (type,), {"__str__": lambda _: "~hi"})):
    def __str__(self):
        return f"<class 'pyrogramv1.types.{self.__name__}'>"


class Object(metaclass=Meta):
    def __init__(self, client: "pyrogramv1.Client" = None):
        self._client = client

    def bind(self, client: "pyrogramv1.Client"):
        """Bind a Client instance to this Pyrogram Object

        Parameters:
            client (:obj:`~pyrogramv1.types.Client`):
                The Client instance to bind this object with. Useful to re-enable bound methods after serializing and
                deserializing Pyrogram objects with ``repr`` and ``eval``.
        """
        self._client = client

    @staticmethod
    def default(obj: "Object"):
        if isinstance(obj, bytes):
            return repr(obj)

        # https://t.me/pyrogramv1chat/167281
        # Instead of re.Match, which breaks for python <=3.6
        if isinstance(obj, typing.Match):
            return repr(obj)

        return {
            "_": obj.__class__.__name__,
            **{
                attr: (
                    "*" * 9
                    if attr == "phone_number" else
                    str(datetime.fromtimestamp(getattr(obj, attr)))
                    if attr.endswith("date") else
                    getattr(obj, attr)
                )
                for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
                if getattr(obj, attr) is not None
            }
        }

    def __str__(self) -> str:
        return dumps(self, indent=4, default=Object.default, ensure_ascii=False)

    def __repr__(self) -> str:
        return "pyrogramv1.types.{}({})".format(
            self.__class__.__name__,
            ", ".join(
                f"{attr}={repr(getattr(self, attr))}"
                for attr in filter(lambda x: not x.startswith("_"), self.__dict__)
                if getattr(self, attr) is not None
            )
        )

    def __eq__(self, other: "Object") -> bool:
        for attr in self.__dict__:
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getstate__(self):
        new_dict = self.__dict__.copy()
        new_dict.pop("_client", None)
        return new_dict
