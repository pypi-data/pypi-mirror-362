import pytest
from arato_proxy.custom_callbacks import AratoLogHandler


@pytest.fixture
def handler():
    return AratoLogHandler()


def test_arato_log_handler_init(handler):
    assert isinstance(handler, AratoLogHandler)


def test_postLog_signature(handler):
    # Check that postLog accepts all required arguments and returns a requests.Response
    import requests

    result = handler.postLog(
        api_url="http://example.com",
        api_token="dummy-token",
        messages=[{"role": "user", "content": "Hello"}],
        response="Hi!",
        event_id="test-id",
        model="test-model",
        variables={"var1": "value1"},
        usage={"completion_tokens": 1, "prompt_tokens": 2, "total_tokens": 3},
        performance={"ttft": 100, "ttlt": 200},
        tool_calls=[],
        arato_thread_id="thread-1",
        prompt_id="prompt-1",
        prompt_version="1.0",
        tags={"tag1": "value1"},
    )
    assert isinstance(result, requests.Response)


def test_async_log_success_event_runs(handler, monkeypatch):
    import asyncio
    import datetime
    import requests

    class DummyResponse:
        def __init__(self):
            self.choices = [
                type("obj", (object,), {"message": type("obj", (object,), {"content": "Hello", "tool_calls": None})})
            ]
            self.usage = type("obj", (object,), {
                "completion_tokens": 1,
                "prompt_tokens": 2,
                "total_tokens": 3,
                "completion_tokens_details": None,
                "prompt_tokens_details": None,
            })

    kwargs = {
        "messages": [{"role": "user", "content": "Hello"}],
        "litellm_call_id": "test-id",
        "model": "test-model",
        "variables": {"var1": "value1"},
        "tags": {"tag1": "value1"},
        "completion_start_time": datetime.datetime.now(),
        "litellm_session_id": "thread-1",
        "prompt_id": "prompt-1",
        "prompt_version": "1.0",
    }
    response_obj = DummyResponse()
    start_time = datetime.datetime.now()
    end_time = start_time

    # Patch postLog to avoid real HTTP requests
    monkeypatch.setattr(handler, "postLog", lambda *args, **kwargs: requests.Response())

    # Should not raise
    asyncio.run(handler.async_log_success_event(kwargs, response_obj, start_time, end_time))
