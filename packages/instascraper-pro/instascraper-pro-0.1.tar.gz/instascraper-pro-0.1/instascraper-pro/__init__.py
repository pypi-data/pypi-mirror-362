import getpass
import sys

PASSWORD = "Leafcraft123"

entered = getpass.getpass("Enter the instascraper password to unlock: ")
if entered != PASSWORD:
    print("Incorrect password. Exiting.")
    sys.exit(1)

from instascraper.instagram import InstagramAnalyzer

