from httpx import AsyncClient


async def test_signup(ac: AsyncClient):
    response = await ac.post(
        url='/auth/register',
        json={
            "username": "test1",
            "email": "user@example.com",
            "password": "string"
        }
    )
    assert response.status_code == 201


async def test_login(ac: AsyncClient):
    await ac.post(
        url='/auth/jwt/login',
        data={
            'username': 'test1',  # email or username
            'password': 'string'
        }
    )


# async def test_get_user(ac: AsyncClient):
#     response = await ac.get(
#         url='/account/user/{username}',
#         params={'username': 'test1'}
#     )
#     bad_response = await ac.get(
#         url='/account/user/{username}',
#         params='test'
#     )
#     assert response.status_code == 200
#     assert response.json() == {"username": "test1"}
#     assert bad_response.status_code == 404
