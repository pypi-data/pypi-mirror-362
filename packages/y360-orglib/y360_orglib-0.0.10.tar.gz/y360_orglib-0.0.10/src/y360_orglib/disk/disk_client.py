#from time import time
import logging
from typing import List
import httpx

from y360_orglib.common.exceptions import APIError, DiskClientError
from y360_orglib.common.http import make_request
from y360_orglib.disk.models import PublicResourcesList, PublicSettings, Resource
from y360_orglib.logging.config import configure_logger


class DiskClient():
    """
    Yandex Disk client
    
    Args:
        token: Disk User's token
        ssl_verify: Verify SSL certificate
        log_level: Log level
    """
    def __init__(self, token: str, ssl_verify=True, log_level=logging.INFO):
        """
        Initialize Yandex Disk client
        Args:
            token: Disk User's token
            ssl_verify: Verify SSL certificate
            log_level: Log level
        """

        self._token = token
        self.log = configure_logger(logger_name=__name__, level=log_level, console=False)
        self._headers = {'Authorization': 'OAuth ' + token}
        self.session = httpx.Client(base_url='https://cloud-api.yandex.net', verify=ssl_verify)
        self.session.headers.update(self._headers)


    def get_public_resources(self, limit: int = 100, offset: int = 0) -> List[Resource]:
        """
        Get list of public resources from Yandex Disk

        Args:
            limit: Number of resources to return
            offset: Offset of the first resource to return
        Returns:
            List[Resource]: List of public resources
        Raises:
            DiskClientError: If failed to get public resources
        """

        url = '/v1/disk/resources/public'
        params = {
            'limit': limit,
            'offset': offset,
            'fields': 'limit,offset,items.public_key,items.public_url,items.name, items.created,items.modified,items.path,items.type,items.mime_type,items.size'
            }
        
        public_resource_list: List[Resource] = []
        
        while True:
            try:
                #start_time = time()
                res = make_request(session=self.session, method='GET', url=url, params=params)
                #end_time = time()
                #print(f'get_public_resources: {end_time - start_time}')
                #self.log.info(f'get_public_resources: {res}')
                public_resource_part = PublicResourcesList(**res).items
                if len(public_resource_part) == 0:
                    break
                if len(public_resource_list) == 0:
                    public_resource_list = public_resource_part
                else:
                    public_resource_list = public_resource_list + public_resource_part
                params['offset'] += limit
            except APIError as e:
                #self.log.error(f'Error get public resources: {e}')
                raise DiskClientError(e)
        return public_resource_list
        
    
    def get_public_settings(self, path: str) -> PublicSettings:
        """
        Get public settings for resource for provided path
            Args:
                path: Path to resource
            Returns:
                PublicSettings: Public settings for resource
            Raises:
                DiskClientError: If failed to get public settings
        """

        url = '/v1/disk/public/resources/public-settings'
        params = {'path': path, 'allow_address_access': True}
        #start_time = time()
        res = make_request(session=self.session, method='GET', url=url, params=params)
        #self.log.info(f'get_public_settings: {res}')
        #end_time = time()
        #print(f'get_public_settings: {end_time - start_time}')

        public_settings = PublicSettings(**res)

        return public_settings    
    

    def close(self):
        """
        Close Disk client session
        """

        self.session.close()
