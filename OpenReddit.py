from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
import requests

def open_reddit_with_multilogin(mla_profile_id):
    """
    Opens Reddit using a specified Multilogin profile and returns the WebDriver instance for further operations.

    :param mla_profile_id: The ID of the Multilogin profile to use.
    :return: WebDriver instance if successful, None otherwise.
    """
    # Multilogin API URL to start the profile
    mla_url = f'http://127.0.0.1:35000/api/v1/profile/start?automation=true&profileId={mla_profile_id}'

    try:
        # Send GET request to start the browser profile by profileId
        resp = requests.get(mla_url)
        resp.raise_for_status()  # Raise an exception for HTTP errors

        json_response = resp.json()
        print(json_response)

        if 'value' not in json_response:
            raise ValueError("Invalid response: 'value' key not found in JSON response")

        # Instantiate the Remote Web Driver to connect to the browser profile launched by previous GET request
        command_executor = json_response['value']
        driver = webdriver.Remote(command_executor=command_executor, options=ChromiumOptions())

        # Perform automation
        target_url = 'https://www.reddit.com/'  # Change this to the desired website
        driver.get(target_url)
        print(f"Page title: {driver.title}")

        return driver  # Return the WebDriver instance for further operations

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        if 'driver' in locals():
            try:
                driver.quit()
            except Exception:
                pass
        return None

# Example usage:
# driver = open_reddit_with_multilogin('48e099f8-2c74-4c41-beb1-b85da0f70f57')
# Perform further operations with the `driver` instance
