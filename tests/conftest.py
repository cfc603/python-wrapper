import pytest

from python_wrapper.client import PythonClient


@pytest.fixture(scope="session")
def api_client():
    """Returns PythonClient instance"""
    def _get_client(api_endpoint="https://www.example.com/user/testuser/",
                    additional_verbs={}, identifiers={}):
        return PythonClient(
            "api_key",
            api_endpoint=api_endpoint,
            additional_verbs=additional_verbs,
            identifiers=identifiers
        )

    return _get_client
