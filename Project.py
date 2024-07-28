# Project.py
import gspread
from google.oauth2.service_account import Credentials
from OpenReddit import open_reddit_with_multilogin
from SearchReddit import search_reddit
from OpenResult import open_random_search_result
from OpenCommunities import open_communities
from ScrollThrough import scroll_through
import streamlit as st
from time import sleep
import urllib3
from requests.exceptions import ConnectionError

def main(search_terms):
    # Define the Multilogin profile ID and search terms
    mla_profile_ids = [
        '2a368372-35c1-4d26-9d31-84732c68b2e9',
        'ecf09171-5112-4f33-8d96-3fdee87d6847',
        '82ca5599-fcdc-4085-9ad0-2470ce3de5c0',
        '73491d72-0a22-4016-a3ea-38b2d9257e44'
    ]
    mla_profile_names = [
        'Steven3369Ij', 'MajorSmall2966', 'Jeff1735Uv', 'David5803Oc'
    ]

    # Get credentials from Streamlit secrets
    credentials_dict = {
        "type": st.secrets["googleapi"]["type"],
        "project_id": st.secrets["googleapi"]["project_id"],
        "private_key_id": st.secrets["googleapi"]["private_key_id"],
        "private_key": st.secrets["googleapi"]["private_key"],
        "client_email": st.secrets["googleapi"]["client_email"],
        "client_id": st.secrets["googleapi"]["client_id"],
        "auth_uri": st.secrets["googleapi"]["auth_uri"],
        "token_uri": st.secrets["googleapi"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["googleapi"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["googleapi"]["client_x509_cert_url"]
    }

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "1zRsB81g4n6Br8h6cRlStNPBSSbAVQ24LulhZRq2NpTE"
    sheet = client.open_by_key(sheet_id).worksheet("Script data")
    values_list = sheet.get_all_values()
    column_data = [row[6] for row in values_list[1:] if len(row) > 6]
    search_terms = [item for item in column_data if item]
    print(search_terms)

    failed_profiles = []

    def process_profile(profile_id):
        try:
            driver = open_reddit_with_multilogin(profile_id)
            for k in range(100):
                print(k)
            driver.quit()
            print("Before sleeping")
            sleep(20)
            print("After sleeping")
            return True
        except (ConnectionError, urllib3.exceptions.NewConnectionError) as e:
            print(f"Connection error with profile ID {profile_id}: {e}")
            print("Before sleeping1")
            sleep(20)
            print("After Sleeping1")
            return False
        except Exception as e:
            print(f"An unexpected error occurred with profile ID {profile_id}: {e}")
            return False

    i = 0
    while i < len(mla_profile_ids):
        profile_id = mla_profile_ids[i]
        if not process_profile(profile_id):
            failed_profiles.append(profile_id)
        i += 1

    # Retry failed profiles
    retry_failed = True
    while retry_failed and failed_profiles:
        retry_failed = False
        remaining_profiles = []
        for profile_id in failed_profiles:
            if not process_profile(profile_id):
                remaining_profiles.append(profile_id)
                retry_failed = True
        if len(remaining_profiles) == len(failed_profiles):
            print("All remaining ids failing")
            print(remaining_profiles)
            break
        failed_profiles = remaining_profiles

    return search_terms





# if __name__ == "__main__":
#     main()














# while i<4:
#         try:
#             driver = open_reddit_with_multilogin(mla_profile_ids[i])
#             for k in range(100):
#                 print(k)
#             driver.quit()
#             print("Before sleeping")
#             sleep(20)
#             print("After sleeping")
#             # # quit
#             # if driver:
#             #     # Perform the search
#             #     search_reddit(driver, search_terms)
#             #     # sleep for 5 seconds
#             #     time.sleep(3)
#             #     open_communities(driver)
#             #     time.sleep(5)
#             #     # Open a random search result
#             #     open_random_search_result(driver)
#             #     time.sleep(3)
#             #     scroll_through(driver, 20)
#             #     time.sleep(3)
#             #     driver.quit()
#             #     sleep(2)
#             # else:
#             #     print("Failed to open Reddit with Multilogin profile.")
#         except:
#             # try opening current profile again
#             print("Before sleeping1")
#             sleep(20)
#             print("After Sleeping1")
#             i = i-1
#         i = i+1
