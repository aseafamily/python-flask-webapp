import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

def generate_rss_feed(url, output_file):
    # Step 1: Scrape content from the website
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the website: {url}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Example: Scraping articles with a common HTML structure
    articles = soup.find_all('a', class_='WlydOe')
    if not articles:
        print("No articles found on the website.")
        return

    # Step 2: Initialize the FeedGenerator
    fg = FeedGenerator()
    fg.title('Custom RSS Feed')
    fg.link(href=url, rel='self')
    fg.description('RSS feed generated from the website')

    # Step 3: Add articles to the feed
    for article in articles:
        url = article.get('href')
        title_elem = article.find('div', class_='n0jPhd')
        description_elem = article.find('div', class_='GI74Re')
        date_elem = article.find('div', class_='OSrXXb')
        
        title = title_elem.text if title_elem else "No title"
        description = description_elem.text if description_elem else "No description"
        pub_date = date_elem.text if date_elem else "No date"
        
        # Convert pub_date to a valid date (if needed)
        try:
            pub_date = datetime.datetime.now().isoformat()  # Replace with actual parsing if available
        except Exception as e:
            pub_date = None

    # Add each article as an entry in the RSS feed
    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=url)
    fe.description(description)
    if pub_date:
        fe.pubDate(pub_date)


    # Step 4: Write the RSS feed to a file
    rss_feed = fg.rss_str(pretty=True)
    with open(output_file, 'wb') as file:
        file.write(rss_feed)

    print(f"RSS feed generated successfully: {output_file}")

# Example usage
website_url = "https://www.google.com/search?sca_esv=16785a0985ba4fc4&rlz=1C1VDKB_enUS1016US1016&sxsrf=ADLYWIKNF8k8dLQVuUzDaE5utcns-dR-wg:1735885328005&q=atp&tbm=nws&source=lnms&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3JzWreY9LW7LdGrLDAFqYDH2bHZiU5SwFHpsjQQXz5AGYvVpY8Fv7klAkKlNSPjiPAAhCE2omvSzVwAHtwNMaSGcl7S0mCnSbJYWjsBLpQgSX6KMrHUzS7Ic8aqk8MoW4Lhq3r5wGZxkAsYxlIUardH3q02eUCu30KpmH5-c0yU8W--nUVw&sa=X&ved=2ahUKEwi_zuLi9NiKAxXqHDQIHW7WBUgQ0pQJegQIJRAB&biw=1718&bih=1270&dpr=1"  # Replace with the target website URL
output_rss_file = "custom_feed.xml"
generate_rss_feed(website_url, output_rss_file)
