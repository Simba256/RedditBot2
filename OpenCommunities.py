from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def open_communities(driver):
    try:
        wait = WebDriverWait(driver, 10)

        xpath = "/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[1]/div/div[1]/faceplate-tabgroup/a[1]/span/span/faceplate-tracker"

        try:
            # Wait for the element to be present
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            print("Found communities button")

            # Scroll the element into view
            # driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)  # Give time for the scroll action to complete

            # Ensure the element is visible and clickable
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            # Click the element
            element.click()
            print("Clicked communities button")

            # Wait for the communities tab to load
            time.sleep(3)  # Adjust the sleep time as necessary

        except TimeoutException:
            print("Communities button not found")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Element not found: {str(e)}")

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the search results page
# driver = ... (initialize your WebDriver here)
# open_communities(driver)
