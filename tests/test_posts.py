from httpx import AsyncClient


async def test_post_list(ac: AsyncClient):
    result = await ac.get('/posts/')
    assert result.status_code == 200
    assert result.json() == []
