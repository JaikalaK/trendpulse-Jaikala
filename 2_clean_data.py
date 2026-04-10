import os
from pathlib import Path
import pandas as pd


# Script 2: Clean Data
# This script loads the latest raw JSON from Task 1, cleans it using Pandas,
# and saves the cleaned result as data/trends_clean.csv.


def load_latest_json_file(data_dir="data"):
    # Find only raw trends_YYYYMMDD.json files (exclude clean/analysis files).
    json_files = sorted(
        f for f in Path(data_dir).glob("trends_*.json")
        if not f.name.startswith("trends_clean_")
    )
    if not json_files:
        print(f"No JSON files found in {data_dir}")
        return None
    return json_files[-1]


def clean_and_save_data(data_dir="data"):
    # Main flow for clean data .
    if not os.path.exists(data_dir):
        os.makedirs(data_dir
 
    input_file = load_latest_json_file(data_dir)
    if not input_file:
        return
 
    # Load raw JSON into DataFrame.
    try:
        df = pd.read_json(input_file)
    except ValueError as e:
        print(f"Error: {e}")
        return

    print(f"Loaded {len(df)} stories from {input_file}")

    # Remove duplicate post_id rows.
    df = df.drop_duplicates(subset=["post_id"])
    print(f"After removing duplicates: {len(df)}")

    # Drop rows with missing post_id, title, or score.
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # Convert numeric columns to integers.
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")
    df = df.dropna(subset=["score", "num_comments"])
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)

    # Remove low-quality rows where score < 5.
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # Clean whitespace in title.
    df["title"] = df["title"].astype(str).str.strip()

    output_file = os.path.join(data_dir, "trends_clean.csv")
    df.to_csv(output_file, index=False)

    print(f"\nSaved {len(df)} rows to {output_file}")
    print("\nStories per category:")
    print(df["category"].value_counts())

if __name__ == "__main__":
    clean_and_save_data()
