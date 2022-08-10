#!/usr/bin/env python3

from xml import dom
import requests
import sys
import os
import csv
from datetime import date

def get_options():
    suppression_list = []
    #build the menu
    suppressions_menu = {"1":"Bounces","2":"Complaints","3":"Unsubscribes","4":"All the above"}
    for entry in suppressions_menu:
        print( '['+ entry + ']', suppressions_menu[entry])
    selection=input("Which suppression list do you wish to export? ")
    if selection == '1':
        suppression_list.append('bounces')
        return suppression_list
    elif selection == '2':
        suppression_list.append('complaints')
        return suppression_list
    elif selection == '3':
        suppression_list.append('unsubscribes')
        return suppression_list
    elif selection == '4':
        suppression_list.append('bounces')
        suppression_list.append('complaints')
        suppression_list.append('unsubscribes')
        return suppression_list
    else:
        print("Unknown Option Selected. Exiting script")
        sys.exit()

#Define function to make sure user inputed domain exists
def verify_domain(domain_name,customer_api_key):
    data = requests.get( "https://api.mailgun.net/v3/domains/" + domain_name, auth=("api", customer_api_key))
    if data.status_code == 200:
        # Domain exists
        return True
    elif data.status_code == 404:
        # Domain does not exist
        print("Domain " + domain_name + " was not found: ")
        return False
    else:
        # Any other error
        print("Error communicating with API endpoint when attempting to verify domain. Error Code: {} - {}".format(data.status_code, data.text))
        sys.exit()

# creates the files and directory
def create_file(name):
    file_directory = f'{os.path.dirname(os.path.realpath(__file__))}/files/suppressions'
    if not os.path.exists(file_directory):
        print('Creating directory, "files\suppressions"\n')
        os.makedirs(file_directory)
    file_name = os.path.join(file_directory, f'{name}.csv')
    return file_name

def get_suppressions(domain_name,stype,customer_api_key):
    skip = 0
    #loop through suppression types
    while True:
        print("Now checking " + stype + " on domain " + domain_name)
        data = requests.get("https://api.mailgun.net/v3/" + domain_name + "/" + stype,
                            auth=("api", customer_api_key),
                            params={"skip": skip, "limit": 1000})

        if data.status_code != 200:
            print("Error communicating with API endpoint. Error Code: {}".format(data.status_code))
            sys.exit()
        logs = data.json()
        llogs = len(logs['items'])
        if logs['items'] and skip == 0: # if there are suppressions create a file and write header
            file_name = create_file(domain_name + '_' + stype)
            sfile = open(file_name, 'w', newline='', encoding='utf-8')
            headeroutput = ["address","code","error","created_at","MessageHash"]
            writer = csv.DictWriter(sfile, fieldnames=headeroutput)
            writer.writeheader()
        elif logs['items'] and skip != 0:
            for rows in logs['items']:
                writer.writerow(rows)
        elif llogs == 0:
            print(domain_name + " has no " + stype)
            return
        if llogs == 1000:
            print("Fetching next page of suppressions")
            skip += 1000
            continue

        sfile.close()
        break
        return

def main():
    customer_api_key = ""
    domain_name = ""
    today = date.today()
    file_name = "suppressions-" + str(today)

    while len(customer_api_key) == 0:
        #instructions
        print("This script was written to export a domain's suppression list(s) to a csv \n \
file. You will be asked to provide the the list domains in a csv file as \n \
well as your Mailgun API key. The output will be in the \n \
`./files/suppressions/` folder. \n")
        customer_api_key = input("What is your Mailgun API key? ")

        if customer_api_key == "exit":
            sys.exit()

    while len(domain_name) == 0:
        domain_name = input("Name of file with domains ")
        try:
            f = open(domain_name, 'r', encoding="utf-8")
        except FileNotFoundError:
            if domain_name == "exit":
                sys.exit()
            print("The file you specified cannot be found. Please try again.")
            domain_name = ""

    options = get_options()

    for line in f: #grab domain from file
        domain_name = str(line).rstrip() #removes any trailing new lines
        if verify_domain(domain_name, customer_api_key): #verify domain exists
            for stype in options: #grab suppression type
                get_suppressions(domain_name, stype, customer_api_key) #use the above domain and stype
                print("Finished with " + stype + " on " + domain_name)
        print("Finished with " + domain_name)
    print("Script completed.")

if __name__ == "__main__":
    main()