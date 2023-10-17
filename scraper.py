import time

from selenium import webdriver
from selenium.webdriver.common.by import By

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
    date = "Wednesday, October 18th, 2023"

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
