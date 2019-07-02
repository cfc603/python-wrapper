import getpass
import os
import requests

from python_wrapper import PYTHON_WRAPPER_API_ENDPOINT


# Maps certain function names to HTTP verbs
VERBS = {
    "create": "POST",
    "read": "GET",
    "update": "PUT",
    "delete": "DELETE"
}

# A list of identifiers that should be extracted and placed into the url
# string if they are passed into the kwargs.
IDENTIFIERS = {
    "console_id": "consoles",
    "domain_name": "webapps",
    "static_id": "static_files",
}


# Define exceptions
class PythonAPIError(Exception):
    pass


class PythonClient(object):
    """
    A generic Python API client.
    """
    api_key = ""
    client = None
    user = None
    path = []

    def __init__(self, api_key=None, path=None, user=None, additional_verbs={},
                 identifiers={}):
        """
        :param api_key: The API key.
        :param path: The current path constructed for this request.
        :param user: username
        :param client: The HTTP client to use to make the request.
        :param additional_vervs: Map additional function name to HTTP verbs
                                 without removing them from path
        :params identifiers: A list of identifiers that should be extracted and
                             placed into the url string if they are passed into
                             the kwargs.
        """
        self.api_key = api_key or os.environ["API_TOKEN"]
        self.path = path or []
        self.user = user or getpass.getuser()
        self.additional_verbs = additional_verbs
        self.identifiers = identifiers

    def __getattr__(self, attr):
        """
        Uses attribute chaining to help construct the url path of the request.
        """
        try:
            return object.__getattr__(self, attr)
        except AttributeError:
            return PythonClient(
                self.api_key,
                self.path + [attr],
                self.user,
                self.additional_verbs,
                self.identifiers
            )

    def construct_request(self, **kwargs):
        """
        :param kwargs: The arguments passed into the request. Valid values are:
            "console_id", "domain_name", and "static_id" will be extracted and
            placed into the url. "data" will be passed seperately. Remaining
            kwargs will be passed as params into request.
        """
        path = self.path[:]

        # Find the HTTP method if we were called with create(), update(),
        # read(), or delete()
        if path[-1] in VERBS.keys():
            action = path.pop()
            method = VERBS[action]
        elif path[-1] in self.additional_verbs.keys():
            method = self.additional_verbs[path[-1]]
        else:
            method = "GET"

        # Extract certain kwargs and place them in the url instead
        for identifier, name in self.identifiers.items():
            value = kwargs.pop(identifier, None)
            if value:
                path.insert(path.index(name)+1, str(value))

        # Need to pass data seperately from rest of kwargs
        data = kwargs.pop("data", None)

        # Build url
        url = PYTHON_WRAPPER_API_ENDPOINT.format(self.user)
        url = url + "/".join(path) + "/"

        return url, method, data, kwargs

    def make_request(self, url, method, token, **kwargs):
        """
        Actually responsible for making the HTTP request.
        :param url: The URL to load.
        :param method: The HTTP method to use.
        :param token: API token
        :param kwargs: Values are passed into :class:`Request <Request>`
        """
        response = requests.request(
            method=method,
            url=url,
            headers={
                "Authorization": "Token {}".format(token),
                "User-Agent": "Python Client",
            },
            **kwargs
        )

        if not response.ok:
            raise PythonAPIError(
                "{} calling API: {}".format(
                    response.status_code, response.text
                )
            )

        return response

    def __call__(self, **kwargs):
        url, method, data, params = self.construct_request(**kwargs)
        return self.make_request(
            url, method, self.api_key, data=data, params=params
        )
