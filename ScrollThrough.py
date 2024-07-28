from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.remote.webelement import WebElement
import random
from SearchReddit import expand_shadow_element
from time import sleep





# from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import re

def expand_shadow_element(driver, element: WebElement) -> WebElement:
    """
    Expands a shadow DOM element.

    :param driver: The WebDriver instance.
    :param element: The WebElement representing the shadow host.
    :return: The shadow root WebElement.
    """
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root


def find_elements_in_shadow_root(driver, shadow_root: WebElement, pattern_xpath: str) -> list:
    """
    Finds elements in the shadow root that match the given XPath pattern.

    :param driver: The WebDriver instance.
    :param shadow_root: The shadow root WebElement.
    :param pattern_xpath: The XPath pattern to match.
    :return: A list of matching WebElements.
    """
    all_elements = shadow_root.find_elements(By.XPATH, ".//*")
    print("All elements found in shadow root:", all_elements)
    matching_elements = []

    for element in all_elements:
        try:
            element_id = element.get_attribute("id")
            if element_id and re.match(r'^t3_[a-zA-Z0-9]{7}$', element_id):  # Updated regex pattern for 10-character IDs
                full_xpath = f"//*[@id='{element_id}']{pattern_xpath}"
                matching_element = shadow_root.find_element(By.XPATH, full_xpath)
                matching_elements.append(matching_element)
        except NoSuchElementException:
            continue

    return matching_elements

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the page
# Assuming `shadow_root` is the shadow root WebElement you have already accessed
# pattern_xpath = "//div[2]/span/span/button[1]"
# matching_elements = find_elements_in_shadow_root(driver, shadow_root, pattern_xpath)
# print(matching_elements)


def upvote_post(driver, shadow_host_xpath: str):
    """
    Searches for elements within a shadow DOM that match the given XPath pattern.

    :param driver: The WebDriver instance.
    :param shadow_host_xpath: The XPath to the shadow host element.
    :param pattern_xpath: The XPath pattern to match inside the shadow DOM.
    """
        

    wait = WebDriverWait(driver, 10)
    print("Shadow searching")
    try:
        shadow_host = wait.until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath)))
        shadow_root = expand_shadow_element(driver, shadow_host)
        print("Shadow root found")
        
        try:

            upvote_button = shadow_root.find_element(By.CSS_SELECTOR, "div.flex.flex-row.items-center.flex-nowrap.overflow-hidden.justify-start > span > span > button.group.button.flex.justify-center.aspect-square.p-0.border-0.button-secondary.disabled\:text-interactive-content-disabled.button-plain.inline-flex.items-center.hover\:text-action-upvote.focus-visible\:text-action-upvote")
            # upvote_button = shadow_root.find_element(By.)
            print("Upvote button found")

            try:
                upvote_button.click()
                print("Upvote button clicked")
            except Exception as e:
                print(f"Error clicking upvote button")

        except:
            print("Upvote button not found")

    except TimeoutException:
        print("Shadow host not found or timed out")

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the page
# shadow_host_xpath = "/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/article[5]/shreddit-post"
# pattern_xpath = "//div[2]/span/span/button[1]"
# upvote_post(driver, shadow_host_xpath, pattern_xpath)



def upvote_comment(driver, comment_number):
    """
    Find the comments, move into view and upvote it
    """

    try:
        comment_shadow_element_xpath = f"/html/body/shreddit-app/div/div[1]/div/main/div/report-flow-provider/faceplate-batch/shreddit-comment-tree/shreddit-comment[{comment_number}]/shreddit-comment-action-row"
        comment_shadow_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, comment_shadow_element_xpath)))
        print(f"Comment {comment_number} found: {comment_shadow_element.get_attribute('outerHTML')}")

        sleep(random.uniform(0.1, 0.3))
        # Expand the shadow root
        comment_shadow_root = expand_shadow_element(driver, comment_shadow_element)
        print(f"Comment {comment_number} shadow root expanded.")

        # Find the upvote button within the shadow root
        upvote_button_xpath = "//*[@id=\"comment-tree\"]/shreddit-comment[2]/shreddit-comment-action-row//div/div/div[1]/span/button[1]"
        upvote_button = comment_shadow_root.find_element(By.XPATH, upvote_button_xpath)
        print(f"Upvote button found: {upvote_button.get_attribute('outerHTML')}")
        sleep(random.uniform(0.1, 0.5))

        # Click the upvote button
        upvote_button.click()
        print(f"Upvoted comment {comment_number}.")
    except:
        print("Comment not found or error upvoting")
        

    

def find_comment(driver, comment_number):
    """
    Scroll so that comment
    """

    try:
        # Find the comment
        comment_xpath = f"/html/body/shreddit-app/div/div[1]/div/main/div/report-flow-provider/faceplate-batch/shreddit-comment-tree/shreddit-comment[{comment_number}]/shreddit-comment-action-row"
        comment_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, comment_xpath)))
        print(f"Comment {comment_number} found: {comment_element.get_attribute('outerHTML')}")

        # Scroll the comment into view
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", comment_element)
        print(f"Comment {comment_number} scrolled into view.")
    except:
        print("Comment not found")

def scroll_through_post(driver, scroll_time):
    """
    Scroll through the post for a specified amount of time, scrolling slowly and pausing randomly.
    Upvote comments at random intervals.
    """

    scroll_time = scroll_time * 60  # Convert minutes to seconds
    end_time = time.time() + scroll_time  # Calculate end time

    comment_count = 0
    comment_to_upvote = random.randint(1, 6) # Randomly select a comment to upvote
    while time.time() < end_time:
        # Scroll down in small increments
        driver.execute_script("window.scrollBy(0, " + str(random.randint(100, 300)) + ")")
        time.sleep(random.uniform(1.5, 3))

        comment_to_upvote -= 1
        comment_count += 1

        find_comment(driver, comment_count)

        if comment_to_upvote == 0:
            upvote_comment(driver, comment_count)
        if comment_to_upvote <= 0:
            comment_to_upvote = random.randint(1, 6)


def exit_post(driver):
    """
    Clicks on back button to exit the post.
    """
    driver.back()
    sleep(0.8)
    print("Going to previous page")

def open_post(driver, shadow_host_xpath: str):
    """
    Searches for elements within a shadow DOM that match the given XPath pattern.

    :param driver: The WebDriver instance.
    :param shadow_host_xpath: The XPath to the shadow host element.
    :param pattern_xpath: The XPath pattern to match inside the shadow DOM.
    """


    wait = WebDriverWait(driver, 10)
    print("Shadow searching")
    try:
        shadow_host = wait.until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath)))
        sleep(random.uniform(2, 4))

        try:
            # open click on the shadow host element
            shadow_host.click()
            print("Shadow host clicked")
            sleep(1.3)

            scroll_through_post(driver, random.randint(1, 3))
            exit_post(driver)


        except:
            print("Error clicking on post")

    except:
        print("Shadow host not found or timed out")


def scroll_through(driver, scroll_time):
    """
    Scrolls through the page for a specified amount of time, scrolling slowly and pausing randomly,
    while continuously waiting for new content to load.

    :param driver: The WebDriver instance.
    :param scroll_time: The time to scroll in minutes.
    """
    try:

        time.sleep(2) # wait for the page to load


        # Get the initial scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        # Calculate end time
        end_time = time.time() + scroll_time * 60  # Convert minutes to seconds
        
        posts_visited = 0
        index_to_click = 0
        index_to_open = 0

        while time.time() < end_time:
            # Scroll down in small increments
            posts_to_visit = random.randint(1, 3)
            xpath_in_view = get_visible_elements_xpath(driver, posts_visited, posts_visited + posts_to_visit)
            posts_visited += posts_to_visit
            if xpath_in_view is None:
                continue

            print("XPaths in view:",xpath_in_view)

            wait = WebDriverWait(driver, 10)

            # pick a random number 1 to 10
            if index_to_click == 0:
                upvote_post(driver, xpath_in_view)

            print("Index to click:", index_to_click)

            if index_to_open == 0:
                open_post(driver, xpath_in_view)
            
            index_to_click -= 1                
            if index_to_click <= 0:
                index_to_click = random.randint(1, 10)
            
            index_to_open -= 1
            if index_to_open <= 0:  
                index_to_open = random.randint(1, 10)


            # scroll a random number between 300 and 500 pixels
            driver.execute_script("window.scrollBy(0, " + str(random.randint(300, 500)) + ")")

            # Wait to load the page
            time.sleep(random.uniform(1.5, 3))  # Random wait time between 1.5 to 3 seconds

            # Optionally, add randomness to the pause
            if random.random() < 0.1:  # 10% chance to pause longer
                pause_duration = random.uniform(5, 15)  # Pause between 5 to 15 seconds
                print(f"Pausing for {pause_duration:.2f} seconds...")
                time.sleep(pause_duration)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # Wait for some time to allow more content to load if available
                print("Waiting for new content to load...")
                time.sleep(random.uniform(3, 7))  # Wait for 3 to 7 seconds for new content
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                # If no new content is loaded after waiting, consider it as the end
                # if new_height == last_height:
                #     print("No new content loaded. Ending scroll.")
                #     break
                last_height = new_height
            else:
                last_height = new_height

    except Exception as e:
        print(f"Error scrolling through the page: {str(e)}")




# from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webelement import WebElement
# import time

def is_element_in_view(driver, element: WebElement) -> bool:
    """
    Checks if an element is within the visible viewport.

    :param driver: The WebDriver instance.
    :param element: The WebElement to check.
    :return: True if the element is in view, False otherwise.
    """
    view_top = driver.execute_script("return window.pageYOffset;")
    view_bottom = view_top + driver.execute_script("return window.innerHeight;")
    element_top = element.location['y']
    element_bottom = element_top + element.size['height']
    
    return element_bottom >= view_top and element_top <= view_bottom

def get_visible_elements_xpath(driver, l, r):
    """
    Lists the XPaths of elements matching the specified pattern that are in view on the current page.

    :param driver: The WebDriver instance.
    :return: A list of XPaths of elements that are in view.
    """
    print("Trying to get visible xpath", l+1, r+1)
    xpath = None
    print("Trying to get visible xpath")
    for i in range(l+1, r+1):  # Adjust the range as needed based on the expected number of elements
        current_xpath = f"/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/article[{i}]/shreddit-post"
        try:
            element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, current_xpath)))
            
            if is_element_in_view(driver, element):
                xpath = current_xpath
                print("XPath in view:", xpath)
                # sleep for a random amount between 2 and 4 seconds
                time.sleep(random.uniform(2, 4))
        
        except:
            print("Element not found")
            continue

    print("Returning xpath")
    return xpath

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the page
# visible_xpaths = get_visible_elements_xpaths(driver)
# print(visible_xpaths)


def is_element_in_view(driver, element: WebElement) -> bool:
    """
    Checks if an element is in view in the current viewport.

    :param driver: The WebDriver instance.
    :param element: The WebElement to check.
    :return: True if the element is in view, False otherwise.
    """
    element_location = element.location_once_scrolled_into_view
    viewport_height = driver.execute_script("return window.innerHeight")
    element_y = element_location['y']

    return 0 <= element_y <= viewport_height

# # Example usage:
# # Assuming `driver` is your WebDriver instance and you've already navigated to the page
# # driver = ... (initialize your WebDriver here)
# visible_xpaths = get_visible_elements_xpaths(driver)
# print("Visible XPaths:", visible_xpaths)





def find_and_scroll_to_element(driver, xpath, timeout=10):
    """
    Checks if an element specified by XPath is present on the page, 
    and scrolls to move it into view if it is found.

    :param driver: The WebDriver instance.
    :param xpath: The XPath of the element to find.
    :param timeout: Time to wait for the element to be found.
    :return: True if the element is found and scrolled into view, False otherwise.
    """
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        print(f"Element found: {element.get_attribute('outerHTML')}")

        # Scroll the element into view
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
        print("Element scrolled into view.")
        return True

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Element not found: {str(e)}")
        return False

# Example usage:
# Assuming `driver` is your WebDriver instance and you've already navigated to the page
# driver = ... (initialize your WebDriver here)
# xpath = "your_xpath_here"
# find_and_scroll_to_element(driver, xpath)





# # Example usage:
# # Assuming `driver` is your WebDriver instance and you've already navigated to the page
# # driver = ... (initialize your WebDriver here)
# # scroll_through(driver, 2)  # Scroll for 2 minutes


# /html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/article[5]/shreddit-post
# /html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/article[6]/shreddit-post
# /html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/article[8]/shreddit-post
# /html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/article[12]/shreddit-post
# /html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/shreddit-ad-post[1]
# /html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/shreddit-ad-post[2]
# /html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/shreddit-ad-post[1]

# XPath
# //*[@id="t3_1e86emb"]//div[2]/span/span/button[1]
# //*[@id="t3_1e7s20i"]//div[2]/span/span/button[1]
# //*[@id="t3_1e6ymrz"]//div[2]/span/span/button[1]
# //*[@id="t3_1e6h4az"]//div[2]/span/span/button[1]
# //*[@id="in-feed-ad"]/div[2]/span/span/button[1]
# //*[@id="in-feed-ad"]/div[2]/span/span/button[1]


# CSS Selector
# div.flex.flex-row.items-center.flex-nowrap.overflow-hidden.justify-start > span > span > button.group.button.flex.justify-center.aspect-square.p-0.border-0.button-secondary.disabled\:text-interactive-content-disabled.button-plain.inline-flex.items-center.hover\:text-action-upvote.focus-visible\:text-action-upvote
# div.flex.flex-row.items-center.flex-nowrap.overflow-hidden.justify-start > span > span > button.group.button.flex.justify-center.aspect-square.p-0.border-0.button-secondary.disabled\:text-interactive-content-disabled.button-plain.inline-flex.items-center.hover\:text-action-upvote.focus-visible\:text-action-upvote
# div > div > span > span > button.group.button.flex.justify-center.aspect-square.p-0.border-0.button-secondary.disabled\:text-interactive-content-disabled.button-plain.inline-flex.items-center.hover\:text-action-upvote.focus-visible\:text-action-upvote
# div.flex.flex-row.items-center.flex-nowrap.overflow-hidden.justify-start > span > span > button.group.button.flex.justify-center.aspect-square.p-0.border-0.button-secondary.disabled\:text-interactive-content-disabled.button-plain.inline-flex.items-center.hover\:text-action-upvote.focus-visible\:text-action-upvote
# div.flex.flex-row.items-center.flex-nowrap.overflow-hidden.justify-start > span > span > button.group.button.flex.justify-center.aspect-square.p-0.border-0.button-secondary.disabled\:text-interactive-content-disabled.button-plain.inline-flex.items-center.hover\:text-action-upvote.focus-visible\:text-action-upvote
# div.flex.flex-row.items-center.flex-nowrap.overflow-hidden.justify-start > span > span > button.group.button.flex.justify-center.aspect-square.p-0.border-0.button-secondary.disabled\:text-interactive-content-disabled.button-plain.inline-flex.items-center.hover\:text-action-upvote.focus-visible\:text-action-upvote
# div.flex.flex-row.items-center.flex-nowrap.overflow-hidden.justify-start > span > span > button.group.button.flex.justify-center.aspect-square.p-0.border-0.button-secondary.disabled\:text-interactive-content-disabled.button-plain.inline-flex.items-center.hover\:text-action-upvote.focus-visible\:text-action-upvote
# div.flex.flex-row.items-center.flex-nowrap.overflow-hidden.justify-start > span > span > button.group.button.flex.justify-center.aspect-square.p-0.border-0.button-secondary.disabled\:text-interactive-content-disabled.button-plain.inline-flex.items-center.hover\:text-action-upvote.focus-visible\:text-action-upvote

# Outer HTML
# <button rpl="" aria-pressed="false" class=" group button flex justify-center aspect-square p-0 border-0 button-secondary disabled:text-interactive-content-disabled button-plain  inline-flex items-center hover:text-action-upvote focus-visible:text-action-upvote" style="height: var(--size-button-sm-h);" upvote=""> <!--?lit$482268974$--><span class="flex mx-xs text-16"> <!--?lit$482268974$--><svg rpl="" fill="currentColor" height="16" icon-name="upvote-outline" viewBox="0 0 20 20" width="16" xmlns="http://www.w3.org/2000/svg"> <!--?lit$482268974$--><!--?lit$482268974$--><path d="M12.877 19H7.123A1.125 1.125 0 0 1 6 17.877V11H2.126a1.114 1.114 0 0 1-1.007-.7 1.249 1.249 0 0 1 .171-1.343L9.166.368a1.128 1.128 0 0 1 1.668.004l7.872 8.581a1.25 1.25 0 0 1 .176 1.348 1.113 1.113 0 0 1-1.005.7H14v6.877A1.125 1.125 0 0 1 12.877 19ZM7.25 17.75h5.5v-8h4.934L10 1.31 2.258 9.75H7.25v8ZM2.227 9.784l-.012.016c.01-.006.014-.01.012-.016Z"></path><!--?--> </svg> </span> <!--?lit$482268974$--><faceplate-screen-reader-content> <!--?lit$482268974$-->Upvote </faceplate-screen-reader-content><!--?--> </button>
# <button rpl="" aria-pressed="false" class=" group button flex justify-center aspect-square p-0 border-0 button-secondary disabled:text-interactive-content-disabled button-plain  inline-flex items-center hover:text-action-upvote focus-visible:text-action-upvote" style="height: var(--size-button-sm-h);" upvote=""> <!--?lit$482268974$--><span class="flex mx-xs text-16"> <!--?lit$482268974$--><svg rpl="" fill="currentColor" height="16" icon-name="upvote-outline" viewBox="0 0 20 20" width="16" xmlns="http://www.w3.org/2000/svg"> <!--?lit$482268974$--><!--?lit$482268974$--><path d="M12.877 19H7.123A1.125 1.125 0 0 1 6 17.877V11H2.126a1.114 1.114 0 0 1-1.007-.7 1.249 1.249 0 0 1 .171-1.343L9.166.368a1.128 1.128 0 0 1 1.668.004l7.872 8.581a1.25 1.25 0 0 1 .176 1.348 1.113 1.113 0 0 1-1.005.7H14v6.877A1.125 1.125 0 0 1 12.877 19ZM7.25 17.75h5.5v-8h4.934L10 1.31 2.258 9.75H7.25v8ZM2.227 9.784l-.012.016c.01-.006.014-.01.012-.016Z"></path><!--?--> </svg> </span> <!--?lit$482268974$--><faceplate-screen-reader-content> <!--?lit$482268974$-->Upvote </faceplate-screen-reader-content><!--?--> </button>

# Element
# <button rpl="" aria-pressed="false" class=" group button flex justify-center aspect-square p-0 border-0 button-secondary disabled:text-interactive-content-disabled button-plain  inline-flex items-center hover:text-action-upvote focus-visible:text-action-upvote" style="height: var(--size-button-sm-h);" upvote=""> <!--?lit$482268974$--><span class="flex mx-xs text-16"> <!--?lit$482268974$--><svg rpl="" fill="currentColor" height="16" icon-name="upvote-outline" viewBox="0 0 20 20" width="16" xmlns="http://www.w3.org/2000/svg"> <!--?lit$482268974$--><!--?lit$482268974$--><path d="M12.877 19H7.123A1.125 1.125 0 0 1 6 17.877V11H2.126a1.114 1.114 0 0 1-1.007-.7 1.249 1.249 0 0 1 .171-1.343L9.166.368a1.128 1.128 0 0 1 1.668.004l7.872 8.581a1.25 1.25 0 0 1 .176 1.348 1.113 1.113 0 0 1-1.005.7H14v6.877A1.125 1.125 0 0 1 12.877 19ZM7.25 17.75h5.5v-8h4.934L10 1.31 2.258 9.75H7.25v8ZM2.227 9.784l-.012.016c.01-.006.014-.01.012-.016Z"></path><!--?--> </svg> </span> <!--?lit$482268974$--><faceplate-screen-reader-content> <!--?lit$482268974$-->Upvote </faceplate-screen-reader-content><!--?--> </button>
# <button rpl="" aria-pressed="false" class=" group button flex justify-center aspect-square p-0 border-0 button-secondary disabled:text-interactive-content-disabled button-plain  inline-flex items-center hover:text-action-upvote focus-visible:text-action-upvote" style="height: var(--size-button-sm-h);" upvote=""> <!--?lit$482268974$--><span class="flex mx-xs text-16"> <!--?lit$482268974$--><svg rpl="" fill="currentColor" height="16" icon-name="upvote-outline" viewBox="0 0 20 20" width="16" xmlns="http://www.w3.org/2000/svg"> <!--?lit$482268974$--><!--?lit$482268974$--><path d="M12.877 19H7.123A1.125 1.125 0 0 1 6 17.877V11H2.126a1.114 1.114 0 0 1-1.007-.7 1.249 1.249 0 0 1 .171-1.343L9.166.368a1.128 1.128 0 0 1 1.668.004l7.872 8.581a1.25 1.25 0 0 1 .176 1.348 1.113 1.113 0 0 1-1.005.7H14v6.877A1.125 1.125 0 0 1 12.877 19ZM7.25 17.75h5.5v-8h4.934L10 1.31 2.258 9.75H7.25v8ZM2.227 9.784l-.012.016c.01-.006.014-.01.012-.016Z"></path><!--?--> </svg> </span> <!--?lit$482268974$--><faceplate-screen-reader-content> <!--?lit$482268974$-->Upvote </faceplate-screen-reader-content><!--?--> </button>











# Comments:

# XPath to button:
# //*[@id="comment-tree"]/shreddit-comment[1]/shreddit-comment-action-row//div/div/div[1]/span/button[1]
# //*[@id="comment-tree"]/shreddit-comment[2]/shreddit-comment-action-row//div/div/div[1]/span/button[1]


# XPath to shadow_root:
# /html/body/shreddit-app/div/div[1]/div/main/div/report-flow-provider/faceplate-batch/shreddit-comment-tree/shreddit-comment[1]/shreddit-comment-action-row
# /html/body/shreddit-app/div/div[1]/div/main/div/report-flow-provider/faceplate-batch/shreddit-comment-tree/shreddit-comment[2]/shreddit-comment-action-row