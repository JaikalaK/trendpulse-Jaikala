import json
import os
from datetime import datetime
from pathlib import Path


# Script 2: Clean Data
# This script loads raw story data, validates it, removes duplicates, 
# and calculates engagement scores. Outputs a cleaned JSON file.


def load_raw_data(data_dir="data"):
    # Load the most recent raw story data file from the data directory
    json_files = sorted(Path(data_dir).glob("trends_*.json"))
    if not json_files:
        print(f"No JSON files found in {data_dir}")
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


def validate_story(story):
    # Check that story has all required fields with values
    required_fields = ["post_id", "title", "category", "score", "num_comments", "author"]
    for field in required_fields:
        if field not in story or story[field] is None:
            return False
    return True


def calculate_engagement_score(story):
    # Calculate engagement score: score + (comments * 2)
    score = story.get("score", 0)
    comments = story.get("num_comments", 0)
    engagement = score + (comments * 2)
    return round(engagement, 2)


def clean_story(story):
    # Standardize story data: convert types, trim strings, ensure min values
    return {
        "post_id": int(story.get("post_id", 0)),
        "title": str(story.get("title", "")).strip(),
        "category": str(story.get("category", "uncategorized")).lower(),
        "score": max(0, int(story.get("score", 0))),
        "num_comments": max(0, int(story.get("num_comments", 0))),
        "author": str(story.get("author", "unknown")).strip(),
        "url": str(story.get("url", "")).strip(),
        "engagement_score": None,
        "collected_at": str(story.get("collected_at", datetime.now().isoformat()))
    }


def remove_duplicates(stories):
    # Remove stories with duplicate post IDs, keep first occurrence
    seen_ids = set()
    unique_stories = []
    duplicates_removed = 0
    
    for story in stories:
        post_id = story.get("post_id")
        if post_id not in seen_ids:
            seen_ids.add(post_id)
            unique_stories.append(story)
        else:
            duplicates_removed += 1
    
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicates")
    return unique_stories


def clean_and_save_data(data_dir="data"):
    # Main function: Load raw data, clean it, and save results
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    print("="*50)
    print("STEP 2: Clean Data")
    print("="*50)
    
    raw_stories = load_raw_data(data_dir)
    if not raw_stories:
        return
    
    print(f"\nValidating {len(raw_stories)} stories...")
    valid_stories = [s for s in raw_stories if validate_story(s)]
    print(f"{len(valid_stories)} stories are valid")
    
    print("Cleaning data...")
    cleaned_stories = [clean_story(s) for s in valid_stories]
    
    print("Removing duplicates...")
    unique_stories = remove_duplicates(cleaned_stories)
    
    print("Calculating engagement scores...")
    for story in unique_stories:
        story["engagement_score"] = calculate_engagement_score(story)
    
    unique_stories.sort(key=lambda x: x["engagement_score"], reverse=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = os.path.join(data_dir, f"trends_clean_{date_str}.json")
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(unique_stories, f, indent=2, ensure_ascii=False)
        
        print(f"\n" + "="*50)
        print(f"Saved to {output_file}")
        print(f"Total clean stories: {len(unique_stories)}")
        print("="*50)
        
    except IOError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    clean_and_save_data()
