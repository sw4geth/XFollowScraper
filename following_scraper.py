# -*- coding: utf-8 -*-
"""Twitter Following Scraper"""

import argparse
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

# Initialize a global variable for the WebDriver
driver = ""

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


# Function to create the WebDriver instance and log in
def create_driver(username):
    global driver

    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to Twitter login page and enter credentials
    driver.get("https://x.com/i/flow/login")
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="text"]'))
    )
    username_input.send_keys(USERNAME)
    username_input.send_keys(Keys.RETURN)
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
    )
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    # Wait for login to complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@aria-label="Profile"]'))
    )
    print("Logged in successfully.")

    # Explicitly navigate to the following page
    driver.get(f"https://x.com/{username}/following")
    time.sleep(5)  # Allow time for the page to load fully
    print("Navigated to:", driver.current_url)


# Function to scrape the following list
def scrape_users():
    start_time = time.time()

    # Wait for the "following" section to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div",
            )
        )
    )

    following_users = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Locate all user entries in the "following" list
        users = driver.find_elements(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div",
        )
        print(f"Found {len(users)} users on this scroll")  # Debugging output

        # Extract text or details from each user entry
        for user in users:
            try:
                user_text = user.text
                if user_text and user_text not in following_users:  # Avoid duplicates
                    following_users.append(user_text)
            except Exception as e:
                print(f"Error extracting user: {e}")

        # Scroll down and wait for the page to load more users
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(2)  # Adjust based on load times
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Scrolling took {execution_time} seconds to execute.")
    return following_users


# Function to save the following list to a file
def save_users(data, username, output_folder):
    start_time = time.time()

    # Create the specified output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Save data to a file
    file_path = os.path.join(output_folder, f"{username}_following.txt")
    with open(file_path, "w") as file:
        for line in data:
            file.write(line + "\n")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Saving took {execution_time} seconds to execute.")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Scrape Twitter following list.")
    parser.add_argument("--username", required=True, help="Twitter username to scrape")
    parser.add_argument(
        "--output_folder", required=True, help="Output folder to store the file"
    )

    args = parser.parse_args()

    print(
        "Creating the driver and logging in: It may take some time if it's the first time."
    )
    create_driver(args.username)
    print("Driver created and logged in successfully.")

    print(f"Scraping the following list for {args.username}...")
    data = scrape_users()
    print("Following list scraped successfully.")

    print(f"Saving the following list to file...")
    save_users(data, args.username, args.output_folder)
    print("Following list saved successfully.")

    # Close the WebDriver instance
    driver.quit()
