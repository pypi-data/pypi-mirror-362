import time
import httpx
from typing import Any, Dict, Optional
from httpx import RequestError
from y360_orglib.common.exceptions import AuthenticationError, BadRequestError, ConnectionError
from y360_orglib import configure_logger

logger = configure_logger(logger_name = __name__)

def make_request(
    session: httpx.Client,
    method: str,
    url: str,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    max_retries: int = 3,
    retry_delay: float = 1.0
) -> Any:
    """
    Make HTTP request with retry logic and error handling.
    
    Args:
        session: Requests session to use
        method: HTTP method (GET, POST, etc.)
        url: Request URL
        params: URL parameters
        data: Form data
        json: JSON data
        max_retries: Maximum number of retries
        retry_delay: Delay between retries in seconds
        
    Returns:
        Response data as dictionary
        
    Raises:
        APIError: For API-related errors
        AuthenticationError: For authentication failures
        RateLimitError: When rate limited
        ConnectionError: For network issues
    """
    retries = 0
    while retries <= max_retries:
        try:
            response = session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json,
                timeout=30  # Reasonable timeout
            )
            
            # Check for rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', retry_delay))
                logger.warning(f"Rate limited. Retrying after {retry_after} seconds")
                time.sleep(retry_after)
                retries += 1
                continue

            if response.status_code == 500:
                retry_after = int(response.headers.get('Retry-After', retry_delay))
                logger.error(f"Internal Server error. Retrying after {retry_after} seconds")
                time.sleep(retry_after)
                retries += 1
                continue

            if response.status_code == 400:
                raise BadRequestError(f"Request failed: {response.text}")
                
            # Check for auth issues
            if response.status_code in (401, 403):
                raise AuthenticationError(f"Authentication failed {response.status_code}: {response.text}")
                
            # Raise for other bad status codes
            response.raise_for_status()
            
            # Return the JSON response
            return response.json()
        
            
        except RequestError as e:
            if retries < max_retries:
                logger.warning(f"Request failed. Retrying ({retries+1}/{max_retries}): {str(e)}")
                time.sleep(retry_delay)
                retries += 1
            else:
                logger.error(f"Request failed after {max_retries} retries: {str(e)}")
                raise ConnectionError(f"Connection error: {str(e)}") from e
            
        except httpx.HTTPStatusError as e:
                logger.error(f"Request failed after {max_retries} retries: {str(e)}")
                raise ConnectionError(f"Connection error: {str(e)}") from e