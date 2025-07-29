"""
Root descriptor returns the first base class in the MRO of this single
inheriting enumeration, that subclassed KeeNum.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import AbstractKeeDesc

if TYPE_CHECKING:  # pragma: no cover
  from .. import KeeMeta


class Root(AbstractKeeDesc):
  """
  Root descriptor returns the first base class in the MRO of this single
  inheriting enumeration, that subclassed KeeNum.
  """

  def __instance_get__(self, instance: KeeMeta) -> KeeMeta:
    """
    Please note, that multiple inheritance is strictly prohibited. To
    understand why, see the one line implementation below. Now consider
    how much more complex and unpredictable it would have been to support
    multiple inheritance.
    """
    return instance if instance.isRoot else instance.root
