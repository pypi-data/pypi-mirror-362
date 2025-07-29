import time
import os
import re
import cv2
import easyocr
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class InstagramAnalyzer:
    def __init__(self, username, password, headless=True, verbose=True):
        self.username = username
        self.password = password
        self.headless = headless
        self.verbose = verbose
        self.driver = None

    def log(self, message):
        if self.verbose:
            print(message)

    def setup_driver(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-notifications")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--user-agent=Mozilla/5.0")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, "username")))
        self.driver.find_element(By.NAME, "username").send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 30).until(lambda d: "instagram.com" in d.current_url and "login" not in d.current_url)
        time.sleep(2)
        try:
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()
        except:
            pass

    def logout(self):
        if self.driver:
            self.driver.quit()

    def extract_number(self, text):
        if not text:
            return 0
        text = text.replace(",", "").lower()
        m = re.match(r"([\d\.]+)([kmb]?)", text)
        if m:
            num = float(m.group(1))
            mult = {"k":1e3, "m":1e6, "b":1e9}.get(m.group(2),1)
            return int(num * mult)
        return 0

    def extract_profile_details(self, target_username):
        self.driver.get(f"https://www.instagram.com/{target_username}/")
        time.sleep(5)
        data = {
            "username": target_username,
            "posts": 0,
            "followers": 0,
            "following": 0,
            "verified": "No",
            "bio": "",
            "full_name": ""
        }
        # Stats
        stats = self.driver.find_elements(By.XPATH, '//header//section//ul//li')
        if len(stats) >= 3:
            data["posts"] = self.extract_number(stats[0].text)
            data["followers"] = self.extract_number(stats[1].text)
            data["following"] = self.extract_number(stats[2].text)
        # Verified
        try:
            self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Verified')]")
            data["verified"] = "Yes"
        except:
            pass
        # Full Name
        try:
            data["full_name"] = self.driver.find_element(By.XPATH, "//section/main//h1").text
        except:
            pass
        # Bio
        try:
            bio = self.driver.find_element(By.XPATH, "//section/main//h1/../../div[2]/span").text
            data["bio"] = bio
        except:
            pass
        return data

    def collect_all_posts(self, target_username):
        self.driver.get(f"https://www.instagram.com/{target_username}/")
        time.sleep(3)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        links = set()
        last_height = 0
        attempts = 0
        while True:
            posts = self.driver.find_elements(By.XPATH, '//a[contains(@href,"/p/") or contains(@href,"/reel/")]')
            before = len(links)
            for p in posts:
                href = p.get_attribute("href")
                if href:
                    links.add(href)
            after = len(links)
            if after == before:
                attempts +=1
                if attempts > 5:
                    break
            else:
                attempts =0
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        return list(links)

    def analyze_single_post(self, url, take_screenshot=False):
        self.driver.get(url)
        time.sleep(3)
        post = {"url": url, "likes":0, "comments":0}
        # Likes
        try:
            like_element = self.driver.find_element(By.XPATH, "//section//button/span")
            post["likes"] = self.extract_number(like_element.text)
        except:
            pass
        # Comments
        try:
            comments = self.driver.find_elements(By.XPATH, "//ul/li/div/div/div[2]/span")
            post["comments"] = len(comments)-1
        except:
            pass
        # Caption
        try:
            post["caption"] = self.driver.find_element(By.XPATH, "//article//span").text
        except:
            post["caption"] = ""
        # Screenshot
        if take_screenshot:
            os.makedirs("screenshots", exist_ok=True)
            path = f"screenshots/{int(time.time())}.png"
            self.driver.save_screenshot(path)
            post["screenshot"] = path
        return post

    def save_profile_to_csv(self, data, filename):
        df = pd.DataFrame([data])
        df.to_csv(filename, index=False)

    def save_profile_to_json(self, data, filename):
        df = pd.DataFrame([data])
        df.to_json(filename, orient='records', lines=True)

    def save_posts_to_json(self, posts, filename):
        df = pd.DataFrame(posts)
        df.to_json(filename, orient='records', lines=True)

    def save_posts_to_csv(self, posts, filename):
        df = pd.DataFrame(posts)
        df.to_csv(filename, index=False)

    def analyze_profile(self, target_username, max_posts=None, take_screenshots=False):
        profile = self.extract_profile_details(target_username)
        self.save_profile_to_csv(profile, f"{target_username}_profile.csv")
        urls = self.collect_all_posts(target_username)
        if max_posts:
            urls = urls[:max_posts]
        results = []
        for i, url in enumerate(urls,1):
            post = self.analyze_single_post(url, take_screenshots)
            results.append(post)
        self.save_posts_to_csv(results, f"{target_username}_posts.csv")
        return {"profile": profile, "posts": results}

    def analyze_profiles(self, usernames, max_posts=None, take_screenshots=False):
        all_results = {}
        for username in usernames:
            self.log(f"Analyzing {username}...")
            result = self.analyze_profile(username, max_posts, take_screenshots)
            all_results[username] = result
        return all_results

    def get_profile_stats_only(self, username):
        profile = self.extract_profile_details(username)
        self.save_profile_to_csv(profile, f"{username}_profile_stats.csv")
        return profile
