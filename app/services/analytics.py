from app.services.search import search_posts
from collections import Counter

def calculate_distribution(posts):

    sentiments = []

    for post in posts.posts:
        for comment in post.comments:
            sentiments.append(comment["sentiment"])

    count = Counter(sentiments)
    total = len(sentiments)
    percentages = {s: round((c / total) * 100) for s, c in count.items()}

    return percentages