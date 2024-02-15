#!/usr/bin/env python3

from datetime import date
from time import sleep
import requests
import sys
import os


# grab all the unverified domains on the account
def get_domains(customer_api_key):
    skip = 0
    domains = []
    while True:
        data = requests.get("https://api.mailgun.net/v4/domains",
                            auth=("api", customer_api_key),
                            params={"skip": skip, "limit": 1000, "state": "unverified"})
        if data.status_code != 200:
            print("Error communicating with API endpoint. Error Code: {} - {} \n URL: {}"
                  .format(data.status_code, data.text, data.url))
            sys.exit()
        total = data.json()['total_count']
        if total == 0:
            print("All the domains on this account are already in verified status.")
            sys.exit()
        else:
            print("Total Unverifed Domains on Account: " + str(total))
            items = data.json()['items']
            domains_list = [d["name"] for d in items]
            # Attempt to verify the specified domain
            for domain in domains_list:
                print("\n starting verification for " + domain)
                verify = requests.put("https://api.mailgun.net/v4/domains/" + domain + "/verify",
                                auth=("api", customer_api_key))
                # A slight limiter to keep from hitting the API too quickly 
                sleep(.25)
            domains.extend(items)
            if len(items) == 1000:
                print("Fetching next domain page")
                skip += 1000
                continue
            break
        
    return domains


def main():
    customer_api_key = ""
    today = date.today()
    file_name = "domains-" + str(today)

    while len(customer_api_key) == 0:
        #instructions
        print ("This script was written to start the verification process for any unverified domains on your account.\nPlease provide your Mailgun API key to continue. Type 'exit' if you wish to quit.\n")
        customer_api_key = input("What is your Mailgun API key? ")

        if customer_api_key == "exit":
            sys.exit()

    domains = get_domains(customer_api_key)
    print("The verification process has been triggered for all the above domains. This can take a few minutes for each domain. Please do not run this script back to back.")
if __name__ == "__main__":
    main()
