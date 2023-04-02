#!/usr/bin/env python3

from datetime import date
import requests
import sys
import csv

# grab all the domains on the account
def get_domains(customer_api_key):
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
        domains.extend(items)
        if len(items) == 1000:
            print("Fetching next domain page")
            skip += 1000
            continue
        break
    return domains

def assign_webhook(customer_api_key, domain, webhook):
    endpoint = "https://api.mailgun.net/v3/domains/" + domain + "/webhooks/" + webhook
    data = requests.delete(endpoint,auth=("api", customer_api_key))
    if data.status_code != 200:
        message = "Error communicating with API endpoint. Error Code: " + str(data.status_code) + "Message: " + data.text
    else:
        message = data.json()['message']
    return message

def main():
    customer_api_key = ""
    webhooks = ["clicked","complained","delivered","opened","permanent_fail","temporary_fail","unsubscribed"]
    today = date.today()
    file_name = "delete-webhooks-log-" + str(today) + ".csv"

    #request api key
    while len(customer_api_key) == 0:
        print("This script was written to delete every webhook on your Mailgun \n\
account. If this is not what you wish to do, please type 'exit' at \n\
the prompt below. Otherwise, please provide your Mailgun API key to continue.\n\n")
        customer_api_key = input("What is your Mailgun API key? ")
        if customer_api_key == "exit":
            sys.exit()

    #pull all domains on account
    domains_list = [d["name"] for d in get_domains(customer_api_key)]
    #create csv log file and write the header
    log_file = open(file_name, 'w', newline='', encoding='utf-8')
    headeroutput = ["Domain","Webhook","Message"]
    writer = csv.DictWriter(log_file, fieldnames=headeroutput)
    writer.writeheader()

    #loop through the domains creating one of each webhook
    for domain in domains_list:
        for webhook in webhooks:
            #create webhook
            call = assign_webhook(customer_api_key, domain, webhook)
            #log attempt
            writer.writerow({'Domain': domain, 'Webhook': webhook, 'Message': call})

if __name__ == "__main__":
    main()