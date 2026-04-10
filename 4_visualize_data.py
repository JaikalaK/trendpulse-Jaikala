import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict


# Script 4: Visualize Data
# This script creates 5 visualization charts from analysis data:
# Category distribution pie chart, engagement bar chart, top stories chart,
# engagement distribution histogram, and score vs comments scatter plot.


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


def plot_category_distribution(stories, output_dir):
    # Create pie chart showing story count for each category
    category_counts = defaultdict(int)
    for story in stories:
        cat = story.get("category", "uncategorized")
        category_counts[cat] += 1
    
    fig, ax = plt.subplots(figsize=(10, 8))
    categories = list(category_counts.keys())
    counts = list(category_counts.values())
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    
    ax.pie(counts, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title('Story Distribution by Category', fontsize=14, weight='bold')
    plt.tight_layout()
    output_path = os.path.join(output_dir, "01_category_distribution.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: 01_category_distribution.png")
    return output_path


def plot_engagement_by_category(stories, output_dir):
    # Create bar chart showing average engagement score for each category
    category_engagement = defaultdict(list)
    for story in stories:
        cat = story.get("category", "uncategorized")
        engagement = story.get("engagement_score", 0)
        category_engagement[cat].append(engagement)
    
    categories = []
    avg_engagements = []
    for cat in sorted(category_engagement.keys()):
        engagements = category_engagement[cat]
        avg = sum(engagements) / len(engagements)
        categories.append(cat.capitalize())
        avg_engagements.append(avg)
    
    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.bar(categories, avg_engagements, color='#45B7D1', edgecolor='#2E86AB', linewidth=2)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.0f}', ha='center', va='bottom', fontsize=11)
    
    ax.set_ylabel('Average Engagement Score', fontsize=12, weight='bold')
    ax.set_title('Average Engagement by Category', fontsize=14, weight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    output_path = os.path.join(output_dir, "02_engagement_by_category.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: 02_engagement_by_category.png")
    return output_path


def plot_top_stories(stories, output_dir, limit=10):
    # Create horizontal bar chart showing top N stories by engagement score
    top = sorted(stories, key=lambda x: x.get("engagement_score", 0), reverse=True)[:limit]
    titles = [s.get("title", "")[:40] + "..." for s in top]
    engagements = [s.get("engagement_score", 0) for s in top]
    categories = [s.get("category", "") for s in top]
    
    category_colors = {
        'technology': '#FF6B6B',
        'worldnews': '#4ECDC4',
        'sports': '#45B7D1',
        'science': '#FFA07A',
        'entertainment': '#98D8C8',
        'uncategorized': '#95A5A6'
    }
    colors = [category_colors.get(cat, '#95A5A6') for cat in categories]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    y_pos = range(len(titles))
    bars = ax.barh(y_pos, engagements, color=colors, edgecolor='black', linewidth=1.5)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2., f' {width:.0f}', ha='left', va='center', fontsize=10)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(titles, fontsize=10)
    ax.set_xlabel('Engagement Score', fontsize=12, weight='bold')
    ax.set_title(f'Top {limit} Stories by Engagement', fontsize=14, weight='bold')
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()
    output_path = os.path.join(output_dir, "03_top_stories.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: 03_top_stories.png")
    return output_path


def plot_engagement_distribution(stories, output_dir):
    # Create histogram showing distribution of engagement scores
    engagements = [s.get("engagement_score", 0) for s in stories]
    
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.hist(engagements, bins=30, color='#45B7D1', edgecolor='#2E86AB', linewidth=1.5, alpha=0.8)
    
    avg_engagement = sum(engagements) / len(engagements)
    max_engagement = max(engagements)
    
    ax.axvline(avg_engagement, color='red', linestyle='--', linewidth=2, label=f'Mean: {avg_engagement:.0f}')
    ax.axvline(max_engagement, color='green', linestyle='--', linewidth=2, label=f'Max: {max_engagement:.0f}')
    
    ax.set_xlabel('Engagement Score', fontsize=12, weight='bold')
    ax.set_ylabel('Number of Stories', fontsize=12, weight='bold')
    ax.set_title('Distribution of Engagement Scores', fontsize=14, weight='bold')
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    output_path = os.path.join(output_dir, "04_engagement_distribution.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: 04_engagement_distribution.png")
    return output_path


def plot_score_vs_comments(stories, output_dir):
    # Create scatter plot showing relationship between story score and comment count
    scores = [s.get("score", 0) for s in stories]
    comments = [s.get("num_comments", 0) for s in stories]
    categories = [s.get("category", "") for s in stories]
    
    category_colors = {
        'technology': '#FF6B6B',
        'worldnews': '#4ECDC4',
        'sports': '#45B7D1',
        'science': '#FFA07A',
        'entertainment': '#98D8C8',
        'uncategorized': '#95A5A6'
    }
    colors = [category_colors.get(cat, '#95A5A6') for cat in categories]
    
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.scatter(scores, comments, c=colors, s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
    
    ax.set_xlabel('Score (Upvotes)', fontsize=12, weight='bold')
    ax.set_ylabel('Number of Comments', fontsize=12, weight='bold')
    ax.set_title('Story Score vs Number of Comments', fontsize=14, weight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    legend_patches = [mpatches.Patch(color=color, label=cat.capitalize()) for cat, color in category_colors.items()]
    ax.legend(handles=legend_patches, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, "05_score_vs_comments.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: 05_score_vs_comments.png")
    return output_path


def visualize_data(data_dir="data"):
    # Main function: Load clean data and create 5 visualization charts
    print("="*50)
    print("STEP 4: Create Visualizations")
    print("="*50)
    
    viz_dir = os.path.join(data_dir, "visualizations")
    if not os.path.exists(viz_dir):
        os.makedirs(viz_dir)
        print(f"Created directory: {viz_dir}")
    
    print()
    stories = load_clean_data(data_dir)
    if not stories:
        return
    
    print("\nGenerating visualizations...")
    
    try:
        plot_category_distribution(stories, viz_dir)
        plot_engagement_by_category(stories, viz_dir)
        plot_top_stories(stories, viz_dir, limit=10)
        plot_engagement_distribution(stories, viz_dir)
        plot_score_vs_comments(stories, viz_dir)
        
        chart_files = list(Path(viz_dir).glob("*.png"))
        
        print(f"\n" + "="*50)
        print(f"Created {len(chart_files)} visualizations")
        print(f"Charts saved in: {viz_dir}")
        print("="*50)
        
    except ImportError:
        print("\nmatplotlib not found. Install it with:")
        print("   pip install matplotlib")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    visualize_data()
