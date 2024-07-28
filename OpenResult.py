from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

def open_random_search_result(driver):
    """
    Opens a random page from the first three search results.

    :param driver: The WebDriver instance.
    """
    try:
        wait = WebDriverWait(driver, 10)

        # Randomly select one of the first three search results
        random_index = random.randint(1, 3)

        # List of possible XPaths for each result
        xpath = f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{random_index}]/div/faceplate-tracker/a"

        random_result = None

        # Loop through the possible XPaths and find a clickable element
    
        try:
            random_result = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            print(f"Element not found for XPath: {xpath}")

        if random_result:
            print(f"Selected Result: {random_result.get_attribute('outerHTML')}")

            # Click the selected result to open the page
            random_result.click()

            # Wait for the new page to load
            time.sleep(3)
        else:
            print("No clickable search result found.")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Element not found: {str(e)}")

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the search results page
# driver = ... (initialize your WebDriver here)
# open_random_search_result(driver)

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the search results page
# driver = ... (initialize your WebDriver here)
# open_random_search_result(driver)



# /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/div/faceplate-tracker/a
# /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[2]/div/faceplate-tracker/a
# /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[3]/div/faceplate-tracker/a