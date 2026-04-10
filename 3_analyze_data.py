import os
import numpy as np
import pandas as pd


# Script 3: Analysis
# This script loads data/trends_clean.csv, runs analysis using Pandas + NumPy,
# adds new columns, and saves data/trends_analysed.csv.


def analyze_trends(data_dir="data"):
    # Main flow for  analysis.
    input_file = os.path.join(data_dir, "trends_clean.csv")
    if not os.path.exists(input_file):
        print(f"Missing file: {input_file}")
        return

    df = pd.read_csv(input_file)
    print(f"Loaded data: {df.shape}")

    print("\nFirst 5 rows:")
    print(df.head(5))

    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()
    print(f"\nAverage score   : {avg_score:.2f}")
    print(f"Average comments: {avg_comments:.2f}")

    # NumPy stats required by the rubric.
    scores = df["score"].to_numpy()
    comments = df["num_comments"].to_numpy()
    print("\n--- NumPy Stats ---")
    print(f"Mean score   : {np.mean(scores):.2f}")
    print(f"Median score : {np.median(scores):.2f}")
    print(f"Std deviation: {np.std(scores):.2f}")
    print(f"Max score    : {np.max(scores)}")
    print(f"Min score    : {np.min(scores)}")

    category_counts = df["category"].value_counts()
    top_category = category_counts.index[0]
    top_category_count = category_counts.iloc[0]
    print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

    most_commented_idx = int(np.argmax(comments))
    most_commented_title = df.iloc[most_commented_idx]["title"]
    most_commented_count = int(df.iloc[most_commented_idx]["num_comments"])
    print(
        f"Most commented story: \"{most_commented_title}\" - {most_commented_count} comments"
    )

    # Add required columns.
    df["engagement"] = df["num_comments"] / (df["score"] + 1)
    df["is_popular"] = df["score"] > avg_score

    output_file = os.path.join(data_dir, "trends_analysed.csv")
    df.to_csv(output_file, index=False)
    print(f"\nSaved to {output_file}")

if __name__ == "__main__":
    analyze_trends()
