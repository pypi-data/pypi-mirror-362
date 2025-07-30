from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakPostError
from pydantic import BaseModel, Field
from typing import Optional, Union
from novara.config import AuthConfig, config
from requests.exceptions import *
from requests.auth import AuthBase, HTTPBasicAuth, HTTPDigestAuth
from urllib.parse import urljoin

import time
import webbrowser
import requests


class Token_Response(BaseModel):
    access_token:str
    refresh_token:str
    expires_in:int
    refresh_expires_in:int
    token_type:str
    session_state:str
    scope:str
    not_before_policy:int = Field(alias='not-before-policy')

class Device_Response(BaseModel):
    device_code:str
    user_code:str
    verification_uri:str
    verification_uri_complete:str
    expires_in:int
    interval:int

class UserInfoModel(BaseModel):
    id:Optional[str] = Field(alias='sub')
    username:Optional[str] = Field(alias='preferred_username')
    email:Optional[str]
    email_verified:Optional[bool] = False

CLIENT_ID='novara-cli'

class KeycloakOIDCAuth(AuthBase):
    auth_config:AuthConfig
    client:KeycloakOpenID = None

    def __init__(self, auth_config:AuthConfig):
        self.auth_config = auth_config
        self.client = KeycloakOpenID(server_url=self.auth_config.auth_server_url, realm_name='oauth2-proxy', client_id='novara-cli')
        if self.auth_config.valide_until and self.auth_config.valide_until > time.time():
            return
        device_response = Device_Response.model_validate(self.client.device(scope='openid'))

        webbrowser.open(device_response.verification_uri_complete)
        print(f'login at {device_response.verification_uri_complete} \n or at {device_response.verification_uri} with code {device_response.user_code}')

        for _ in range(device_response.expires_in // device_response.interval):
            try:
                raw_token = self.client.token(grant_type='urn:ietf:params:oauth:grant-type:device_code', device_code=device_response.device_code)
                break
            except KeycloakPostError as e:
                if b'authorization_pending' in e.error_message:
                    time.sleep(device_response.interval)
                    continue
                raise e

        raw_token['valide_until'] = time.time() + raw_token['refresh_expires_in']

        self.auth_config.update(raw_token)

    def refresh_auth_token(self):
        if time.time() < self.auth_config.valide_until:
            try:
                raw_tokens = self.client.refresh_token(self.auth_config.refresh_token)
            except KeycloakPostError:
                self.auth_config.valide_until = None
                self.__init__(self.auth_config)
                return
            raw_tokens['valide_until'] = time.time() + raw_tokens['refresh_expires_in']
            self.auth_config.update(raw_tokens)
        
    def get_user_info(self) -> UserInfoModel:
        raw_user_info = self.client.userinfo(self.auth_config.access_token)
        print(raw_user_info)
        return UserInfoModel.model_validate(raw_user_info)

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        r.headers['Authorization'] = f'{self.auth_config.token_type} {self.auth_config.access_token}'
        return r

class AuthSession(requests.Session):
    auth:Union[KeycloakOIDCAuth, HTTPBasicAuth, HTTPDigestAuth, None] = None
    def __init__(self, auth_config:AuthConfig, **kwargs):
        super().__init__()
        self.auth_config = auth_config
        match auth_config.auth_type:
            case 'oauth':
                self.auth = KeycloakOIDCAuth(auth_config)
            case 'basic':
                self.auth = HTTPBasicAuth(auth_config.username, auth_config.password)
            case 'digest':
                self.auth = HTTPDigestAuth(auth_config.username, auth_config.password)
        
        self.on_update()

    def get_user_info(self):
        if hasattr(self.auth, 'get_user_info'):
            return self.auth.get_user_info()
        return UserInfoModel(name=self.auth_config.username, email=None)

    def refresh_token(self):
        if hasattr(self.auth, 'refresh_auth_token'):
            self.auth.refresh_auth_token()
            self.on_update()
        
    def on_update(self):
        pass

    def request(self,
                method,
                url,
                params=None,
                data=None,
                headers=None,
                cookies=None,
                files=None,
                auth=None,
                timeout=None,
                allow_redirects=True,
                proxies=None,
                hooks=None,
                stream=None,
                verify=None,
                cert=None,
                json=None):

        self.refresh_token()

        return super().request(method=method, 
                               url=url, 
                               params=params, 
                               data=data, 
                               headers=headers, 
                               cookies=cookies, 
                               files=files, 
                               auth=auth or self.auth, 
                               timeout=timeout,
                               allow_redirects=allow_redirects, 
                               proxies=proxies, 
                               hooks=hooks, 
                               stream=stream, 
                               verify=verify, 
                               cert=cert, 
                               json=json)

class LazyInitRequest(AuthSession):
    def __init__(self):
        self.is_initialized = False

    def on_update(self):
        config.save()

    def request(self, 
                method,
                url:str,
                params=None,
                data=None,
                headers=None,
                cookies=None,
                files=None,
                auth=None,
                timeout=None,
                allow_redirects=True,
                proxies=None,
                hooks=None,
                stream=None,
                verify=None,
                cert=None,
                json=None):
        
        if not url.startswith('http'):
            url = urljoin(config.auth_config.server_url, url)
        if not self.is_initialized:
            self.is_initialized = True
            super().__init__(config.auth_config)
        return super().request(method=method, 
                               url=url, 
                               params=params, 
                               data=data, 
                               headers=headers, 
                               cookies=cookies, 
                               files=files, 
                               auth=auth, 
                               timeout=timeout,
                               allow_redirects=allow_redirects, 
                               proxies=proxies, 
                               hooks=hooks, 
                               stream=stream, 
                               verify=verify, 
                               cert=cert, 
                               json=json)

request = LazyInitRequest()