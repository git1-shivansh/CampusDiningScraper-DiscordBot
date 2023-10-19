## MealScrapeBot: A Discord Bot for Menu Scraping
Introduction
MealScrapeBot is a Python-based Discord bot designed to scrape menu items from the ASU Barrett Dining Center's website. Users can interact with the bot to request the menu for specific meals on specific dates, and the bot responds with the details in a tabulated format.

## Dependencies:
1. discord.py: The primary library used to interface with the Discord API.
2. python-dotenv: A module to manage environment variables, particularly useful for keeping the bot token secure.
3. selenium: The web scraping library that allows the bot to navigate and extract data from the dining center's website.

## Code Structure:
Imports and Initial Setup: Libraries and extensions needed for the bot's operation are imported. This includes command extensions from discord.py and the web driver setup for Selenium.

Selenium-based Web Scraping: The scrape_menu function is the core function that visits the website, navigates through it using the provided date and meal parameters, and extracts the menu items. It uses Chrome's web driver for this purpose.

Discord Bot Events and Commands:

on_ready: Event triggered when the bot logs in and becomes ready.
hello: A simple command to test the bot's responsiveness.

on_message: Event that captures and logs every message in channels the bot has access to.
on_command_error: Logs any command errors.

menu: A command that triggers the scrape_menu function and sends the scraped data to the Discord channel in a tabulated format.
Data Formatting: The format_as_table function formats the scraped data as a table to present it in a readable manner on Discord.

Bot Initialization: The bot token is retrieved from environment variables and the bot is set to run

## Prerequisites

- Python 3.x
- Virtual environment (recommended)

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone [your-repo-link]
   cd WebScraperV2
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
3. Update the.env file with your Discord BOT key
## Usage

1. Run the main script:
   ```bash
   python main.py


