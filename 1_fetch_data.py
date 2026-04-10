import requests
import json
import time
import os
from datetime import datetime
import urllib3

# Disable SSL warnings
urllib3.disable_warnings()

# API settings
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Keywords to categorize stories
CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}


def fetch_top_story_ids(limit=500):
    # Get list of top story IDs from API
    try:
        print(f"Fetching top {limit} story IDs...")
        url = f"{BASE_URL}/topstories.json"
        response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        response.raise_for_status()
        story_ids = response.json()[:limit]
        print(f"Got {len(story_ids)} story IDs")
        return story_ids
    except requests.RequestException as e:
        print(f"Error: {e}")
        return []


def fetch_story_details(story_id):
    # Get full details for one story by ID
    try:
        url = f"{BASE_URL}/item/{story_id}.json"
        response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching story {story_id}")
        return None


def categorize_story(title):
    # Make title lowercase for comparison
    title_lower = title.lower()
    
    # Check each category and its keywords
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            # If keyword found in title, return that category
            if keyword.lower() in title_lower:
                return category
    
    # If no keyword matches, return uncategorized
    return "uncategorized"


def extract_story_fields(story):
    # Get important fields from story data
    if not story:
        return None
    return {
        "post_id": story.get("id"),
        "title": story.get("title", ""),
        "category": categorize_story(story.get("title", "")),
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by", "unknown"),
        "url": story.get("url", ""),
        "collected_at": datetime.now().isoformat()
    }


def fetch_and_save_stories(output_dir="data", stories_per_category=25):
    # Create output folder if it does not exist.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Fetch top story IDs from Hacker News.
    story_ids = fetch_top_story_ids(500)
    if not story_ids:
        print("Failed to fetch story IDs")
        return
    
    # Store collected stories by category and in one final list.
    stories_by_category = {cat: [] for cat in CATEGORIES.keys()}
    stories_by_category["uncategorized"] = []
    all_stories = []
    
    print(f"\nFetching story details...")
    for idx, story_id in enumerate(story_ids, 1):
        # Get one story from the API.
        story = fetch_story_details(story_id)
        if not story:
            continue
        
        # Keep only fields needed for the project.
        story_data = extract_story_fields(story)
        if not story_data:
            continue
        
        category = story_data["category"]
        
        # Keep a fixed number of stories per category.
        if len(stories_by_category[category]) < stories_per_category:
            stories_by_category[category].append(story_data)
            all_stories.append(story_data)
            print(f"  [{idx}] {story_data['title'][:50]}... -> {category}")
        
        # Stop when all main categories reached their target.
        total_collected = sum(len(stories_by_category[cat]) for cat in stories_by_category)
        if total_collected >= stories_per_category * len(CATEGORIES):
            break
        
        # Small pause to avoid hitting API too quickly.
        if idx % 5 == 0:
            time.sleep(2)
    
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = os.path.join(output_dir, f"trends_{date_str}.json")
    
    try:
        # Save collected stories to JSON file.
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_stories, f, indent=2, ensure_ascii=False)
        
        print(f"Collected {len(all_stories)} stories. Saved to data/trends_{date_str}.json")
        print("\nBreakdown:")
        for category in CATEGORIES.keys():
            count = len(stories_by_category[category])
            if count > 0:
                print(f"  {category}: {count}")
        if stories_by_category["uncategorized"]:
            print(f"  uncategorized: {len(stories_by_category['uncategorized'])}")
        
    except IOError as e:
        print(f"Error saving file: {e}")


if __name__ == "__main__":
    fetch_and_save_stories(stories_per_category=25)
