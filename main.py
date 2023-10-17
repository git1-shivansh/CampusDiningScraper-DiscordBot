import discord
from discord.ext import commands
import time
import os
from dotenv import load_dotenv


from selenium import webdriver
from selenium.webdriver.common.by import By

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Ensure this intent is enabled in your Discord Developer Portal as well.

def scrape_menu(meal, date):

    '''
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    '''

    driver = webdriver.Chrome()

    website = 'https://asu.campusdish.com/DiningVenues/TempeBarrettDiningCenter'
    driver.get(website)

    # Close pop-ups
    cross1 = driver.find_element(By.XPATH, '//button[@class="sc-dCFHLb ciePfj"]')
    cross2 = driver.find_element(By.XPATH,
                                 '//button[@class="onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon"]')
    cross1.click()
    cross2.click()

    time.sleep(5)

    # Change meal type if needed
    changeMealButton = driver.find_element(By.XPATH, '//button[@class="sc-gdyeKB iyulWo DateMealFilterButton"]')
    changeMealButton.click()
    current_value = driver.find_element(By.CSS_SELECTOR, ".css-15gud3p-singleValue").text

    # Change date

    desired_date_element = driver.find_element(By.XPATH, '//button[@aria-label="Choose a Date to Show Menu"]')
    desired_date_element.click()
    desired_date_element = driver.find_element(By.XPATH, f'//div[@aria-label="Choose {date}"]')
    desired_date_element.click()


    time.sleep(5)

    meal_xpath = f"//div[text()='{meal}']"

    if current_value != meal:
        dropdown = driver.find_element(By.CSS_SELECTOR, ".select-wrapper-main.css-b62m3t-container .css-6e0f30-control")
        dropdown.click()
        time.sleep(5)

        meal_option = driver.find_element(By.XPATH, meal_xpath)
        meal_option.click()

    # Confirm the changes
    doneButton = driver.find_element(By.XPATH, '//button[@class="sc-aXZVg sc-gEvEer iekijp bscJkh Done"]')
    doneButton.click()

    time.sleep(5)

    entrees_headings = driver.find_elements(By.XPATH,
                                            "//div[@data-category='entrées_4295'][not(ancestor::div[@id='9124'])]//h3[@class='sc-kAkpmW lhUkLi HeaderItemName']/span")
    entree_names = [entree.text for entree in entrees_headings]

    hotSandwiches_headings = driver.find_elements(By.XPATH,
                                                  "//div[@data-category='hot_sandwiches_4295'][not(ancestor::div[@id='9124'])]//h3[@class='sc-kAkpmW lhUkLi HeaderItemName']/span")
    hotSandwiches_names = [hotSandwiches.text for hotSandwiches in hotSandwiches_headings]

    sides_headings = driver.find_elements(By.XPATH,
                                          "//div[@data-category='sides_4295'][not(ancestor::div[@id='9124'])]//h3[@class='sc-kAkpmW lhUkLi HeaderItemName']/span")  # replace 'sides_XXXX' with the correct category attribute for sides
    side_names = [side.text for side in sides_headings]

    # If 'entrées' heading exists, scrape 'entrées'. Otherwise, scrape 'sandwiches'
    entrees_exist_9125 = driver.find_elements(By.XPATH, "//div[@id='9125']//div[contains(@data-category, 'entrées')]")

    if entrees_exist_9125:
        entrees_headings_9125 = driver.find_elements(By.XPATH,
                                                     "//div[@id='9125']//div[contains(@data-category, 'entrées')]//h3[@class='sc-kAkpmW lhUkLi HeaderItemName']/span")
        entree_names_9125 = [entree.text for entree in entrees_headings_9125]
        entree_names.extend(entree_names_9125)  # Append the new names to the existing list
    else:
        sandwiches_headings_9125 = driver.find_elements(By.XPATH,
                                                        "//div[@id='9125']//div[contains(@data-category, 'sandwiches')]//h3[@class='sc-kAkpmW lhUkLi HeaderItemName']/span")
        sandwich_names_9125 = [sandwich.text for sandwich in sandwiches_headings_9125]
        entree_names.extend(sandwich_names_9125)  # Append the new names to the existing list

    # Scraping the pizza headings
    pizza_headings = driver.find_elements(By.XPATH,
                                          "//div[@data-category='pizza_4295']//h3[@class='sc-kAkpmW lhUkLi HeaderItemName']/span")
    pizza_names = [pizza.text for pizza in pizza_headings]

    print("Entrees:", entree_names)
    print("Sides:", side_names)
    print("Pizza:", pizza_names)
    print("Hot Sandwiches:", hotSandwiches_names)
    results = {
        "Entrees": entree_names,
        "Sides": side_names,
        "Pizza": pizza_names,
        "Hot Sandwiches": hotSandwiches_names
    }
    return results


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('Bot is ready')
    channel = bot.get_channel(1124371481825136683)
    await channel.send("Hello! I'm online now 🚀")

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")
    await bot.process_commands(message)  # Make sure to process other commands!

@bot.event
async def on_command_error(ctx, error):
    print(f"Command error: {error}")


def format_as_table(data):
    # Find the maximum width for each column
    max_widths = {
        "Category": max(len("Category"), max(len(category) for category in data.keys())),
        "Items": max(len("Items"), max(len(item) for items in data.values() for item in items))
    }

    # Create a divider based on the max widths
    divider = '+-' + '-' * max_widths["Category"] + '-+' + '-' * max_widths["Items"] + '-+'

    # Create the header row
    header = "| {Category:<{Category_width}} | {Items:<{Items_width}} |".format(
        Category="Category",
        Category_width=max_widths["Category"],
        Items="Items",
        Items_width=max_widths["Items"]
    )

    table = [divider, header, divider]

    # Add each row for each category
    for category, items in data.items():
        for item in items:
            row = "| {Category:<{Category_width}} | {Items:<{Items_width}} |".format(
                Category=category if items.index(item) == 0 else "",  # only show category on first item
                Category_width=max_widths["Category"],
                Items=item,
                Items_width=max_widths["Items"]
            )
            table.append(row)
        table.append(divider)

    return "\n".join(table)


@bot.command()
async def menu(ctx, meal, *, date):  # The * means "consume the rest of the message as this argument"
    # Run your scraping function with provided parameters
    scraped_data = scrape_menu(meal, date)

    # Format the data as a table
    table = format_as_table(scraped_data)

    full_message = f"Menu for {meal} on {date}:\n```\n{table}\n```"  # use code block for monospace font
    await ctx.send(full_message)


load_dotenv()
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
bot.run(BOT_TOKEN)
