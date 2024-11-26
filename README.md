# Twitter Following Scraper

This script scrapes the list of accounts a given X user is following. It uses Selenium to automate the process and extracts the usernames into a text file.  Only working for the first scroll. ~40 accounts.

---

## Prerequisites

1. **Python**: Ensure you have Python 3.7 or later installed.
2. **Google Chrome**: Install the latest version of Google Chrome.
3. **Chromedriver**: The script will automatically manage Chromedriver using `webdriver_manager`.

---

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/twitter-following-scraper.git
   cd twitter-following-scraper
Install dependencies:

bash

pip install -r requirements.txt
Create a .env file in the project directory with your Twitter login credentials:


USERNAME=your_twitter_username
PASSWORD=your_twitter_password
Usage
Run the script using the following command:

bash
python following_scraper.py --username TARGET_USERNAME --output_folder OUTPUT_FOLDER

TARGET_USERNAME: The Twitter username of the user whose following list you want to scrape.
OUTPUT_FOLDER: The directory where the scraped list will be saved.
Example:
bash
Copy code
python following_scraper.py --username elonmusk --output_folder ./output
Output
The script will save the extracted usernames to a file named TARGET_USERNAME_following.txt in the specified OUTPUT_FOLDER.

#Notes
You will have to parse the user data 
Ensure your Twitter account has access to the "following" list of the target user.
Twitter's dynamic loading may require slower scrolling or longer run times for large "following" lists.
This script is designed to scrape! Have fun and go wild with it—just remember to be mindful of Twitter's terms of service.
Troubleshooting
Not capturing all usernames: Twitter may limit the visible "following" list depending on session state, account type, or scraping patterns. Retry after some time or use a verified account.
Chromedriver issues: Ensure your Chrome browser is up-to-date, and reinstall dependencies if needed:

bash
pip install --upgrade webdriver_manager