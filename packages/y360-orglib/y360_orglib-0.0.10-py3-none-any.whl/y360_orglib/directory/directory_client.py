
import logging
from typing import List, Tuple
import httpx
from y360_orglib.directory.models import Contact, GroupMembers2, GroupsPage, User, User2fa, UsersPage
from y360_orglib.common.exceptions import APIError, DirectoryClientError
from y360_orglib.common.http import make_request
from y360_orglib.logging.config import configure_logger


class DirectoryClient():
    """
    Directory API Client
    
    Args:
        api_key (str): API key
        org_id (str): Organization ID
        ssl_verify (bool, optional): Verify SSL certificate. Defaults to True.
        log_level (int, optional): Log level. Defaults to logging.INFO.
    """

    __url = 'https://api360.yandex.net/directory/v1/org/'
    __url_v2 = 'https://api360.yandex.net/directory/v2/org/'
    __per_page = 100
    
    def __init__(self, api_key: str, org_id: str, ssl_verify=True, log_level=logging.INFO):
        """Initialize the Directory Client
        
        Args:
            api_key (str): API key
            org_id (str): Organization ID
            ssl_verify (bool, optional): Verify SSL certificate. Defaults to True.
            log_level (int, optional): Log level. Defaults to logging.INFO.

        """

        self._api_key = api_key
        self._org_id = org_id
        self.log = configure_logger(logger_name=__name__, level=log_level)
        self.session = httpx.Client(verify=ssl_verify)
        self._headers = {
            "Authorization": f"OAuth {api_key}",
            "content-type": "application/json",
        }
        self.session.headers.update(self._headers)


    def count_pages(self)-> Tuple[int, int]:
        """
        Get number of pages in users list response

        Returns:
            Tuple[int, int]: (users_count, pages_count)
        
        Raises:
            DirectoryClientError: If error occurs
        """

        path = f'{self.__url}{self._org_id}/users?perPage={self.__per_page}'

        try:
            response_json = make_request(session=self.session, url=path, method='GET')
            pages_count = response_json['pages']
            users_count = response_json['total']
            return users_count, pages_count
        except APIError as e:
            self.log.error(f"Error getting users pages count: {e}")
            raise DirectoryClientError(e)
        
    
    def get_users_page(self, page) -> UsersPage:
        """
        Get a Users page with list of users (default 100 per page)

        Args:
            page (int): Page number
        Returns:
            UsersPage: Users page object
        Raises:
            DirectoryClientError: If error occurs
        """

        path = f'{self.__url}{self._org_id}/users?page={page}&perPage={self.__per_page}'

        try:
            response_json = response_json = make_request(session=self.session, url=path, method='GET')
            return UsersPage(**response_json)
        except APIError as e:
            self.log.error(f"Error getting users page: {e}")
            raise DirectoryClientError(e)
        
    
    def get_all_users(self) -> List[User]:
        """
        Get all users of an organization.

        Returns:
            List[User]: List of User objects
        """
        
        users = []
        _, total_pages = self.count_pages()
        for page in range(1, total_pages + 1):
            users_page = self.get_users_page(page)
            users.extend(users_page.users)

        return users
    
    
    def add_user_contacts(self, user: User, contacts: List[Contact], replace=False):
        """Add contacts to a user.

        Args:
            user (User): User object
            contacts (List[Contact]): List of contacts
            replace (bool, optional): Replace existing contacts. Defaults to False.
        
        Returns:
            dict: Response with operation result json
        """

        path = f'{self.__url}{self._org_id}/users/{user.uid}/contacts'
        
        if not replace:
            for user_contact in user.contacts:
                if not user_contact.synthetic:
                    contacts.append(user_contact)
        contacts_json = {"contacts": []}
        for contact in contacts:
            contacts_json["contacts"].append(contact.model_dump(by_alias=True))
        try:
            response_json = make_request(session=self.session, url=path, method='PUT', json=contacts_json)
            return response_json
        except APIError as e:
            self.log.error(f"Error adding user contacts: {e}")
            raise DirectoryClientError(e)
        
        
    def add_user_to_group(self, user_id: str, group_id: int) -> dict:
        """
        Add user to a group
        Use API v1 method: https://yandex.ru/dev/api360/doc/ru/ref/GroupService/GroupService_AddMember

        Args:
            user_id (str): User ID
            group_id (int): Group ID

        Returns:
            dict: Response
        """

        path = f'{self.__url}{self._org_id}/groups/{group_id}/members'
        body = {
            "id": user_id,
            "type": 'user'
        }
        try:
            response_json = make_request(session=self.session, url=path, method='POST', json=body)
            return response_json
        except APIError as e:
            self.log.error(f"Error adding user to group: {e}")
            raise DirectoryClientError(e)
        

    def get_groups_page(self, page: int = 1, per_page: int = 10) -> GroupsPage:
        """
        Get groups of an organization
        Use API v1 method: https://yandex.ru/dev/api360/doc/ru/ref/GroupService/GroupService_List

        Args:
            page (int, optional): Page number. Defaults to 1.
            per_page (int, optional): Number of groups per page. Defaults to 10.

        Returns:
            GroupsPage: List of groups
        """

        path = f'{self.__url}{self._org_id}/groups?page={page}&perPage={per_page}'

        try:
            response_json = make_request(session=self.session, url=path, method='GET')
            return GroupsPage(**response_json)
        except APIError as e:
            self.log.error(f"Error getting groups page: {e}")
            raise DirectoryClientError(e)
    

    def get_group_members_v2(self, group_id) -> GroupMembers2:
        """
        Get members of a group
        Use API v2 method: https://yandex.ru/dev/api360/doc/ru/ref/GroupV2Service/GroupService_ListMembers

        Args:
            group_id (number): Group ID number. Use get_groups(page, per_page) to get IDs

        Returns:
            GroupMembers2: Object with lists of group members
        """

        path = f'{self.__url_v2}{self._org_id}/groups/{group_id}/members'

        try:
            response_json = make_request(session=self.session, url=path, method='GET')
            return GroupMembers2(**response_json)
        except APIError as e:
            self.log.error(f"Error getting group members: {e}")
            raise DirectoryClientError(e)
        
    def get_user_2fa(self, user_id: str) -> User2fa:
        """
        Get 2fa status of a user
        Use API v2 method: https://yandex.ru/dev/api360/doc/ru/ref/UserService/UserService_Get2fa

        Args:
            user_id (str): User ID

        Returns:
            User2fa: Object with 2fa status
        """
        
        path = f'{self.__url}{self._org_id}/users/{user_id}/2fa'

        try:
            response_json = make_request(session=self.session, url=path, method='GET')
            return User2fa(**response_json)
        except APIError as e:
            self.log.error(f"Error getting user 2fa: {e}")
            raise DirectoryClientError(e)
           
    def close(self):
        """
        Close client session
        """

        self.session.close()