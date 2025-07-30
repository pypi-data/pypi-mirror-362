import asyncio
import json as json_lib
import pickle
from time import perf_counter

import httpx
import pytest
import structlog
from hypothesis import given
from hypothesis import strategies as st
from pydantic import SecretStr
from structlog.testing import LogCapture

from arraylake.api_utils import (
    ArraylakeHttpClient,
    TokenAuth,
    UserAuth,
    calc_backoff,
    handle_response,
    retry_on_exception,
)
from arraylake.config import config
from arraylake.repos.v1.metastore.http_metastore import (
    HttpMetastoreConfig,
    HttpMetastoreDatabase,
    HttpMetastoreDatabaseConfig,
)
from arraylake.token import AuthException
from arraylake.types import OauthTokens


def _get_test_tokens(fname) -> dict:
    """helper function to independently load oauth tokens"""
    with fname.open() as f:
        tokens = json_lib.load(f)
    return tokens


# regression test for
# https://github.com/earth-mover/arraylake/issues/302
# https://github.com/earth-mover/arraylake/issues/303
@pytest.mark.asyncio
async def test_http_request_headers(respx_mock, token, test_token_file) -> None:
    api_url = "https://foo.com"

    if token is None:
        tokens = _get_test_tokens(test_token_file)
        test_token = tokens["id_token"]
    else:
        test_token = token

    client = ArraylakeHttpClient(api_url, token=token)

    custom_headers = {"special": "header"}

    route = respx_mock.get(api_url + "/bar").mock(return_value=httpx.Response(httpx.codes.OK))

    async def check_client(client):
        assert str(client.api_url) == api_url
        response = await client._request("GET", "bar", headers=custom_headers)
        assert response.status_code == 200

    await check_client(client)
    assert route.calls.last.request.headers["authorization"] == f"Bearer {test_token}"
    assert route.calls.last.request.headers["special"] == "header"
    assert route.calls.last.request.headers["arraylake-feature-managed-sessions"] == "True"
    c1_headers = dict(route.calls.last.request.headers)

    client2 = pickle.loads(pickle.dumps(client))

    await check_client(client2)
    assert route.calls.last.request.headers == c1_headers

    # Ensure that changes to the managed sessions config setting propagate
    with config.set({"server_managed_sessions": False}):
        client = ArraylakeHttpClient(api_url, token=token)
        await check_client(client)
        assert route.calls.last.request.headers["authorization"] == f"Bearer {test_token}"
        assert route.calls.last.request.headers["special"] == "header"
        assert route.calls.last.request.headers["arraylake-feature-managed-sessions"] == "False"


def test_calc_backoff() -> None:
    assert calc_backoff(0, backoff_factor=0.5, jitter_ratio=0.1, max_backoff_wait=10) == 0
    assert calc_backoff(1, backoff_factor=0.5, jitter_ratio=0.0, max_backoff_wait=10) == 0.5
    assert calc_backoff(1, backoff_factor=0.5, jitter_ratio=0.1, max_backoff_wait=10) in [0.45, 0.55]


@given(
    st.integers(min_value=0, max_value=100),
    st.floats(min_value=0, max_value=100, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, max_value=1),
    st.integers(min_value=0, max_value=100),
)
def test_calc_backoff_is_valid(attempt, backoff_factor, jitter_ratio, max_backoff_wait) -> None:
    backoff = calc_backoff(attempt, backoff_factor=backoff_factor, jitter_ratio=jitter_ratio, max_backoff_wait=max_backoff_wait)
    assert backoff >= 0
    assert backoff <= max_backoff_wait


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [429, 502, 503, 504])
@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE", "POST"])
async def test_retries(respx_mock, status_code, method) -> None:
    mock_url = "https://foo.bar/"

    clock = []

    def side_effect(request, route):
        clock.append(perf_counter())
        if route.call_count > 2:
            return httpx.Response(200)
        return httpx.Response(status_code)

    route = respx_mock.request(method, mock_url).mock(side_effect=side_effect)
    client = ArraylakeHttpClient(mock_url)
    response = await client._request(method, "")
    assert response.status_code == 200
    assert route.call_count == 4

    # verify increasing backoff
    diff = [clock[n] - clock[n - 1] for n in range(1, len(clock))]
    assert diff[-1] > diff[0]


@pytest.mark.asyncio
async def test_retry_after_header(respx_mock) -> None:
    mock_url = "https://foo.bar/"

    clock = []
    retry_after_time = 1

    def side_effect(request, route):
        clock.append(perf_counter())
        if route.call_count > 0:
            return httpx.Response(200)
        return httpx.Response(429, headers={"Retry-After": str(retry_after_time)})

    route = respx_mock.get(mock_url).mock(side_effect=side_effect)
    client = ArraylakeHttpClient(mock_url)
    response = await client._request("GET", "")
    assert response.status_code == 200
    assert route.call_count == 2

    # verify specified wait time
    diff = clock[1] - clock[0]
    assert diff > retry_after_time


@pytest.mark.parametrize("method", ["GET", "PUT", "POST"])
@pytest.mark.parametrize("headers", [None, {"foo": "bar"}, {"Authorization": "abc"}])
@pytest.mark.parametrize("json", [None, {"abc": "xyz"}])
def test_token_auth_does_not_mutate_request(test_token, method, headers, json) -> None:
    auth = TokenAuth(test_token)
    url = "https://foo.com"
    request = httpx.Request(method, url, headers=headers, json=json)
    orig_headers = request.headers.copy()
    request = next(auth.auth_flow(request))
    # check that authorization header was inserted
    assert request.headers["Authorization"] == f"Bearer {test_token}"

    # check that the rest of the request is the same
    assert request.method == method
    assert request.url == url
    for k, header in orig_headers.items():
        # authorization is one the key that we expect to be mutated (if it was on the original request for some reason)
        if k != "authorization":  # keys are lower case
            assert header == request.headers.get(k)
    if json:
        assert json_lib.dumps(json).encode("utf-8") in request.content


@pytest.mark.asyncio
async def test_user_auth_requires_login(tmp_path) -> None:
    # Note: while this test does not explicitly await anything, the UserAuth class does include an asyncio.Lock
    # therefore, we mark this test for async execution
    bad_token_file = str(tmp_path / "tokens.json")
    with config.set({"service.token_path": bad_token_file}):
        with pytest.raises(AuthException, match=r"Not logged in, please log in .*"):
            UserAuth("https://foo.com")


@pytest.mark.asyncio
async def test_auth_adds_authorization_header_token_auth(test_token, respx_mock) -> None:
    auth = TokenAuth(test_token)
    route = respx_mock.get("https://foo.com").mock(return_value=httpx.Response(httpx.codes.OK))
    async with httpx.AsyncClient(auth=auth) as client:
        await client.get("https://foo.com")
    assert route.calls.last.request.headers["Authorization"] == f"Bearer {test_token}"


@pytest.mark.asyncio
async def test_auth_adds_authorization_header_user_auth(test_token_file, respx_mock) -> None:
    auth = UserAuth("https://foo.com")
    tokens = _get_test_tokens(test_token_file)
    test_token = tokens["id_token"]
    route = respx_mock.get("https://foo.com").mock(return_value=httpx.Response(httpx.codes.OK))
    async with httpx.AsyncClient(auth=auth) as client:
        await client.get("https://foo.com")
    assert route.calls.last.request.headers["Authorization"] == f"Bearer {test_token}"


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE"])
@pytest.mark.parametrize("headers", [None, {"foo": "bar"}, {"Authorization": "abc"}])
@pytest.mark.parametrize("json", [None, {"abc": "xyz"}])
async def test_user_auth_does_not_mutate_request(test_token_file, method, headers, json) -> None:
    url = "https://foo.com"
    auth = UserAuth(url)

    tokens = _get_test_tokens(test_token_file)
    test_token = tokens["id_token"]

    request = httpx.Request(method, url, headers=headers, json=json)
    orig_headers = request.headers.copy()
    request_gen = auth.async_auth_flow(request)
    request = await request_gen.__anext__()  # TODO: switch to anext(request_gen) when python>=3.10
    # check that authorization header was inserted
    assert request.headers["Authorization"] == f"Bearer {test_token}"

    # check that the rest of the request is the same
    assert request.method == method
    assert request.url == url
    for k, header in orig_headers.items():
        # authorization is one the key that we expect to be mutated (if it was on the original request for some reason)
        if k != "authorization":  # keys are lower case
            assert header == request.headers.get(k)
    if json:
        assert json_lib.dumps(json).encode("utf-8") in request.content


@pytest.mark.asyncio
async def test_user_auth_refresh_request(test_token_file, mock_auth_provider_config) -> None:
    # Note: while this test does not explicitly await anything, the UserAuth class does include an asyncio.Lock
    # therefore, we execute this mark this test for async execution
    url = "https://foo.com"
    auth = UserAuth(url)

    tokens = _get_test_tokens(test_token_file)
    refresh_token = tokens["refresh_token"]

    request = auth._token_handler.refresh_request
    content = dict(item.split("=") for item in request.content.decode("utf-8").split("&"))

    assert request.method == "POST"
    assert request.url.path == "/oauth/token"
    assert content["refresh_token"] == refresh_token


@pytest.mark.asyncio
async def test_user_auth_refreshes_on_401(test_token_file, respx_mock, mock_auth_provider_config) -> None:
    url = "https://foo.com"
    auth = UserAuth(url)

    # orig_tokens = _get_test_tokens(test_token_file)
    new_tokens = {
        "access_token": "akdh83",
        "id_token": "asdjkd7367",
        "refresh_token": "2383478nd",
        "expires_in": 86400,
        "token_type": "Bearer",
    }

    refresh_request = auth._token_handler.refresh_request
    respx_mock.get(url__eq=url).mock(side_effect=[httpx.Response(httpx.codes.UNAUTHORIZED), httpx.Response(httpx.codes.OK)])
    respx_mock.post(refresh_request.url).mock(return_value=httpx.Response(httpx.codes.OK, json=new_tokens))

    async with httpx.AsyncClient(auth=auth) as client:
        result = await client.get(url)
        assert result.status_code == httpx.codes.OK

    updated_tokens = _get_test_tokens(test_token_file)
    assert new_tokens == updated_tokens


@pytest.mark.asyncio
async def test_sync_user_auth_flow_raises(test_token_file) -> None:
    # Note: while this test does not explicitly await anything, the UserAuth class does include an asyncio.Lock
    # therefore, we execute this mark this test for async execution
    url = "https://foo.com"
    auth = UserAuth(url)

    request = httpx.Request("GET", url)
    with pytest.raises(RuntimeError, match="Sync auth flow not implemented yet"):
        auth.sync_auth_flow(request)

    with httpx.Client(auth=auth) as client:
        with pytest.raises(RuntimeError, match="Sync auth flow not implemented yet"):
            client.get(url)


# additional tests to write:
# test that we handle a failure to refresh gracefully


@pytest.mark.asyncio
async def test_retry_on_exception_decorator() -> None:
    @retry_on_exception(ValueError, n=3)
    async def raise_value_error():
        raise ValueError

    # Test that the function raises an exception if it fails 3 times
    with pytest.raises(ValueError):
        await raise_value_error()

    # Test that the function succeeds if it fails fewer than 3 times
    count = 0

    @retry_on_exception(ValueError, n=3)
    async def raise_value_error_then_succeed():
        nonlocal count
        count += 1
        if count < 2:
            raise ValueError
        else:
            return True

    assert await raise_value_error_then_succeed() is True
    assert count == 2

    # test that other errors are raised immediately
    count = 0

    @retry_on_exception(ValueError, n=3)
    async def raise_key_error():
        nonlocal count
        count += 1
        raise KeyError

    with pytest.raises(KeyError):
        await raise_key_error()
    assert count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("exception", [httpx.RemoteProtocolError, httpx.ConnectError])
async def test_retry_request_connection_errors(exception, respx_mock) -> None:
    # regression test for https://github.com/earth-mover/arraylake/issues/514

    mock_url = "https://foo.bar/"
    route = respx_mock.request("POST", mock_url).mock(side_effect=[exception, httpx.Response(200)])
    client = ArraylakeHttpClient(mock_url)
    response = await client._request("POST", "")
    assert response.status_code == 200
    assert route.call_count == 2

    # test that repeated exceptions are passed through
    mock_url = "https://spam.bar/"
    route = respx_mock.request("POST", mock_url).mock(side_effect=5 * [exception])
    client = ArraylakeHttpClient(mock_url)
    with pytest.raises(exception):
        await client._request("POST", "")
    assert route.call_count == 5


@pytest.mark.asyncio
async def test_token_refresh_from_metastoredb(test_token_file, respx_mock, mock_auth_provider_config) -> None:
    # regression test for https://linear.app/earthmover/issue/EAR-545/404-on-refresh-token-attempt
    with test_token_file.open() as f:
        test_tokens = OauthTokens.model_validate_json(f.read())

    # we test the refresh flow, which yields a new set of id+access tokens
    # this object is what we expect our handler token state to look like after refresh
    refreshed_test_tokens = test_tokens.model_copy(
        update={"id_token": SecretStr("new-id-token"), "access_token": SecretStr("new-access-token")}
    )

    api_url = "https://foo.com"

    # the refresh call _only_ returns an id+access token, it does not include a refresh token
    # this is the mocked response our refresh API call sends back
    # delete the refresh token, so we can assert our handler still has the original refresh_token
    refresh_tokens_response = json_lib.loads(refreshed_test_tokens.model_dump_json())
    del refresh_tokens_response["refresh_token"]

    branch_json = [{"id": "main", "commit_id": "645127d28f7c1d09b42e3018"}]
    branches_route = respx_mock.get(f"{api_url}/repos/my-org/my-repo/branches").mock(
        side_effect=[httpx.Response(httpx.codes.UNAUTHORIZED), httpx.Response(httpx.codes.OK, json=branch_json)]
    )
    refresh_token_route = respx_mock.post(f"https://{mock_auth_provider_config.domain}/oauth/token").mock(
        return_value=httpx.Response(httpx.codes.OK, json=refresh_tokens_response)
    )

    config = HttpMetastoreConfig(api_url, "my-org")
    db_config = HttpMetastoreDatabaseConfig(config, "my-repo")
    db = HttpMetastoreDatabase(db_config)

    db = HttpMetastoreDatabase(db_config)
    branches = await db.get_branches()
    assert branches[0].id == branch_json[0]["id"]

    assert branches_route.call_count == 2
    assert refresh_token_route.call_count == 1


@pytest.fixture(name="log_output")
def fixture_log_output():
    return LogCapture()


@pytest.fixture(autouse=True)
def fixture_configure_structlog(log_output):
    structlog.configure(processors=[log_output])


def test_handle_response():
    mock_request = httpx.Request("POST", "https://earthmover.io/content/foo", params={"a": "b"}, json={"foo": "bar"})
    mock_response = httpx.Response(
        200, request=mock_request, content=json_lib.dumps({"detail": "Not found"}), headers={"Content-Type": "application/json"}
    )
    handle_response(mock_response)


def test_handle_response_error(log_output):
    mock_request = httpx.Request(
        "POST", "https://earthmover.io/content/foo", params={"a": "b"}, json={"foo": "bar"}, headers={"Authorization": "Bearer foo"}
    )
    mock_response = httpx.Response(
        404,
        request=mock_request,
        content=json_lib.dumps({"detail": "Not found"}),
        headers={"Content-Type": "application/json", "x-request-id": "7eea73c041524f268f804af813f7618f"},
    )
    with pytest.raises(ValueError, match="Error response"):
        handle_response(mock_response)
    entries = log_output.entries[0]
    assert entries["log_level"] == "debug"
    assert entries["url"] == "https://earthmover.io/content/foo?a=b"
    assert entries["request_content"] == b'{"foo": "bar"}'
    assert entries["request_headers"]["authorization"] == "[omitted]"
    assert entries["response_headers"]["content-type"] == "application/json"
    assert entries["response_headers"]["x-request-id"] == "7eea73c041524f268f804af813f7618f"


@pytest.mark.asyncio
@pytest.mark.parametrize("verify_ssl", [True, False])
async def test_config_verify_ssl(respx_mock, verify_ssl):
    import ssl

    mock_url = "https://foo.bar/"
    _route = respx_mock.request("GET", mock_url).mock(side_effect=[httpx.ConnectError, httpx.Response(200)])

    with config.set({"service.ssl.verify": verify_ssl}):
        client = ArraylakeHttpClient(mock_url)

        # This triggers building the client
        _ = await client._request("GET", "")

    verify_mode = ssl.CERT_REQUIRED if verify_ssl else ssl.CERT_NONE
    assert client._get_client()._transport.wrapped_transport._pool._ssl_context.verify_mode == verify_mode


@pytest.mark.asyncio
@pytest.mark.parametrize("cafile", [None, "/path/to/cafile"])
async def test_config_custom_ssl_cert(respx_mock, cafile):
    import ssl

    mock_url = "https://foo.bar/"
    _route = respx_mock.request("GET", mock_url).mock(side_effect=[httpx.ConnectError, httpx.Response(200)])

    with config.set({"service.ssl.cafile": cafile}):
        client = ArraylakeHttpClient(mock_url)

        if not cafile:
            _ = await client._request("GET", "")
            assert client._get_client()._transport.wrapped_transport._pool._ssl_context.verify_mode == ssl.CERT_REQUIRED
        else:
            # This error shwos us the cert was passed through to the ssl context
            # but fails because the cert file does not exist
            with pytest.raises(FileNotFoundError):
                _ = await client._request("GET", "")


def test_separate_loops(respx_mock):
    mock_url = "https://foo.bar/"
    client = ArraylakeHttpClient(mock_url)
    route = respx_mock.get(mock_url).mock(return_value=httpx.Response(httpx.codes.OK))

    async def _request():
        return await client._request("GET", "")

    loop1 = asyncio.new_event_loop()
    loop2 = asyncio.new_event_loop()

    loop1.run_until_complete(_request())
    loop1.close()
    loop2.run_until_complete(_request())
    loop2.close()

    # make sure there is one client cached per event loop
    assert len(client._clients) == 2
    assert loop1 in client._clients
    assert loop2 in client._clients
