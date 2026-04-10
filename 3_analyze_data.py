import json
import os
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict


# Script 3: Analyze Data
# This script analyzes cleaned data to find insights: top stories, category stats,
# influential authors, and trending keywords. Outputs analysis JSON file.


def load_clean_data(data_dir="data"):
    # Load the most recent cleaned data file
    json_files = sorted(Path(data_dir).glob("trends_clean_*.json"))
    if not json_files:
        print(f"No cleaned JSON files found in {data_dir}")
        return []
    
    latest_file = json_files[-1]
    print(f"Loading: {latest_file}")
    
    try:
        with open(latest_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Loaded {len(data)} stories")
        return data
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error: {e}")
        return []


def get_top_stories(stories, limit=10):
    # Sort stories by engagement score, return top N
    return sorted(
        stories,
        key=lambda x: x.get("engagement_score", 0),
        reverse=True
    )[:limit]


def analyze_categories(stories):
    # Calculate stats for each category: count, avg score, avg engagement, top story
    category_stats = defaultdict(lambda: {
        "count": 0,
        "total_score": 0,
        "total_comments": 0,
        "total_engagement": 0,
        "avg_score": 0,
        "avg_comments": 0,
        "avg_engagement": 0,
        "top_story_title": "",
        "top_story_score": 0
    })
    
    for story in stories:
        cat = story.get("category", "uncategorized")
        score = story.get("score", 0)
        comments = story.get("num_comments", 0)
        engagement = story.get("engagement_score", 0)
        
        category_stats[cat]["count"] += 1
        category_stats[cat]["total_score"] += score
        category_stats[cat]["total_comments"] += comments
        category_stats[cat]["total_engagement"] += engagement
        
        if engagement > category_stats[cat]["top_story_score"]:
            category_stats[cat]["top_story_score"] = engagement
            category_stats[cat]["top_story_title"] = story.get("title", "")
    
    for cat in category_stats:
        count = category_stats[cat]["count"]
        if count > 0:
            category_stats[cat]["avg_score"] = round(
                category_stats[cat]["total_score"] / count, 2
            )
            category_stats[cat]["avg_comments"] = round(
                category_stats[cat]["total_comments"] / count, 2
            )
            category_stats[cat]["avg_engagement"] = round(
                category_stats[cat]["total_engagement"] / count, 2
            )
    
    return dict(category_stats)


def get_top_authors(stories, limit=10):
    # Find authors with highest average engagement, return top N
    author_stats = defaultdict(lambda: {
        "count": 0,
        "total_engagement": 0,
        "avg_engagement": 0
    })
    
    for story in stories:
        author = story.get("author", "unknown")
        engagement = story.get("engagement_score", 0)
        
        author_stats[author]["count"] += 1
        author_stats[author]["total_engagement"] += engagement
    
    for author in author_stats:
        count = author_stats[author]["count"]
        author_stats[author]["avg_engagement"] = round(
            author_stats[author]["total_engagement"] / count, 2
        )
    
    sorted_authors = sorted(
        [{"author": a, **stats} for a, stats in author_stats.items()],
        key=lambda x: (x["avg_engagement"], x["count"]),
        reverse=True
    )
    return sorted_authors[:limit]


def get_trending_keywords(stories, limit=20):
    # Extract and count keywords from story titles (ignore common stop words)
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "was", "are", "be", "been",
        "have", "has", "do", "does", "did", "will", "would", "could", "should",
        "may", "might", "must", "can", "it", "this", "that", "these", "those"
    }
    
    words = Counter()
    for story in stories:
        title = story.get("title", "").lower()
        title_words = [
            w.strip('.,!?;:"\'-') for w in title.split()
            if w.strip('.,!?;:"\'-').lower() not in stop_words
            and len(w.strip('.,!?;:"\'-')) > 3
        ]
        words.update(title_words)
    
    return [{"keyword": word, "frequency": count} for word, count in words.most_common(limit)]


def analyze_trends(data_dir="data"):
    # Main function: Load clean data and generate analysis results
    print("="*50)
    print("STEP 3: Analyze Data")
    print("="*50)
    
    stories = load_clean_data(data_dir)
    if not stories:
        return
    
    print("\nAnalyzing top stories...")
    top_stories = get_top_stories(stories, 10)
    
    print("Analyzing categories...")
    category_analysis = analyze_categories(stories)
    
    print("Finding top authors...")
    top_authors = get_top_authors(stories, 10)
    
    print("Finding trending keywords...")
    trending_keywords = get_trending_keywords(stories, 20)
    
    results = {
        "analysis_date": datetime.now().isoformat(),
        "total_stories_analyzed": len(stories),
        "top_stories": [
            {
                "rank": i + 1,
                "title": s.get("title", ""),
                "category": s.get("category", ""),
                "engagement_score": s.get("engagement_score", 0),
                "score": s.get("score", 0),
                "num_comments": s.get("num_comments", 0),
                "author": s.get("author", "")
            }
            for i, s in enumerate(top_stories)
        ],
        "category_analysis": {
            cat: {
                "count": stats["count"],
                "avg_engagement": stats["avg_engagement"],
                "avg_score": stats["avg_score"],
                "avg_comments": stats["avg_comments"],
                "top_story": {
                    "title": stats["top_story_title"],
                    "engagement": stats["top_story_score"]
                }
            }
            for cat, stats in category_analysis.items()
        },
        "top_authors": [
            {
                "rank": i + 1,
                "author": a["author"],
                "story_count": a["count"],
                "avg_engagement": a["avg_engagement"]
            }
            for i, a in enumerate(top_authors)
        ],
        "trending_keywords": trending_keywords
    }
    
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = os.path.join(data_dir, f"analysis_{date_str}.json")
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n" + "="*50)
        print(f"Saved to {output_file}")
        
        print(f"\nTop 5 Stories:")
        for story in top_stories[:5]:
            print(f"  {story['engagement_score']:.0f} - {story['title'][:50]}")
        
        print(f"\nTop Categories:")
        sorted_cats = sorted(category_analysis.items(), key=lambda x: x[1]["avg_engagement"], reverse=True)
        for cat, stats in sorted_cats[:5]:
            print(f"  {cat}: {stats['count']} stories (avg: {stats['avg_engagement']})")
        
        print(f"\nTop Authors:")
        for author in top_authors[:5]:
            print(f"  {author['author']}: {author['count']} stories (avg: {author['avg_engagement']})")
        
        print("="*50)
        
    except IOError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_trends()
