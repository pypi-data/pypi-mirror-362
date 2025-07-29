from griptape_nodes.retained_mode.events.secrets_events import (
    DeleteSecretValueRequest,
    GetAllSecretValuesRequest,
    GetAllSecretValuesResultSuccess,
    GetSecretValueRequest,
    GetSecretValueResultFailure,
    GetSecretValueResultSuccess,
    SetSecretValueRequest,
)
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes


class TestSecretEvents:
    def test_get_set_delete_secret_value_request(self) -> None:
        GriptapeNodes.handle_request(SetSecretValueRequest(key="SECRET_KEY", value="foo"))
        result = GriptapeNodes.handle_request(GetSecretValueRequest(key="SECRET_KEY"))

        assert isinstance(result, GetSecretValueResultSuccess)

        assert result.value == "foo"

        GriptapeNodes.handle_request(DeleteSecretValueRequest(key="SECRET_KEY"))

        result = GriptapeNodes.handle_request(GetSecretValueRequest(key="SECRET_KEY"))

        assert isinstance(result, GetSecretValueResultFailure)

    def test_get_all_secret_values_request(self) -> None:
        GriptapeNodes.handle_request(SetSecretValueRequest(key="SECRET_KEY_1", value="foo"))
        GriptapeNodes.handle_request(SetSecretValueRequest(key="SECRET_KEY_2", value="foo"))
        result = GriptapeNodes.handle_request(GetAllSecretValuesRequest())

        assert isinstance(result, GetAllSecretValuesResultSuccess)

        assert result.values == {
            "SECRET_KEY_1": "foo",
            "SECRET_KEY_2": "foo",
        }
