#!/usr/bin/env python3

from datetime import date
import requests
import sys
import csv
import validators

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

def assign_webhook(customer_api_key, domain, webhook, customer_url):
    endpoint = "https://api.mailgun.net/v3/domains/" + domain + "/webhooks"
    data = requests.post(endpoint,auth=("api", customer_api_key),params={"id": webhook, "url": customer_url})
    if data.status_code != 200:
        message = "Error Code: " + str(data.status_code) + " - Message: " + data.text
    else:
        message = data.json()['message']
    return message

def main():
    customer_api_key = ""
    customer_url = ""
    webhooks = ["clicked","complained","delivered","opened","permanent_fail","temporary_fail","unsubscribed"]
    today = date.today()
    file_name = "create-webhooks-log-" + str(today) + ".csv"

    #request api key
    while len(customer_api_key) == 0:
        print("This script was written to assign a single endpoint to every webhook for \n\
all domains on a Mailgun account. If this is not what you wish to do, \n\
please type 'exit' at the prompt below. Otherwise, please provide your \n\
Mailgun API key to continue. \n\n")
        customer_api_key = input("What is your Mailgun API key? ")
        if customer_api_key == "exit":
            sys.exit()

    #request URL to receive webhooks
    while len(customer_url) == 0:
        customer_url = input("\n\nWhat the URL of the endpoint you wish to assign? \n\n")
        if customer_url == "exit":
            sys.exit()
        else:
            customer_url_validated = validators.url(customer_url)
        if not customer_url_validated:
            customer_url = ""
            print("\nURL provided does not pass validation. Please try again.")

    #pull all domains on account
    domains_list = [d["name"] for d in get_domains(customer_api_key)]
    #create csv log file and write the header
    log_file = open(file_name, 'w', newline='', encoding='utf-8')
    headeroutput = ["Domain","Webhook","URL","Message"]
    writer = csv.DictWriter(log_file, fieldnames=headeroutput)
    writer.writeheader()

    #loop through the domains creating one of each webhook
    for domain in domains_list:
        for webhook in webhooks:
            #create webhook
            call = assign_webhook(customer_api_key, domain, webhook, customer_url)
            #log attempt
            writer.writerow({'Domain': domain, 'Webhook': webhook, 'URL': customer_url, 'Message': call})

if __name__ == "__main__":
    main()