import json, hashlib, requests, requests_cache
import urllib.parse
from typing import Any, Dict, List, Literal, Optional, Self
from datetime import datetime, timedelta, timezone
from ._exceptions import SarvException
from ._mixins import ModulesMixin
from ._type_hints import TimeOutput, SarvLanguageType, RequestMethod, SarvGetMethods
from .modules._base import SarvModule


class SarvClient(ModulesMixin):
    """
    SarvClient provides methods for interacting with the SarvCRM API. 
    It supports authentication, data retrieval, and other API functionalities.
    """
    def __init__(
            self,
            url: str,
            utype: str,
            username: str,
            password: str,
            login_type: Optional[str] = None,
            language: SarvLanguageType = 'en_US',
            is_password_md5: bool = False,
            caching: bool = False,
            cache_backend: Literal['memory', 'sqlite'] = 'memory',
        ) -> None:
        """
        Initialize the SarvClient.

        Args:
            url (str): The base URL for the SarvCRM API.
            utype (str): The user type for authentication.
            username (str): The username for authentication.
            password (str): The password for authentication.
            login_type (Optional[str]): The login type for authentication.
            language (SarvLanguageType): The language to use, default is 'en_US'.
            is_password_md5 (bool): Whether the password is already hashed using MD5.
        """
        self._url = url
        self._utype = utype
        self._username = username
        self._password = password if is_password_md5 else self.hash_password(password)
        self._login_type = login_type
        self._language = language
        self._caching = caching
        self._cache_backend = cache_backend

        self._token: str = ''

        self.enable_caching() if self._caching else self.disable_caching()

        super().__init__()


    def _add_headers(self) -> None:
        """
        Adds required sarvcrm headers to session.
        """
        self._session.headers.update({'Content-Type': 'application/json'})
        self._session.headers.update({'Accept': 'application/json'})

    def _create_get_params(
            self, 
            sarv_get_method: Optional[SarvGetMethods] = None,
            sarv_module: Optional[SarvModule | str] = None,
            **addition
        ) -> Dict[str, Any]:
        """
        Create the GET parameters with the method and module.

        Args:
            sarv_get_method (SarvGetMethods): The API method to call.
            sarv_module (Optional[SarvModule | str]): The module name or object.
            addition: Additional parameters to include in the GET request.

        Returns:
            dict: The constructed GET parameters.
        """
        module_name = None

        if sarv_module is not None:
            if isinstance(sarv_module, SarvModule):
                module_name = sarv_module._module_name
            elif isinstance(sarv_module, str):
                module_name = sarv_module
            else:
                raise TypeError(f'Module type must be instance of SarvModule or str not {sarv_module.__class__.__name__}')

        get_parms = {
            'method': sarv_get_method,
            'module': module_name,
        }
        get_parms = {k: v for k, v in get_parms.items() if v is not None}

        if addition:
            get_parms.update(**addition)

        return get_parms

    def enable_caching(self) -> None:
        """
        Enables the caching and replaces `Session` with `CachedSession` or creates it.
        """
        self._session = requests_cache.CachedSession(
            cache_name='sarv_api_cache',
            backend=self._cache_backend,
            allowable_methods=('GET', 'POST'),
            allowable_codes=(200,),
        )
        self._add_headers()

    def disable_caching(self) -> None:
        """
        Disables the caching and replaces `CachedSession` with `Session` or creates it.
        """
        self._session = requests.Session()
        self._add_headers()


    def _send_request(
            self, 
            request_method: RequestMethod,
            endpoint: Optional[str] = None,
            head_params: Optional[dict] = None,
            get_params: Optional[dict] = None,
            post_params: Optional[dict] = None,
            caching: bool = False,
            expire_after: int = 300,
        ) -> Any:
        """
        Send a request to the Sarv API and return the response data.

        Args:
            request_method (RequestMethod): The HTTP method for the request ('GET', 'POST', etc.).
            head_parms (dict): The headers for the request.
            get_parms (dict): The GET parameters for the request.
            post_params (dict): The POST parameters for the request.

        Returns:
            Any: The data parameter from the server response that can be `List` or `Dict`

        Raises:
            SarvException: If the server returns an error response.
        """
        head_params = head_params or {}
        get_params = get_params or {}
        post_params = post_params or {}

        if self._token:
            head_params['Authorization'] = f'Bearer {self._token}'

        kwargs = {
            'method': request_method,
            'url': urllib.parse.urljoin(self._url.rstrip('/') + '/', (endpoint or '').lstrip('/')),
            'headers': head_params,
            'params': get_params,
            'json': post_params,
            'verify': True,
        }

        if isinstance(self._session, requests_cache.CachedSession):
            ## Use cache
            if caching:
                kwargs.update({'expire_after': expire_after})
                response: requests.Response = self._session.request(**kwargs)

            ## If caching enabled but user dont want to use it
            else:
                with self._session.cache_disabled():
                    response: requests.Response = self._session.request(**kwargs)

        else:
            ## Normal request without caching
            response: requests.Response = self._session.request(**kwargs)

        # Check for Server respond
        try:
            # Deserialize sarvcrm servers response
            response_dict: dict = response.json()

        # Raise this on quirky responses from Sarvcrm servers
        # Sometimes the servers send other content types instead of json
        except json.decoder.JSONDecodeError:
            if 'MySQL Error' in response.text:
                raise SarvException(
                    'There are Errors in the database\n'
                    'if you are sending raw SQL Query to server\n'
                    'please check syntax and varible names'
                )
            else:
                raise SarvException(
                    'Unkhown Error From Server while parsing json'
                )

        response.raise_for_status()
        return response_dict.get('data', {})


    def login(self) -> str:
        """
        Authenticate the user and retrieve an access token.

        Returns:
            str: The access token for authenticated requests.
        """
        post_params = {
            'utype': self._utype,
            'user_name': self._username,
            'password': self._password,
            'login_type': self._login_type,
            'language': self._language,
        }
        post_params = {k: v for k, v in post_params.items() if v is not None}

        data: Dict[str, Any] = self._send_request(
            request_method='POST',
            get_params=self._create_get_params('Login'), 
            post_params=post_params,
        )

        token = data.get('token', '')

        if token is not None:
            self._token = token
            return self._token
        else:
            raise SarvException('client did not get token from login request')

    def logout(self) -> None:
        """
        Clears the access token from the instance.

        This method should be called to invalidate the session.
        """
        if self._token:
            self._token = ''


    def search_by_number(
            self,
            number: str,
            module: Optional[SarvModule | str] = None,
            ) -> List[Dict[str, Any]]:
        """
        Search the CRM by phone number and retrieve the module item.

        Args:
            number (str): The phone number to search for.
            module (Optional[SarvModule | str]): The module to search in.

        Returns:
            dict: The data related to the phone number if found.
        """
        return self._send_request(
            request_method = 'GET',
            get_params = self._create_get_params(
                'SearchByNumber', 
                sarv_module = module, 
                number = number,
            ),
        )

    @staticmethod
    def iso_time_output(output_method: TimeOutput, dt: datetime | timedelta) -> str:
        """
        Generate a formatted string from a datetime or timedelta object.

        These formats are compliant with the SarvCRM API time standards.

        Args:
            output_method (TimeOutput): Determines the output format ('date', 'datetime', or 'time').
            dt (datetime | timedelta): A datetime or timedelta object.

        Returns:
            str: A string representing the date, datetime, or time.
                - date: "YYYY-MM-DD"
                - datetime: "YYYY-MM-DDTHH:MM:SS+HH:MM"
                - time: "HH:MM:SS"
        """
        if isinstance(dt, timedelta):
            dt = datetime.now(timezone.utc) + dt

        if output_method == 'date':
            return dt.date().isoformat()

        elif output_method == 'datetime':
            return dt.astimezone().isoformat(timespec="seconds")

        elif output_method == 'time':
            return dt.time().isoformat(timespec="seconds")

        else:
            raise TypeError(f'Invalid output method: {output_method}')

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Returns the acceptable hash for SarvCRM Login

        Args:
            password(str): your password
        
        Returns:
            str: md5 hashed password
        """
        return hashlib.md5(password.encode('utf-8')).hexdigest()


    def __enter__(self) -> Self:
        """Basic Context Manager for clean code execution"""
        if not self._token:
            self.login()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Basic Context Manager for clean code execution"""
        self.logout()


    def __repr__(self):
        """
        Provides a string representation for debugging purposes.

        Returns:
            str: A string containing the class name and key attributes.
        """
        return f'{self.__class__.__name__}(utype={self._utype}, username={self._username})'

    def __str__(self) -> str:
        """
        Provides a human-readable string representation of the instance.

        Returns:
            str: A simplified string representation of the instance.
        """
        return f'<SarvClient {self._utype}-{self._username}>'