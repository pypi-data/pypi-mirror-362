"""
Disk Client module for interacting with the Y360 Disk

Details https://yandex.ru/dev/disk-api/doc/ru/
"""

__version__ = "0.1.0"

from y360_orglib.disk.disk_client import DiskClient
from y360_orglib.disk.disk_admin import DiskAdminClient
from y360_orglib.disk.models import PublicResourcesList, Resource, BaseAccess, UserAccess, MacroAccess, PublicSettings, ResourceListShort, ResourceShort


__all__ = [
    "DiskClient",
    "PublicResourcesList",
    "Resource",
    "BaseAccess",
    "UserAccess",
    "MacroAccess",
    "PublicSettings",
    "DiskAdminClient",
    "ResourceListShort",
    "ResourceShort"
    ]