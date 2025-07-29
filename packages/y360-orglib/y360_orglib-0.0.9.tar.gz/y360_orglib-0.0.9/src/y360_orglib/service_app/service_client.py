
import httpx
from y360_orglib import configure_logger
from y360_orglib.common.exceptions import APIError, ServiceAppError
from y360_orglib.common.http import make_request

from y360_orglib.service_app.models import ServiceAppTokenResponse


class ServiceAppClient:
    """
    Service App Client

    Args:
        client_id: Service App Client ID
        client_secret: Service App Client Secret
        ssl_verify: Verify SSL certificate
    """

    def __init__(self, client_id, client_secret, ssl_verify=True):
        """
        Initialize the Service App Client

        Args:
            client_id: Service App Client ID
            client_secret: Service App Client Secret
            ssl_verify: Verify SSL certificate
        """

        self.client_id = client_id
        self.client_secret = client_secret
        self.session = httpx.Client(verify=ssl_verify)

    def get_service_app_token(self, subject_token, subject_token_type = 'urn:yandex:params:oauth:token-type:email') -> ServiceAppTokenResponse:
        """
        Get a service app token for for given User (subject_token)

        Args:
            subject_token: User Id or Email
            subject_token_type: The type of the subject token.\n
                If the subject_token is a User ID, the subject_token_type should be 'urn:yandex:params:oauth:token-type:uid'.\n
                If the subject_token is an Email, the subject_token_type should be 'urn:yandex:params:oauth:token-type:email'.\n
                Default value is 'urn:yandex:params:oauth:token-type:email'.\n
        Returns:
            ServiceAppTokenResponse: Response with service app token for provided User

        Raises:
            ServiceAppError: If failed to get service app token
        """
        
        logger = configure_logger(logger_name=__name__, console=False)
        
        path, headers, data = self._get_headers(subject_token, subject_token_type)

        try:
            self.session.headers.update(headers)
            response_json = make_request(session=self.session, url=path, method='POST', data=data)
            token_response = ServiceAppTokenResponse(**response_json)
            return token_response
        except APIError as e:
            logger.error(f"Failed to get service app token: {e}")
            raise ServiceAppError(e)
    

    def _get_headers(self, subject_token, subject_token_type):
        path = 'https://oauth.yandex.ru/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'subject_token': subject_token,
            'subject_token_type': subject_token_type
        }

        return path, headers, data
    

    def close(self):
        """
        Close the client session
        """

        self.session.close()
    