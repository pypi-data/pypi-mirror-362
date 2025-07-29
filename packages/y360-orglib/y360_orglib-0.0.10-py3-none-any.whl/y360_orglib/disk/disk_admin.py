


import logging
from typing import List
import httpx
import urllib.parse
from y360_orglib.common.exceptions import APIError, DiskClientError
from y360_orglib.common.http import make_request
from y360_orglib.disk.models import PublicSettings, ResourceListShort, ResourceShort
from y360_orglib.logging.config import configure_logger


class DiskAdminClient():
    """ Disk Admin Client
    Uses admin access rights to find shared resources
    More info https://yandex.ru/dev/disk-api/doc/ru/reference/public-owned-by-user
    """

    def __init__(self, token: str, org_id: str, ssl_verify=True, log_level=logging.INFO):
        """ Initialize Disk Admin Client
        Uses admin access rights to find shared resources
        More info https://yandex.ru/dev/disk-api/doc/ru/reference/public-owned-by-user

        Attributes:
            token (str): Organization Admin OAuth token. Required scope: cloud_api:disk.read
            ssl_verify (bool): Verify SSL certificate
            log_level (int): Log level
        """

        self._token = token
        self._org_id = org_id
        self.log = configure_logger(logger_name=__name__, level=log_level, console=False)
        self._headers = {'Authorization': 'OAuth ' + token}
        self.session = httpx.Client(base_url='https://cloud-api.yandex.net', verify=ssl_verify)
        self.session.headers.update(self._headers)


    def get_user_public_resources(self, user_id: str, limit: int = 100, offset: int = 0) -> List[ResourceShort]:
        """ Get list of public resources shared by User
        Attributes:
            user_id (str): User ID
            limit (int): Number of resources to return
            offset (int): Offset of the first resource to return
        Returns:
            List[ResourceShort]: All user shared resources
        Raises:
            DiskClientError: If failed to get shared resources
        """

        url = '/v1/disk/public/resources/admin/public-resources'
        params = {
            'user_id': user_id,
            'org_id': self._org_id,
            'limit': limit,
            'offset': offset
            }
        
        public_resource_list: List[ResourceShort] = []
        
        while True:
            try:
                res = make_request(session=self.session, method='GET', url=url, params=params)

                public_resource_part = ResourceListShort(**res).items
                if len(public_resource_part) == 0:
                    break
                if len(public_resource_list) == 0:
                    public_resource_list = public_resource_part
                else:
                    public_resource_list = public_resource_list + public_resource_part
                params['offset'] += limit
            except APIError as e:
                raise DiskClientError(e)
        return public_resource_list
        
    def get_public_settings_by_key(self, public_key: str) -> PublicSettings:
        """ Get public settings by public key (hash)
        Attributes:
            public_key (str): Public key (hash)
        Returns:
            PublicSettings: Public settings
        Raises:
            DiskClientError: If failed to get public settings
        """

        url = '/v1/disk/public/resources/admin/public-settings'
        params = {'public_key': urllib.parse.quote(public_key, safe='')}

        try: 
            res = make_request(session=self.session, method='GET', url=url, params=params)
            public_settings = PublicSettings(**res)
            return public_settings    
        except APIError as e:
            raise DiskClientError(f'Failed to get public settings for public key {public_key}: {e}')
        
    def get_public_settings_by_path(self, user_id: str, path: str) -> PublicSettings:
        """ Get public settings by path
        Attributes:
            user_id (str): User ID
            path (str): Path to resource
        Returns:
            PublicSettings: Public settings
        Raises:
            DiskClientError: If failed to get public settings
        """

        url = '/v1/disk/public/resources/admin/public-settings-by-path'
        path_short = path[5:]
        params = {
            'user_id': user_id,
            'path': path_short
            }

        try: 
            res = make_request(session=self.session, method='GET', url=url, params=params)
            public_settings = PublicSettings(**res)
            return public_settings    
        except APIError as e:
            raise DiskClientError(f'Failed to get public settings for path {path_short}: {e}')




    def close(self):
        """
        Close Disk client session
        """

        self.session.close()
