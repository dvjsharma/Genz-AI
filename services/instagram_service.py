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
import io
import logging
from tqdm import tqdm
from errors.invalid_input_error import InvalidInputError
from errors.runtime_error import RuntimeError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data(profile_name: str) -> str:
    """
    Fetch data for the given profile and return it as an in-memory CSV.

    :param profile_name: The Instagram profile name for which the data is to be fetched.
    :return: The data fetched from the profile in CSV format.
    """
    if not profile_name.strip():
        raise InvalidInputError("Profile name is empty. Please provide a valid profile name.")
    
    try:
        logging.info(f"Fetching data for profile: {profile_name}")
        
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, profile_name)
        total_posts = profile.mediacount

        output = io.StringIO()
        fieldnames = ['post_id', 'post_type', 'likes', 'comments', 'date_posted', 'vectorize', 'content', 'metadata', 'username']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for post in tqdm(profile.get_posts(), total=total_posts, desc="Processing posts", unit="post"):
            post_type = "reels" if post.is_video else "static_image"
            post_details = {
                'username': profile_name,
                'post_id': post.mediaid,
                'post_type': post_type,
                'likes': post.likes,
                'comments': post.comments,
                'date_posted': post.date.isoformat(),
                'content': f"A post with username:\"{profile_name}\", post_id: \"{post.mediaid}\", post_type: \"{post_type}\", likes: {post.likes}, comments: {post.comments}, date_posted: \"{post.date.isoformat()}\".",
                'vectorize': f"A post with username:\"{profile_name}\", post_id: \"{post.mediaid}\", post_type: \"{post_type}\", likes: {post.likes}, comments: {post.comments}, date_posted: \"{post.date.isoformat()}\".",
                'metadata': str({"post_type": post_type, "username": profile_name}),
            }
            writer.writerow(post_details)

        csv_data = output.getvalue()
        output.close()
        logging.info(f"Data fetching complete for profile: {profile_name}")
        return csv_data

    except instaloader.exceptions.ConnectionException:
        raise InvalidInputError(f"The profile '{profile_name}' does not exist.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")
