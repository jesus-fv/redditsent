from collections import Counter, defaultdict

SENT_CATS = ["positive", "negative", "neutral", "unknown"]
 
def summarize_sentiments(comments):
    
    counts = Counter()
    scores = []
    
    for comment in comments:
        cat = comment.get("sentiment_label")
        counts[cat] += 1
        sc = comment.get("sentiment_score")
        if sc is not None:
            scores.append(sc)
    
    total = sum(counts.values())
    percentages = {cat: (counts.get(cat, 0) / total * 100) if total > 0 else 0.0 for cat in SENT_CATS}
    mean_score = round(sum(scores) / len(scores), 4) if scores else None
    dominant = max(SENT_CATS, key=lambda k: counts.get(k, 0)) if total > 0 else "unknown"

    return {
        "counts": {k: int(counts.get(k, 0)) for k in SENT_CATS},
        "percentages": {k: round(percentages[k], 2) for k in SENT_CATS},
        "mean_sentiment_score": mean_score,
        "dominant": dominant
}
    
def analyze_post(post):
    
    comments = post.get("comments") or []
    sentiments_summary = summarize_sentiments(comments)
    
    return {
        "id": post.get("id"),
        "title": post.get("title"),
        "author": post.get("author"),
        "url": post.get("url"),
        "subreddit": post.get("subreddit"),
        "karma": int(post.get("karma") or post.get("score") or 0),
        "num_comments": int(post.get("num_comments") or len(comments)),
        "media_url": post.get("media_url"),
        "sentiments": sentiments_summary,
        "comments": comments
        
    }
    
def compute_metrics(posts, query: str = "", sort: str = ""):

    all_comments = []
    processed_posts = []
    subreddit_map = defaultdict(list)

    for post in posts:
        pm = analyze_post(post)
        processed_posts.append(pm)
        subreddit_map[pm["subreddit"]].append(pm)
        for c in post.get("comments", []) or []:
            all_comments.append(c)

    global_counts = Counter()
    for p in processed_posts:
        global_counts.update(p["sentiments"]["counts"])
    total_analyzed_comments = sum(global_counts.values()) or 0
    global_percentages = {k: round((global_counts.get(k,0) / total_analyzed_comments * 100) if total_analyzed_comments else 0.0, 2) for k in SENT_CATS}

    scores = [c.get("sentiment_score") for c in all_comments if c.get("sentiment_score") is not None]
    mean_global_score = round(sum(scores)/len(scores),4) if scores else None
    dominant_global = max(SENT_CATS, key=lambda k: global_counts.get(k, 0)) if total_analyzed_comments else "unknown"

    subreddits_summary = []
    for sub, posts_list in subreddit_map.items():
        sub_counter = Counter()
        for p in posts_list:
            sub_counter.update(p["sentiments"]["counts"])
        sub_total_analyzed = sum(sub_counter.values()) or 0
        sub_percentages = {k: round((sub_counter.get(k,0) / sub_total_analyzed * 100) if sub_total_analyzed else 0.0, 2) for k in SENT_CATS}

        mean_scores = [p["sentiments"]["mean_sentiment_score"] for p in posts_list if p["sentiments"]["mean_sentiment_score"] is not None]
        mean_sub_score = round(sum(mean_scores)/len(mean_scores),4) if mean_scores else None
        dominant_sub = max(SENT_CATS, key=lambda k: sub_counter.get(k, 0)) if sub_total_analyzed else "unknown"

        subreddits_summary.append({
            "subreddit": sub,
            "total_posts": len(posts_list),
            "total_comments": sub_total_analyzed,
            "counts": {k: int(sub_counter.get(k,0)) for k in SENT_CATS},
            "percentages": sub_percentages,
            "mean_sentiment_score": mean_sub_score,
            "dominant": dominant_sub,
        })

    result = {
        "query": query,
        "count": len(posts),
        "sort": sort,
        "global": {
            "total_posts": len(posts),
            "total_comments": total_analyzed_comments,
            "counts": {k: int(global_counts.get(k,0)) for k in SENT_CATS},
            "percentages": global_percentages,
            "mean_sentiment_score": mean_global_score,
            "dominant": dominant_global
        },
        "subreddits": subreddits_summary,
        "posts": processed_posts
    }
    
    return result