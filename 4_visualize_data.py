import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# Script 4: Visualizations
# This script reads data/trends_analysed.csv and builds 3 required charts,
# then combines them into a single dashboard image.


def shorten_title(title, max_len=50):
    # Keep titles readable in charts.
    if len(title) <= max_len:
        return title
    return title[:max_len] + "..."


def plot_top_stories(df, output_dir):
    # Chart 1: Top 10 stories by score.
    top = df.nlargest(10, "score").copy()
    top["short_title"] = top["title"].astype(str).apply(shorten_title)

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.barh(top["short_title"], top["score"], color="#2f7f6f")
    ax.set_title("Top 10 Stories by Score")
    ax.set_xlabel("Score")
    ax.set_ylabel("Story Title")
    ax.invert_yaxis()
    plt.tight_layout()

    output_path = os.path.join(output_dir, "chart1_top_stories.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/chart1_top_stories.png")
    return output_path


def plot_categories(df, output_dir):
    # Chart 2: Stories count per category.
    category_counts = df["category"].value_counts()
    colors = ["#f39c12", "#3498db", "#27ae60", "#9b59b6", "#e74c3c", "#7f8c8d"]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(category_counts.index, category_counts.values, color=colors[: len(category_counts)])
    ax.set_title("Stories per Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Number of Stories")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    output_path = os.path.join(output_dir, "chart2_categories.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/chart2_categories.png")
    return output_path


def plot_scatter(df, output_dir):
    # Chart 3: Score vs comments, colored by is_popular.
    fig, ax = plt.subplots(figsize=(8, 6))
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    ax.scatter(not_popular["score"], not_popular["num_comments"], c="#3498db", alpha=0.6, label="Not Popular")
    ax.scatter(popular["score"], popular["num_comments"], c="#e74c3c", alpha=0.7, label="Popular")
    ax.set_title("Score vs Comments")
    ax.set_xlabel("Score")
    ax.set_ylabel("Number of Comments")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()

    output_path = os.path.join(output_dir, "chart3_scatter.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/chart3_scatter.png")
    return output_path


def plot_dashboard(df, output_dir):
    # Bonus: combine all 3 charts into one dashboard figure.
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))

    top = df.nlargest(10, "score").copy()
    top["short_title"] = top["title"].astype(str).apply(shorten_title)
    axes[0].barh(top["short_title"], top["score"], color="#2f7f6f")
    axes[0].set_title("Top 10 Stories by Score")
    axes[0].set_xlabel("Score")
    axes[0].invert_yaxis()

    category_counts = df["category"].value_counts()
    colors = ["#f39c12", "#3498db", "#27ae60", "#9b59b6", "#e74c3c", "#7f8c8d"]
    axes[1].bar(category_counts.index, category_counts.values, color=colors[: len(category_counts)])
    axes[1].set_title("Stories per Category")
    axes[1].set_xlabel("Category")
    axes[1].set_ylabel("Count")
    axes[1].tick_params(axis="x", rotation=30)

    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]
    axes[2].scatter(not_popular["score"], not_popular["num_comments"], c="#3498db", alpha=0.6, label="Not Popular")
    axes[2].scatter(popular["score"], popular["num_comments"], c="#e74c3c", alpha=0.7, label="Popular")
    axes[2].set_title("Score vs Comments")
    axes[2].set_xlabel("Score")
    axes[2].set_ylabel("Comments")
    axes[2].legend()

    fig.suptitle("TrendPulse Dashboard", fontsize=16, fontweight="bold")
    plt.tight_layout()
    output_path = os.path.join(output_dir, "dashboard.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/dashboard.png")
    return output_path


def visualize_data(data_dir="data"):
    # Main flow for visualization .
    input_file = os.path.join(data_dir, "trends_analysed.csv")
    if not os.path.exists(input_file):
        print(f"Missing file: {input_file}")
        return

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_file)
    print(f"Loaded: {input_file} ({df.shape[0]} rows)")

    plot_top_stories(df, output_dir)
    plot_categories(df, output_dir)
    plot_scatter(df, output_dir)
    plot_dashboard(df, output_dir)

    generated = list(Path(output_dir).glob("*.png"))
    print(f"Created {len(generated)} chart files in {output_dir}")


if __name__ == "__main__":
    visualize_data()
