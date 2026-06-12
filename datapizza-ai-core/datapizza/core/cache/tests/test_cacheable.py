from datapizza.core.cache import MemoryCache, cacheable
from datapizza.core.clients.models import ClientResponse, TokenUsage
from datapizza.type import TextBlock


class _CachedClient:
    def __init__(self):
        self.cache = MemoryCache()
        self.calls = 0

    def _get_cache_key(self, args):
        return args["input"]

    @cacheable(_get_cache_key)
    def invoke(self, input: str) -> ClientResponse:
        self.calls += 1
        return ClientResponse(
            content=[TextBlock(content="cached response")],
            usage=TokenUsage(
                prompt_tokens=1,
                completion_tokens=2,
                cached_tokens=3,
                thinking_tokens=4,
            ),
        )


def test_cache_hit_returns_response_with_zero_usage():
    client = _CachedClient()

    first = client.invoke("same input")
    second = client.invoke("same input")

    assert client.calls == 1
    assert second.text == first.text
    assert second is not first
    assert first.usage == TokenUsage(
        prompt_tokens=1,
        completion_tokens=2,
        cached_tokens=3,
        thinking_tokens=4,
    )
    assert second.usage == TokenUsage()
