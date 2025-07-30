import os
from .instagram import InstagramAnalyzer
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get credentials from environment
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        print("ERROR: Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in your .env file.")
        return

    # Prompt user for multiple target profiles
    profiles_input = "nasa, natgeo"
    target_profiles = [p.strip() for p in profiles_input.split(",") if p.strip()]

    if not target_profiles:
        print("ERROR: No valid profiles provided.")
        return

    # Initialize the scraper
    scraper = InstagramAnalyzer(username, password, headless=True, verbose=True)

    try:
        scraper.setup_driver()
        scraper.login()

        # Loop over each target profile
        for profile in target_profiles:
            print(f"\n==== Extracting data for '{profile}' ====")

            # Extract profile details
            profile_data = scraper.extract_profile_details(profile)
            print("\nProfile Details:")
            print(profile_data)

            # Optionally collect posts (commented out)
            # post_urls = scraper.collect_all_posts(profile)
            # print(f"\nFound {len(post_urls)} posts.")

            # Optionally analyze first N posts
            # analyzed_posts = []
            # for url in post_urls[:n]:
            #     post_data = scraper.analyze_single_post(url, take_screenshot=True)
            #     analyzed_posts.append(post_data)
            #     print("\nPost Analysis:")
            #     print(post_data)

            # Save results
            scraper.save_profile_to_json(profile_data, f"{profile}_profile.json")
            # scraper.save_posts_to_json(analyzed_posts, f"{profile}_posts.json")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        scraper.logout()

if __name__ == "__main__":
    main()
