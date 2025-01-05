from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
import json
import os
from azure.storage.fileshare import ShareFileClient
from flask_login import login_required
from datetime import datetime, timedelta
from collections import Counter
import feedparser
import random
import requests

news_bp = Blueprint('news', __name__)

RSS_FEEDS = [
    #'https://www.seattletimes.com/eastside/feed/',
    'https://news.google.com/rss/search?q=tennis&hl=en-US&gl=US&ceid=US:en',
    'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en',
    'https://feeds.bbci.co.uk/sport/tennis/rss.xml',
    'https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml',
    'http://feeds.bbci.co.uk/news/technology/rss.xml',
    'http://feeds.bbci.co.uk/news/business/rss.xml',
    'http://feeds.bbci.co.uk/news/world/rss.xml',
    'https://news.google.com/rss/search?q=finance&hl=en-US&gl=US&ceid=US:en'
    # Add more RSS feed URLs as needed
]

def time_ago(pub_date):
    now = datetime.now()
    pub_date = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z')
    diff = now - pub_date

    if diff.total_seconds() < 3600:  # Less than an hour
        minutes = int(diff.total_seconds() // 60)
        return f"{minutes} minutes ago"
    elif diff.total_seconds() < 86400:  # Less than a day
        hours = int(diff.total_seconds() // 3600)
        return f"{hours} hours ago"
    else:
        return pub_date.strftime('%Y-%m-%d %H:%M:%S')  # Fallback to a standard format

@news_bp.route('/news')
def index():
    all_items = []
    seen_urls = set()  # Set to track unique URLs

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        channel_title = feed.feed.title if 'title' in feed.feed else 'No Title'
        
        for entry in feed.entries:
            # Get the first image URL from media:content if it exists
            image_url = entry.get('media_thumbnail', [{}])[0].get('url', '') if entry.get('media_thumbnail') else ''

            item = {
                'title': entry.title,
                'description': entry.get('description', ''),
                'channel_name': channel_title,
                'url': entry.link,
                'image_url': image_url,  # Use the extracted image URL
                'pub_date': entry.get('published', '')
            }

            # Only add the item if the URL has not been seen before
            if item['url'] not in seen_urls:
                seen_urls.add(item['url'])  # Add the URL to the set
                all_items.append(item)  # Add the item to the list

    # Shuffle the items
    random.shuffle(all_items)

    # Filter out items with pub_date more than 1 day old
    one_day_ago = datetime.now() - timedelta(days=1)
    all_items = [item for item in all_items if datetime.strptime(item['pub_date'], '%a, %d %b %Y %H:%M:%S %Z') > one_day_ago]

    # Sort items by pub_date in descending order
    #all_items.sort(key=lambda x: datetime.strptime(x['pub_date'], '%a, %d %b %Y %H:%M:%S %Z'), reverse=True)

    # After sorting, update the pub_date to be more human-readable
    for item in all_items:
        item['pub_date'] = time_ago(item['pub_date'])

    return render_template('news_index.html', items=all_items)
    #return render_template('news_focus.html', items=all_items)