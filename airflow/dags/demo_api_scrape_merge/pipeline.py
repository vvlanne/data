"""
Variant 1 — API (posts) → SQLite → filtered CSV

DAG id: v1_posts_pipeline
Tasks:
  1) fetch_posts        - load posts from API into SQLite
  2) export_long_posts  - filter posts and export to CSV
"""

from pathlib import Path
import sqlite3

import requests
import pandas as pd


# Base paths for local files (DB + CSV)
FILE_DIR = Path(__file__).resolve().parent
DB_PATH = FILE_DIR / "v1_demo.db"
CSV_PATH = FILE_DIR / "long_posts.csv"


def fetch_posts():
    """
    Task 1: Fetch posts from JSONPlaceholder API and save to SQLite.

    API: https://jsonplaceholder.typicode.com/posts
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    print(f"Requesting data from {url} ...")

    # Fetch data
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Convert to DataFrame and keep needed columns
    df = pd.DataFrame(data)[["id", "userId", "title", "body"]]
    df = df.rename(columns={"userId": "user_id"})

    # Save to SQLite
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("posts", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Saved {len(df)} posts to {DB_PATH} table 'posts'.")


def export_long_posts():
    """
    Task 2: Read posts from SQLite, filter by title length, export to CSV.
    """
    # Read from SQLite
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM posts", conn)
    conn.close()

    print(f"Loaded {len(df)} rows from posts table.")

    # Filter by title length > 30 characters
    filtered = df[df["title"].str.len() > 30]

    # Save to CSV
    filtered.to_csv(CSV_PATH, index=False)

    print(
        f"Exported {len(filtered)} long-title posts to {CSV_PATH} "
        f"(from {len(df)} total)."
    )
