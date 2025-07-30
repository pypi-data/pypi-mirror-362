# SPDX-PackageName: gel-python
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright Gel Data Inc. and the contributors.


from typing import Any

import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    import enum as _enum

    class StrEnum(str, _enum.Enum):
        __str__ = str.__str__
        __format__ = str.__format__  # type: ignore [assignment]

        @staticmethod
        def _generate_next_value_(
            name: str, start: int, count: int, last_values: list[Any]
        ) -> str:
            return name.lower()


__all__ = ("StrEnum",)
