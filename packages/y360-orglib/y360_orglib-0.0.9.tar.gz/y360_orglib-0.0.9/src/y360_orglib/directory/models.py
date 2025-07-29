
from typing import List, Literal
from pydantic import BaseModel, Field


class Contact(BaseModel):
    """User contact model
    Details https://yandex.ru/dev/api360/doc/ru/ref/UserService/UserService_List#v1usercontact

    Attributes:
        contact_type (str): Contact type
        value (str): Contact value
        main (bool): Is main contact or alternate
        alias (bool): Is alias contact
        synthetic (bool): Is synthetic contact (auto-generated)

    """

    contact_type: Literal['email', 'phone_extension', 'phone', 'site', 'icq', 'twitter', 'skype', 'staff'] = Field(alias='type')
    value: str
    main: bool = False
    alias: bool = False
    synthetic: bool = False


class ShortUser(BaseModel):
    """Short user information model
    Details https://yandex.ru/dev/api360/doc/ru/ref/GroupService/GroupService_DeleteMembers#v1shortuser

    Attributes:
        uid (str): User ID
        nickname (str): User nickname
        department_id (int): Department ID
        email (str): User email
        gender (str): User gender
        position (str): User position
    """
    uid: str = Field(alias="id")
    nickname: str
    department_id: int = Field(alias="departmentId")
    email: str
    gender: str
    position: str
    avatar_id: str = Field(alias="avatarId")

    class Name(BaseModel):
        """User Name model

        Attributes:
            first (str): User first name
            last (str): User last name
            middle (str): User middle name
        """

        first: str
        last: str
        middle: str

    name: Name
    

class User(ShortUser):
    """User information model
    Details https://yandex.ru/dev/api360/doc/ru/ref/UserService/UserService_List#v1user

    Attributes:
        is_enabled (bool): Is user enabled
        about (str): User description
        birthday (str): User birthday
        external_id (str): User external ID
        is_admin (bool): Is user admin
        is_robot (bool): Is user robot
        is_dismissed (bool): Is user dismissed
        timezone (str): User timezone
        language (str): User language
        created_at (str): User creation date
        updated_at (str): User update date
        display_name (str): User display name
        groups (List[int]): User groups
        contacts (List[Contact]): User contacts
        aliases (List[str]): User aliases
    """
    is_enabled: bool = Field(alias="isEnabled")
    about: str
    birthday: str
    external_id: str = Field(alias="externalId")
    is_admin: bool = Field(alias="isAdmin")
    is_robot: bool = Field(alias="isRobot")
    is_dismissed: bool = Field(alias="isDismissed")
    timezone: str
    language: str
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    display_name: str = Field(default='', alias="displayName")
    groups: List[int]
    contacts: List[Contact]
    aliases: List[str]


class UsersPage(BaseModel):
    """List of users

    Attributes:
        page (int): Current page
        pages (int): Total pages
        per_page (int): Users per page
        total (int): Total users in organization
        users (List[User]): List of users
    """
    page: int
    pages: int
    per_page: int = Field(alias="perPage")
    total: int
    users: List[User]


class ShortGroup(BaseModel):
    """Short Group model
    Details https://yandex.ru/dev/api360/doc/ru/ref/GroupService/GroupService_DeleteMembers#v1shortgroup

    Attributes:
        group_id (int): Group ID
        name (str): Group name
        members_count (int): Group members count
    """

    group_id: int = Field(alias="id")
    name: str
    members_count: int= Field(alias="membersCount")


class GroupMember(BaseModel):
    """Group member model
    Details https://yandex.ru/dev/api360/doc/ru/ref/GroupService/GroupService_Get#v1groupmember

    Attributes:
        member_id (str): Group member ID
        type (str): Member type (user, group, department)
    """

    member_id: str = Field(alias="id")
    type: Literal['user', 'group', 'department']


class Group(ShortGroup):
        """Group model
        Details https://yandex.ru/dev/api360/doc/ru/ref/GroupService/GroupService_List#v1group

        Attributes:
            type (str): Group type name
            description (str): Group description
            label (str): Group label
            email (str): Group email
            aliases (List[str]): Group email aliases
            external_id (str): Group external ID
            removed (bool): Is group deleted
            members (List[GroupMember]): Group members
            member_of (List[int]): Group member of
            created_at (str): Group creation date
        """

        type: str
        description: str
        label: str
        email: str
        aliases: List[str]
        external_id: str = Field(alias="externalId")
        removed: bool
        members: List[GroupMember]
        member_of: List[int] = Field(alias="memberOf")
        created_at: str= Field(alias="createdAt")
    
    
class GroupsPage(BaseModel):
    """List of Groups

    Attributes:
        groups (List[Group]): List of groups
        page (int): Current page
        pages (int): Total pages
        per_page (int): Groups per page
        total (int): Total groups in org
    """

    groups: list[Group]
    page: int
    pages: int
    per_page: int = Field(alias="perPage")
    total: int


class GroupMembers2(BaseModel):
    """Group members v2 model
    Details https://yandex.ru/dev/api360/doc/ru/ref/GroupV2Service/GroupService_ListMembers

    Attributes:
        groups (List[ShortGroup]): List of groups
        users (List[ShortUser]): List of users       
    """
    groups: List[ShortGroup]
    users: List[ShortUser]

class User2fa(BaseModel):
    """User 2fa details model
    Details https://yandex.ru/dev/api360/doc/ru/ref/UserService/UserService_Get2fa

    Attributes:
        user_id (str): User ID
        has2fa (bool): Is user has personally configured any 2fa methods
        has_security_phone (bool): Is user has set 2fa phone
    """

    user_id: str = Field(alias="userId")
    has2fa: bool
    has_security_phone: bool = Field(alias="hasSecurityPhone")

