from app.services.reddit import search_posts

def test_search_returns_results():
    query = "Coffee"
    response = search_posts(query, sort="new")
    
    assert response.query == query
    assert response.count > 0
    assert len(response.posts) > 0
    for post in response.posts:
        assert post.texto
        assert post.título