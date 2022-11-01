import os
import requests
import csv
from getpass import getpass

def display_menu():

    options = {
        "0" : "proceed with no parameters",
        "1" : "add a start date",
        "2" : "add an end date",
        "3" : "add event type",
        "4" : "add a specific recipient",
    }
    
    for option in options:
        print(f"[{option}] {options[option]}")

def add_params(request_params, param_choice):
    if param_choice == 0:
        return request_params
    elif param_choice == 1:
        begin_date = input("Enter the start date (ex: Thu, 13 Oct 2011 18:02:00 +0000 or 1318546920): ")
        request_params.update({"begin":f"{begin_date}"})
    elif param_choice == 2:
        end_date = input("Enter the end date (ex: Thu, 13 Oct 2011 18:02:00 +0000 or 1318546920): ")
        request_params.update({"end":f"{end_date}"})
    elif param_choice == 3:
        event = input("Enter the event(s) you wish to poll: ")
        request_params.update({"event":f"{event}"})
    elif param_choice == 4:
        recipient = input("Enter the recipeint: ")
        request_params.update({"recipient":f"{recipient}"})
    
    return request_params

def confirm_params(params):
    resp = input("Add more parameters? (Y/N): ").upper()
    while True:
        if resp == 'Y':
            param_choice = input("Enter the paramter you wish to add: ")
            params = add_params(params, param_choice)
            resp = input("Do you want to add more parameters? (Y/N): ").upper()
            
        elif resp == 'N':
            break
        else:
            resp = input("Please enter a valid input (Y/N): ").upper()
    
def create_file():
    name = input("Enter name of the file: ")
    file_directory = f'{os.path.dirname(os.path.realpath(__file__))}'
 
    while os.path.exists(name):
        name = input("File already Exists in directory. Please enter a diferent name: ")

    file_name = os.path.join(file_directory, name)
    return file_name

def write_to_file(file_name, event):
    with open(file_name, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([event])

def get_events(key, url, r_params):
    return requests.get(
            url,
            auth=("api", key),
            params=r_params)

def main():
    csv_file = create_file()
    api_key = getpass(prompt = "Enter your API Key: ")
    region = input("Enter the region your domain is located in: ").upper()
    domain = input("Enter your domain: ")

    if region == "US":
        url = f"https://api.mailgun.net/v3/{domain}/events"
    elif region == "EU":
        url = f"https://api.eu.mailgun.net/v3/{domain}/events"
    
    display_menu()
    
    param_choice = int(input("Enter the paramter you wish to add: "))
    while param_choice > 4:
        display_menu()
        param_choice = int(input("Please enter a valid input: "))
    
    params = add_params({"limit" : 300}, param_choice)

    if param_choice != 0: 
        confirm_params(params)
    
    response = get_events(api_key, url, params)
    
    if response.status_code == 200:
        resp = response.json()
        while len(resp['items']):
            for i in range (len(resp["items"])):
                write_to_file(csv_file, resp["items"][i])
            next_url = resp['paging']['next']
            resp = get_events(api_key, next_url, params).json()
    else:
        print(f"Error: {response.status_code}, closing program")

    print(f"Saved in {csv_file}")
        
if __name__ == "__main__":
    main()