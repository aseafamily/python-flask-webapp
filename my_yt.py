import requests
from bs4 import BeautifulSoup
import re

def get_latest_videos(channel_url):
    # Add headers to mimic a real browser visit
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Send a request to the channel's videos page
    response = requests.get(f"{channel_url}/videos", headers=headers)
    response.raise_for_status()  # Ensure the request was successful
    
    # Parse the page content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find video elements; YouTube's structure may vary, so this may need adjustment
    video_elements = soup.find_all("a", {"id": "video-title"}, limit=5)
    
    videos = []
    
    for video in video_elements:
        # Get video title
        title = video.get("title")
        
        # Get video URL (appending YouTube base URL)
        video_url = "https://www.youtube.com" + video.get("href")
        
        # Request individual video page to extract more info
        video_response = requests.get(video_url, headers=headers)
        video_soup = BeautifulSoup(video_response.text, "html.parser")
        
        # Extract video duration and upload date
        try:
            duration = video_soup.find("span", {"class": "ytp-time-duration"}).text
        except AttributeError:
            duration = "Duration not found"
        
        try:
            datetime = video_soup.find("meta", {"itemprop": "datePublished"})["content"]
        except (AttributeError, TypeError):
            datetime = "Date not found"
        
        # Store video info in a dictionary
        videos.append({
            "title": title,
            "url": video_url,
            "duration": duration,
            "datetime": datetime
        })
    
    return videos

# Example usage
channel_url = "https://www.youtube.com/channel/UC5_qnc3r9Ln4nrGT0sWPgaw"
latest_videos = get_latest_videos(channel_url)

for video in latest_videos:
    print(f"Title: {video['title']}")
    print(f"URL: {video['url']}")
    print(f"Duration: {video['duration']}")
    print(f"Date Published: {video['datetime']}")
    print("-" * 40)
