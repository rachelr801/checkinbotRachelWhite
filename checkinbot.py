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
def collect_instructor_posts():
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
            meta = data.get("meta", {})
            if page >= meta.get("total_pages", page):
                break
            page += 1

        except requests.RequestException as e:
            print(f"Error retrieving posts page {page}: {e}", file=sys.strderr)
            break

    return instructor_posts

#identify checin-in posts, check for replies, handle responses
def process_check_ins(posts, bot_user_id):
    bot_user_id_str = str(bot_user_id)

    for post in posts:
        title = post.get("title", "")
        post_id = post.get("id")

        #identify checin in posts
        if "check-in" in title.lower():
            print(f"Processing check-in post [{post_id}]: '{title}'")

            #get comments to avoid duplicte responses
            comments_url = f"{API_BASE_URL}/api/v1/posts/{post_id}/comments"
            try:
                comments_resp = session.get(comments_url)
                comments_resp.raise_for_status()
                comments = comments_resp.json().get("comments", [])
            except requests.RequestException as e:
                print(f"Could not retrieve comments for post{post_id}: {e}", file=sys.stderr)
                continue

            #deterime in bot has already replied
            already_replied = any(str(c.get("author_id")) == bot_user_id_str for c in comments)
  
            if already_replied:
                print(f"Skipping post {post_id}: Already replied.")
                continue

            #attempt to submit a new reply
            print(f"Submitting reply to post {post_id}...")
            reply_payload = {"body": "Present and accounted for. Task completed automatically via GitHub Actions."}
           
            try:
                reply_resp = session.post(comments_url, json=reply_payload)
                reply_resp.raise_for_status()
                print(f"Successfully replied to post {post_id}.")
            except requests.exceptions.HTTPError as e:
                #handle server window enforcements gracefully
                if e.response is not None and e.response.status_code == 423:
                    print(f"Notice: Check-in window is locked (423) for post {post_id}.")
                else:
                    print(f"HTTP error replying to post {post_id}: {e}", file=sys.stderr)
            except requests.RequestException as e:
                print(f"Network error replying to post {post_id}: {e}", file=sys.stderr)

def main():
    #identity verification
    bot_profile = get_my_profile()
    bot_user_id = bot_profile.get("id")
    print(f"Bot authenticated successfully. User ID: {bot_user_id}")

    #collenct instructor posts
    instructor_posts = collect_instructor_posts()

    #save the metadata file
    output_json_path = os.path.join(ARTIFACT_DIR, "collected.json")
    with open(outut_json_path, 'w', encoding='utf-8') as f:
        json.dump(instructor_posts, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(instructor_posts)} instructor posts to {output_json_path}")

    #handle open check-in actions
    process_check_ins(instructor_posts, bot_user_id)

if__name__ =="__main__":
    main()

                  
          
              
              

  