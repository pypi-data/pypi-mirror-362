from pydantic import BaseModel

class ServiceAppTokenResponse(BaseModel):
    """
    Response from the service app token endpoint
    Details https://yandex.ru/support/yandex-360/business/admin/ru/security-service-applications

    Attributes:
        access_token (str): The access token
        expires_in (int): The number of seconds the token is valid for (always 3600)
        issued_token_type (str): The type of token issued (always access_token)
        scope (str): The scope of the token
        token_type (str): The type of token (always bearer)
    """

    access_token: str
    expires_in: int = 3600
    issued_token_type: str = ''
    scope: str = ''
    token_type: str = ''
    
   
    @property
    def auth_header(self) -> dict:
        """Return the authorization header format for this token"""
        return {"Authorization": f"{self.token_type.capitalize()} {self.access_token}"}