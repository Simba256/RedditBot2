from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.remote.webelement import WebElement
import random

def expand_shadow_element(driver, element: WebElement) -> WebElement:
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root

def search_reddit(driver, search_terms):
    """
    Searches Reddit using a randomly chosen search term with weighted probability.

    :param driver: The WebDriver instance.
    :param search_terms: A list of search terms.
    """
    try:
        wait = WebDriverWait(driver, 10)

        # Define the XPaths and CSS selectors
        xpath1 = "/html/body/shreddit-app/reddit-header-large/reddit-header-action-items/header/nav/div[2]/div/div/search-dynamic-id-cache-controller/reddit-search-large"
        css_selector1 = "#search-input"

        # Wait for and find the first shadow host element
        element1 = wait.until(EC.presence_of_element_located((By.XPATH, xpath1)))
        print(f"XPath 1: {xpath1} - Element found")

        # Access the shadow root of the first shadow host element
        shadow_root1 = expand_shadow_element(driver, element1)
        if shadow_root1:
            print(f"Shadow Root 1 found")

            # Wait for and find the second shadow host element within the first shadow root
            shadow_host2 = wait.until(lambda d: shadow_root1.find_element(By.CSS_SELECTOR, css_selector1))
            if shadow_host2:
                print(f"Shadow Host 2 found")

                # Access the shadow root of the second shadow host element
                shadow_root2 = expand_shadow_element(driver, shadow_host2)
                if shadow_root2:
                    print(f"Shadow Root 2 found")

                    # Wait for and find the input element using the provided XPath
                    input_element = wait.until(lambda d: shadow_root2.find_element(By.NAME, "q"))
                    if input_element:
                        print(f"Input Element found: {input_element.get_attribute('outerHTML')}")

                        # Choose a random search term with weighted probability
                        weights = [0.3] + [0.7 / (len(search_terms) - 1)] * (len(search_terms) - 1)
                        search_term = random.choices(search_terms, weights=weights, k=1)[0]
                        print(f"Selected Search Term: {search_term}")

                        # Enter the search term into the input element and simulate pressing Enter
                        input_element.send_keys(search_term)
                        input_element.send_keys(Keys.RETURN)
                        
                    else:
                        print("Input Element not found")
                else:
                    print("Shadow Root 2 not found")
            else:
                print("Shadow Host 2 not found")
        else:
            print("Shadow Root 1 not found")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Element not found: {str(e)}")
    
    # Adding a sleep to allow time for output observation
    time.sleep(3)

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the target page
# driver = ... (initialize your WebDriver here)
# search_terms = ["term1", "term2", "term3"]
# search_reddit(driver, search_terms)

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the target page
# driver = ... (initialize your WebDriver here)
# search_terms = ["term1", "term2", "term3"]
# search_reddit(driver, search_terms)


# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the target page
# driver = ... (initialize your WebDriver here)
# search_reddit(driver)

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the target page
# driver = ... (initialize your WebDriver here)
# search_reddit(driver)

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the target page
# driver = ... (initialize your WebDriver here)
# search_reddit(driver)

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the target page
# driver = ... (initialize your WebDriver here)
# search_reddit(driver)

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the target page
# driver = ... (initialize your WebDriver here)
# search_reddit(driver)

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the target page
# driver = ... (initialize your WebDriver here)
# search_reddit(driver)

# element: <input type="text" name="q" placeholder="Search Reddit" autocomplete="off" inputmode="">
# outerHTML: label > div > span.input-container.activated > input[type=text]
# selector: document.querySelector("body > shreddit-app > reddit-header-large > reddit-header-action-items > header > nav > div.h-\\[40px\\].flex-1.py-xs.flex.justify-stretch > div > div > search-dynamic-id-cache-controller > reddit-search-large").shadowRoot.querySelector("#search-input").shadowRoot.querySelector("label > div > span.input-container.activated > input[type=text]")
# xpath: //*[@id="search-input"]//label/div/span[2]/input
# full xpath: /html/body/shreddit-app/reddit-header-large/reddit-header-action-items/header/nav/div[2]/div/div/search-dynamic-id-cache-controller/reddit-search-large//div/div[1]/form/faceplate-search-input//label/div/span[2]/input




# xpath1: /html/body/shreddit-app
# xpath2: /html/body/shreddit-app/reddit-header-large
# xpath3: /html/body/shreddit-app/reddit-header-large/reddit-header-action-items/header/nav/div[2]/div/div/search-dynamic-id-cache-controller/reddit-search-large
# xpath4: /html/body/shreddit-app/reddit-header-large/reddit-header-action-items/header/nav/div[2]/div/div/search-dynamic-id-cache-controller/reddit-search-large//div





# body > shreddit-app > reddit-header-large > reddit-header-action-items > header > nav > div.h-\[40px\].flex-1.py-xs.flex.justify-stretch > div > div > search-dynamic-id-cache-controller > reddit-search-large
# shadow_root
# #search-input
# shadow_root
# label > div > span.input-container.activated > input[type=text]


# label