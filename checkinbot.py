# INF601 - Advanced Programming in Python
# Rachel White
# Scheduled Check-In Bot

import os
import sys
import json
import mimetypes
import requests

#load environment variables
API_BASE_URL = os.getenv("PRACTICE_HUB_URL", "").rstrip("/")
API_TOKEN = os.getenv("PRACTICE_API_TOKEN")
INTRUCTOR_ID = os.getenv("INSTRUCTOR_ID")

#ensure required configuration
if not API_BASE_URL or not API_TOKEN or not INSTRUCTOR_ID:
    print("Error: Missing required environment variables.", file=sys.stderr)
    sys.exit(1)

#initialize standard requests session with authentication headers
session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
})

#define output directories
ARTIFACT_DIR = "artifact"
FILES_DIR = os.path.join(ARTIFACT_DIR, "files")
os.makedirs(FILES_DIR, exist_ok=True)

#get my user profile to identify my comments
def get_my_profile():
    url = f"{API_BASE_URL}/api/v1/users/me"
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching profile: {e}", file=sys.stderr)
        sys.exit(1)

#download attached file and save into artifact/files directory
def download_attachment(file_info):
    file_id = file_info.get("id")
    filename = file_info.get("filename", f"file_{file_id}")
    download_url = f"{API_BASE_URL}/api/v1/attachments/{file_id}/download"

    local_path = os.path.join(FILES_DIR, filename)
    print(f"Downloading attachment" {filename} ...")

    try: 
        with session.get(download_url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded: {filename}")
except requests.RequestException as e:
    print(f"Failed to download attachment {filename}: {e}", file=sys.stderr)

#paginate through all posts and return only those created by the instructor
def collent_instructor_posts():
    posts_url = f"{API_BASE_URL}/api/v1/posts"
    instructor_posts = []
    page = 1

    print(f"Starting collection for Instructor ID: {INSTRUCTOR_ID}")

    while True:
        try:
            response = session.get(posts_url, params={"page": page})
            response.raise_for_status()
            data = response.json()

            posts = data.get("posts", [])
            if not posts:
                break

            for post in posts:
                #filter posts belonging to instructor
                if str(post.get("author_id")) == str(INSTRUCTOR_ID):
                    instructor_posts.append(post)

                    #process and download attachments
                    attachments = post.get("attachments", [])
                    for attachment in attachments:
                        download_attachment(attachment)

            #check pagination metadata to see if another page exists
            meta = dat

  