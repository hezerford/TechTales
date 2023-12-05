import pytest
from httpx import AsyncClient
from src.main import app
from src.database import blog_collection

@pytest.fixture
async def test_app(request):
    async with AsyncClient(app=app, base_url="http://127.0.0.1") as client:
        yield client

@pytest.fixture
async def cleanup_data(request):
    yield
    await blog_collection.delete_many({})

async def test_create_article(test_app, cleanup_data):
    # Тест создания статьи
    response = await test_app.post(
        "/articles/",
        json={
            "title": "Test Article",
            "description": "Test Description",
            "content": "Test Content",
            "publication_date": "2023-12-05T12:00:00",
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Article"
    assert response.json()["description"] == "Test Description"
    assert response.json()["content"] == "Test Content"