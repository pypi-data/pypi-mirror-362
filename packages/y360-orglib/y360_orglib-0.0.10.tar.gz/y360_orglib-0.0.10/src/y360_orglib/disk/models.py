from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field

class Resource(BaseModel):
    """
    Resource model
    Details https://yandex.ru/dev/disk-api/doc/ru/reference/response-objects#resource
    
    Attributes:
        public_key (str): Public resource key
        public_url (str): Public resource url
        name (str): Name of the resource (filename or folder)
        created (str): Resource creation date
        modified (str): Resource modify date
        path (str): Full resource path on Disk
        type (str): Resource type (dir, file)
        mime_type (str): Resource MIME-type
        size (int): Resource file size

    """

    public_key: str
    public_url: str
    name: str
    created: str
    modified: str
    path: str
    type: Literal['file', 'dir']
    mime_type: str = ''
    size: int = 0

class PublicResourcesList(BaseModel):
    """
    Public Resources List model
    Details https://yandex.ru/dev/disk-api/doc/ru/reference/response-objects#publicresourcelist

    Attributes:
        items (List[Resource]): List of resources
        limit (int): Limit of resources
        offset (int): Offset of resources
    """

    items: List[Resource]
    limit: int
    offset: int

class ResourceShort(BaseModel):
    """
    Short Resource model
    Details https://yandex.ru/dev/disk-api/doc/ru/reference/response-objects#resourceshort

    Attributes:
        public_hash (str): Published resource key. Only if resource is published
        created_at (str): Resource creation date in ISO 8601 format
        modified_at (str): Resource modify date in ISO 8601 format
        name (str): Resource name (filename or folder name) 
        path (str): Full resource path on Disk
        type (str): Resource type (dir, file)

    """
    public_hash: Optional[str]
    created_at: str
    modified_at: str
    name: str
    path: str
    type: Literal['file', 'dir']

class ResourceListShort(BaseModel):
    """
    Short Resource List model
    Details https://yandex.ru/dev/disk-api/doc/ru/reference/response-objects#resourceshort

    Attributes:
        items (List[Resource]): List of resources
        limit (int): Limit of resources
        offset (int): Offset of resources
    """

    items: List[ResourceShort]
    limit: int
    offset: int


class BaseAccess(BaseModel):
    """
    Base Public Access model
    Details https://yandex.ru/dev/disk-api/doc/ru/reference/response-objects#publicaccesses

    Attributes:
        access_type (str): Access type (macro, user, group, department)
        rights (List[str]): List of rights
        macros (List[str]): List of macro accesses
    """

    macros: List[str] = []
    access_type: str = Field(alias='type')
    rights: List[str] = []
    
class MacroAccess(BaseAccess):
    """
    Macro Accesses model
    
    Args:
        access_type (str): Access type (macro)
        rights (List[str]): List of rights
        macros (List[str]): List of macro accesses
    
    """

    access_type: Literal['macro'] = Field(alias='type')
    

class UserAccess(BaseAccess):
    """
    User Accesses model
  
    Args:
        access_type (str): Access type (user, group, department)
        org_id (int): Organization ID (only for macro type employees)
        user_id (int): User ID

    """

    access_type: Literal['user', 'group', 'department', 'owner'] = Field(alias='type')
    org_id: Optional[int] = None
    user_id: int = Field(alias='id')


class PublicSettings(BaseModel):
    """
    Public settings model
    Details https://yandex.ru/dev/disk-api/doc/ru/reference/response-objects#publicsettings
    
    Attributes:
        available_until (str): Resource link lifetime
        public_accesses (List[Union[MacroAccess, UserAccess]]): List of public accesses
    """

    available_until: Optional[Union[str, int]]
    public_accesses: List[Union[MacroAccess, UserAccess]] = Field(alias='accesses')
    

    


