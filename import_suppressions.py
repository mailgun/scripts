# this script was written to import suppressions via file. 

# this currently accepts a json file containing properly formatted suppressions

# a csv file will also be required to identify the domains for import. no column names needed in csv

# jeremy pockey made this 


import requests
import json
import sys
import csv


# verifies domains
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

def main(headers = {'Content-Type': 'application/json'}):
    customer_api_key = ""
    customer_csv = ""
    file_name = ""
    # headers = {'Content-Type': 'application/json'}

    def import_suppressions(customer_api_key, stype, domain_name):
        data = requests.post("https://api.mailgun.net/v3/"+ domain_name + "/"+ stype,
                auth=("api", customer_api_key),
                data = (file_name), 
                headers = headers
        )
        if data.status_code == 200:
            print(f"{data.status_code} - Successful import!")
        else:
            print(f"Suppression not imported! {data.status_code}")


    # collects customer api key        
    while len(customer_api_key) == 0:
        customer_api_key = input("Please enter your API key: ")
    
    # collects domains for suppressions to be imported into
    while len(customer_csv) == 0:
        customer_csv = input("Please enter the name of the csv file containing your domains: ")

    # collects file with recipients to be imported
    while len(file_name) == 0:
        file_name = input("Please enter the name of the file you are importing: ")  

    if file_name.split(".")[1] == "json":
        print("Ok!")
        # sets the content type for json file
        # headers = {'Content-Type': 'application/json'}
        # opens json file
        with open(file_name, 'r') as handle:
            parsed = json.load(handle)
            # formats json
            file_name = json.dumps(parsed, indent=2)

    # sets the suppression type
    suppressions_menu = {"1":"Bounces","2":"Complaints","3":"Unsubscribes"}
    print(suppressions_menu)
    selection=input("Which suppressions are we importing? ")

    if selection == '1':
        stype = "bounces"
    elif selection == '2':
        stype = "complaints"
    elif selection == '3':
        stype = "unsubscribes"
    # if an invalid entry was returned, exits script
    else:
        print("Unknown Option Selected. Exiting script")
        sys.exit()
    
    # opens csv file containing domains 
    with open(customer_csv) as csv_file:
        domains = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for list in csv_reader:
            for line in list:
                    domain_name = line.replace("['", "")
                    if verify_domain(domain_name,customer_api_key):
                        domains.append(domain_name)
        for item in domains:
            domain_name = item
            import_suppressions(customer_api_key, stype, domain_name)
    
if __name__ == "__main__":
    main()
