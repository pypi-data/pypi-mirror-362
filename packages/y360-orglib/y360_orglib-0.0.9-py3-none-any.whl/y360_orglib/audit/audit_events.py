
import logging

import httpx
from time import sleep
from typing import List

from pydantic import ValidationError
from y360_orglib.audit.event_models import AuditLogEventsPage, EnrichedEvent
from y360_orglib.common.exceptions import EventAuditError
from y360_orglib.common.http import make_request



class AuditEvents():
    """
    Client for Yandex 360 Audit Events Cloud API
    Allows to get organization audit logs. See more details: https://yandex.ru/dev/api360/doc/ru/audit-logs/get-logs
    Args:
        api_key: OAuth token
        org_id: Organization ID
        ssl_verify: Verify SSL certificate
    """

    __url = 'https://cloud-api.yandex.net/v1/auditlog/organizations/'
    
    def __init__(self, api_key: str, org_id: str, ssl_verify=True):
        """
        Initialize the Audit Events Client
        Args:
            api_key: OAuth token
            org_id: Organization ID
            ssl_verify: Verify SSL certificate
        """

        self.__logger = logging.getLogger(__name__)
        self.__org_id = org_id
        self.__headers = {
            "Authorization": f"OAuth {api_key}",
            "content-type": "application/json",
        }
        self.__session = httpx.Client(verify=ssl_verify, timeout=10.0)
        self.__session.headers.update(self.__headers)
        self.__request_url = self.__url + self.__org_id + '/events'


    def get_events(self, started_at, ended_at, count = 100, iteration_key = 0, **kwargs) -> List[EnrichedEvent]:
        """
        Get events page from Audit Events API
        Args:
            started_at: Start date and time of the period to get events from. ISO 8601 format. Example: 2024-01-31T23:59:59+00:00
            ended_at: End time of the period to get events from. ISO 8601 format. Example: 2024-01-31T23:59:59+00:00
            count: Number of events to get. Maximum value is 100. Default value is 100.
            iteration_key: Iteration key to get next page of events

            Other arguments are passed as kwargs for details see https://yandex.ru/dev/api360/doc/ru/audit-logs/get-logs
        
        """

        params = {
            "started_at": started_at,
            "ended_at": ended_at,
            "count": count,
            "iteration_key": iteration_key
        }

        params.update(**kwargs)

        
        has_more_events = True
        enriched_events: List[EnrichedEvent] = []
        
        while has_more_events:
            try:
                self.__logger.debug(f"Getting events page with request params: {params}")
                events_response_json = make_request(session=self.__session, url=self.__request_url, params=params, method='GET')
                #events_response = self.__session.get(url=self.__session.base_url, params=params)
                if 'code' in events_response_json:
                    raise EventAuditError(f"Error in logs request. Server response: {events_response_json}")
                else:
                    events_page = AuditLogEventsPage(**events_response_json)
                    self.__logger.info(f"Got events page with {len(events_page.items)} events")
                has_more_events = events_page.iteration_key is not None
                if has_more_events:
                    params["iteration_key"] = events_page.iteration_key
                else:
                    self.__logger.debug("No more events to load")         
                enriched_events.extend(events_page.items)
                sleep(1)
            except ValidationError as e:
                self.__logger.error(f"Failed to validate server response with error: {e}")
                self.__logger.error(f"Server response object {events_response_json}")
                raise EventAuditError(f"Failed to validate server response object: {events_response_json}")
        self.__logger.info(f"Loaded {len(enriched_events)} events")
        return enriched_events

    def close(self):
        self.__session.close()




