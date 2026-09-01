from types import SimpleNamespace

import pytest
import responses

from baremetal_access_dashboard.client import AccessAPIError, request


@responses.activate
def test_project_token_is_forwarded_only_to_internal_api():
    responses.get(
        "http://access-api.test/v1/requests", json=[{"id": "request-1"}],
        headers={"Content-Type": "application/json"},
    )
    result = request(SimpleNamespace(token="project-token"), "GET", "/v1/requests")
    assert result == [{"id": "request-1"}]
    assert responses.calls[0].request.headers["X-Auth-Token"] == "project-token"


@responses.activate
def test_non_json_and_error_responses_fail_closed():
    responses.get(
        "http://access-api.test/v1/requests", body="login", status=200,
        headers={"Content-Type": "text/html"},
    )
    with pytest.raises(AccessAPIError, match="returned 200"):
        request(SimpleNamespace(token="project-token"), "GET", "/v1/requests")


def test_missing_project_token_is_rejected():
    with pytest.raises(AccessAPIError, match="project-scoped"):
        request(SimpleNamespace(token=""), "GET", "/v1/requests")


@responses.activate
def test_idempotency_key_is_forwarded_on_submission():
    responses.post(
        "http://access-api.test/v1/requests", json={"id": "request-1"},
        headers={"Content-Type": "application/json"},
    )
    request(
        SimpleNamespace(token="project-token"), "POST", "/v1/requests",
        json={"profile": "general-1u"}, idempotency_key="request-key-123",
    )
    assert responses.calls[0].request.headers["Idempotency-Key"] == "request-key-123"
