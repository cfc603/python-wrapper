import pytest
import responses

from python_wrapper.client import PythonAPIError


class PythonClientTestCase(object):

    API_ENDPOINT = "https://www.example.com/user/testuser/"

    def asserts(self, expected_url, method="GET", data=None):
        assert len(responses.calls) == 1
        call = responses.calls[0]
        assert call.response.url == self.get_url(expected_url)
        assert call.request.method == method
        if data:
            for argument in data:
                assert argument in call.response.request.body

    def get_url(self, url):
        return self.API_ENDPOINT + url


class TestMakeRequest(PythonClientTestCase):

    @responses.activate
    def test_make_request(self, api_client):
        responses.add(responses.GET, self.get_url("details/"))
        api_client().details()

        assert len(responses.calls) == 1
        call = responses.calls[0]
        headers = call.request.headers
        assert headers["Authorization"] == "Token api_key"
        assert headers["User-Agent"] == "Python Client"
        assert call.response.ok is True

    @responses.activate
    def test_make_request_not_okay(self, api_client):
        responses.add(responses.GET, self.get_url("detail/"), status=404)

        with pytest.raises(PythonAPIError):
            api_client().detail()

    @responses.activate
    def test_make_request_verb_create(self, api_client):
        url_path = "details/"
        responses.add(responses.POST, self.get_url(url_path))
        api_client().details.create()
        self.asserts(url_path, method="POST")

    @responses.activate
    def test_make_request_verb_read(self, api_client):
        url_path = "details/"
        responses.add(responses.GET, self.get_url(url_path))
        api_client().details()
        self.asserts(url_path)

    @responses.activate
    def test_make_request_verb_update(self, api_client):
        url_path = "details/"
        responses.add(responses.PUT, self.get_url(url_path))
        api_client().details.update()
        self.asserts(url_path, method="PUT")

    @responses.activate
    def test_make_request_verb_delete(self, api_client):
        url_path = "details/"
        responses.add(responses.DELETE, self.get_url(url_path))
        api_client().details.delete()
        self.asserts(url_path, method="DELETE")

    @responses.activate
    def test_make_request_additional_verbs(self, api_client):
        url_path = "details/reload/"
        responses.add(responses.POST, self.get_url(url_path))
        api_client(additional_verbs={"reload": "POST"}).details.reload()
        self.asserts(url_path, method="POST")

    @responses.activate
    def test_make_request_identifiers(self, api_client):
        url_path = "details/123/"
        responses.add(responses.GET, self.get_url(url_path))
        api_client(identifiers={"detail_id": "details"}).details(detail_id=123)
        self.asserts(url_path)

    @responses.activate
    def test_make_request_params_post(self, api_client):
        url_path = "details/"
        responses.add(responses.POST, self.get_url(url_path))
        api_client().details.create(data={
                "domain_name": "www.test.com",
                "python_version": "python27",
        })
        self.asserts(
            url_path,
            "POST",
            ["domain_name=www.test.com", "python_version=python27"]
        )
