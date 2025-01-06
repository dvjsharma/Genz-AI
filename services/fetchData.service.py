"""
Brief: This file contains the functions to fetch data from Instagram via Instaloader.

Description: This file contains the function `fetch_data` which takes the Instagram profile name as input and fetches the data from the profile. The data is saved in a CSV file with the following columns:
- post_id: The unique identifier of the post.
- post_type: The type of the post (static-image or reels).
- likes: The number of likes on the post.
- comments: The number of comments on the post.
- date_posted: The date when the post was posted.
- vectorize: A string that can be used for vectorization.
- content: The content of the post.
- metadata: The metadata of the post.
- username: The username of the profile.

Author: Team Genz-AI

"""

import instaloader
import csv
import os
from tqdm import tqdm

def fetch_data(profile_name: str, output_dir: str = 'data') -> None:
    # Initialize
    L = instaloader.Instaloader()

    # Load the profile
    profile = instaloader.Profile.from_username(L.context, profile_name)

    # Get the total count
    total_posts = profile.mediacount

    # Create the output dir if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create the filename
    filename = f"{output_dir}/{profile_name}.csv"

    # Open the CSV file
    with open(filename, "w", newline='', encoding='utf-8') as csv_file:
        fieldnames = ['post_id', 'post_type', 'likes', 'comments', 'date_posted', 'vectorize', 'content', 'metadata', 'username']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for post in tqdm(profile.get_posts(), total=total_posts, desc="Processing posts", unit="post"):
            post_type = "reels" if post.is_video else "static-image"
            post_details = {
                'post_id': post.mediaid,
                'post_type': post_type,
                'likes': post.likes,
                'comments': post.comments,
                'date_posted': post.date.isoformat(),
                'vectorize': f"A post with username:\"{profile_name}\", post_id: \"{post.mediaid}\", post_type: \"{post_type}\", likes: {post.likes}, comments: {post.comments}, date_posted: \"{post.date.isoformat()}\".",
                'content': f"A post with username:\"{profile_name}\", post_id: \"{post.mediaid}\", post_type: \"{post_type}\", likes: {post.likes}, comments: {post.comments}, date_posted: \"{post.date.isoformat()}\".",
                'metadata': str({"post_type": post_type, "username": profile_name}),
                'username': profile_name,
            }
            writer.writerow(post_details)

    print(f"Post details have been saved to '{filename}'.")