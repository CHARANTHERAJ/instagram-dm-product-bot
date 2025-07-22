import os
import re
import time
from dotenv import load_dotenv
from instagrapi import Client

# Load environment variables from .env (useful locally)
load_dotenv()

# Get Instagram login details from environment variables
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

if not USERNAME or not PASSWORD:
    raise Exception("Please set IG_USERNAME and IG_PASSWORD in environment variables.")

# Initialize and login
cl = Client()
cl.login(USERNAME, PASSWORD)

# To track last seen messages
seen_threads = set()

def extract_reel_link(text):
    """Extract Instagram reel link from message text"""
    pattern = r"(https?://www\.instagram\.com/reel/[A-Za-z0-9_-]+)"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def generate_product_link(reel_link):
    """Fake product link generator (replace this with real logic if needed)"""
    return f"https://yourstore.com/product?ref={reel_link[-10:]}"

def listen_for_dms():
    print("Listening for new DMs...")

    while True:
        inbox = cl.direct_threads(amount=10)
        for thread in inbox:
            thread_id = thread.id
            if thread_id in seen_threads:
                continue

            # Get last message
            if not thread.messages:
                continue

            last_msg = thread.messages[0]
            sender_username = last_msg.user.username
            message_text = last_msg.text

            print(f"New message from {sender_username}: {message_text}")

            # Check for reel link
            reel_link = extract_reel_link(message_text)
            if reel_link:
                product_link = generate_product_link(reel_link)
                cl.direct_send(text=f"Here's your product link: {product_link}", user_ids=[last_msg.user_id])
                print(f"Replied to {sender_username} with product link.")
            else:
                print("No valid reel link found in message.")

            # Mark thread as seen
            seen_threads.add(thread_id)

        time.sleep(10)  # Wait before checking again

if __name__ == "__main__":
    listen_for_dms()
