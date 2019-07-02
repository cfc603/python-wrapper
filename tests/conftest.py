import pytest

from python_wrapper.client import PythonClient


@pytest.fixture(scope="session")
def api_client():
    """Returns PythonClient instance"""
    def _get_client(user="testuser", additional_verbs={}, identifiers={}):
        return PythonClient(
            "api_key",
            user=user,
            additional_verbs=additional_verbs,
            identifiers=identifiers
        )

    return _get_client
