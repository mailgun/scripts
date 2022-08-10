#!/usr/bin/env python3

from datetime import date
import requests
import sys
import os

# creates the file and directory for logging everything
def create_file(name):
    file_directory = f'{os.path.dirname(os.path.realpath(__file__))}/files'
    if not os.path.exists(file_directory):
        print('Creating directory: "files"\n')
        os.makedirs(file_directory)
    print('Creating file: ' + name + '\n')
    file_name = os.path.join(file_directory, f'{name}.csv')
    f = open(file_name, 'w')
    f.write("DOMAIN")
    return f


# grab all the domains on the account
def get_domains(customer_api_key, f):
    skip = 0
    domains = []
    while True:
        data = requests.get("https://api.mailgun.net/v3/domains",
                            auth=("api", customer_api_key),
                            params={"skip": skip, "limit": 1000})
        if data.status_code != 200:
            print("Error communicating with API endpoint. Error Code: {} - {}"
                  .format(data.status_code, data.text))
            sys.exit()
        items = data.json()['items']
        domains_list = [d["name"] for d in items]
        for domain in domains_list:
            f.write('\n' + domain)
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
        print ("This script was written to export a list of all domains on a Mailgun account to a csv file.\nPlease provide your Mailgun API key to continue. Type 'exit' if you wish to quit.\n")
        customer_api_key = input("What is your Mailgun API key? ")

        if customer_api_key == "exit":
            sys.exit()

    f = create_file(file_name)
    domains = get_domains(customer_api_key,f)

if __name__ == "__main__":
    main()
