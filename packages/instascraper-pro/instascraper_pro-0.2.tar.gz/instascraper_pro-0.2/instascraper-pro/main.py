import os
from instascraper.instagram import InstagramAnalyzer
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get credentials from environment
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        print(" ERROR: Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in your .env file.")
        return

    # Initialize the scraper
    scraper = InstagramAnalyzer(username, password, headless=True, verbose=True)
    
    try:
        scraper.setup_driver()
        scraper.login()

        target_profile = "nasa"

        # Extract profile details
        profile_data = scraper.extract_profile_details(target_profile)
        print("\nProfile Details:")
        print(profile_data)

        # Collect all post URLs
        #post_urls = scraper.collect_all_posts(target_profile)
        #print(f"\nFound {len(post_urls)} posts.")

        # Analyze first n posts
        #analyzed_posts = []
        #for url in post_urls[:n]:
            #post_data = scraper.analyze_single_post(url, take_screenshot=True)
            #analyzed_posts.append(post_data)
            #print("\nPost Analysis:")
            #print(post_data)


        # Optionally save results
        scraper.save_profile_to_json(profile_data, f"{target_profile}_profile.json")
        #scraper.save_posts_to_json(analyzed_posts, f"{target_profile}_posts.json")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        scraper.logout()

if __name__ == "__main__":
    main()
