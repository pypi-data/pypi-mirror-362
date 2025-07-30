from pbi import PowerBIClient

def test_client_init(monkeypatch):
    class MockResponse:
        def json(self):
            return {'access_token': 'dummy_token'}

    def mock_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)
    client = PowerBIClient("tenant", "client", "secret")
    assert client.access_token == "dummy_token"
