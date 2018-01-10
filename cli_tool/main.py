# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:55:45 2018

@author: Guillaume Caillaud
"""
import os
try:
    import requests
except:
    print("ERROR: Could not import requests module. Please add requests with pip install")
    os.system("pause")
    os._exit
import json

class cli_tool:
    #Information for where data is located
    stored_data = 'data/data.json'
    api_url = "http://localhost:3000/"
    data = {}
    
    #Main function
    def __init__(self):
        self.get_data()
        print("Welcome to Selectra CLI Tool")
        print("This tool enables you to access and edit billing data")
        print("Type Ctrl+C to close the tool")
        while True:
            print("Enter the following codes to:")
            print("1 - See customers list")
            print("2 - See providers list")
            print("3 - See contracts list")
            print("10 - See billing information")
            print("21 - Edit customers info")
            print("22 - Edit providers info")
            print("23 - Edit contracts info")
            print("31 - Add customer")
            print("32 - Add provider")
            print("33 - Add contract")
            print("40 - Modify a contract")
            try:
                action = int(input(''))
                #Processing input -1 lets the user exit the program
                if action == -1:
                    break
                elif action == 1:
                    self.get_users()
                elif action == 2:
                    self.get_providers()
                elif action == 3:
                    self.get_contracts()
                    #print(self.data["contracts"])
                elif action == 10:
                    print(self.billing())
                elif action == 21:
                    self.set_users()
                elif action == 22:
                    self.set_providers()
                elif action == 23:
                    self.set_contracts()
                elif action == 31:
                    self.add_users()
                elif action == 32:
                    self.add_providers()
                elif action == 33:
                    self.add_contracts()
                elif action == 40:
                    self.modify_contracts()
                else:
                    print("Wrong input, please retry\n")
            except:
                print("Wrong input, please retry\n")
    
    #Retrieving input data from JSON file
    def get_data(self):
        self.data = json.loads(open(self.stored_data, 'rb').read())
    
    #Displaying users data in a table
    def get_users(self):
        users = self.data["users"]
        print(repr("user ID").rjust(8), repr("Yearly Consumption").rjust(20))
        for user in users:
            print(repr(user["id"]).rjust(8), repr(user["yearly_consumption"]).rjust(20))
    
    #Displaying providers data in a table        
    def get_providers(self):
        users = self.data["providers"]
        print(repr("Provider ID").rjust(16), repr("Price per kWh").rjust(15), repr("Cancellation fee?").rjust(20))
        for user in users:
            print(repr(user["id"]).rjust(16), repr(user["price_per_kwh"]).rjust(15), repr(user["cancellation_fee"]).rjust(20))
    
    #Displaying contracts data in a table
    def get_contracts(self):
        users = self.data["contracts"]
        print(repr("Contract ID").rjust(12), repr("User ID").rjust(10), repr("Provider ID").rjust(15), repr("Start date").rjust(15), repr("End date").rjust(15), repr("Green Electricity?").rjust(20))
        for user in users:
            print(repr(user["id"]).rjust(12), repr(user["user_id"]).rjust(10), repr(user["provider_id"]).rjust(15), repr(user["start_date"]).rjust(15), repr(user["end_date"]).rjust(15), repr(user["green"]).rjust(20))
    
    #Writing data in JSON file from class variable
    def write_data(self):
        with open(self.stored_data, 'w') as json_file:
            json.dump(self.data, json_file, indent=2)
    
    #Changing users data
    def set_users(self):
        self.get_data()
        customers = self.data["users"]
        print("Enter customer ID")
        user_id = int(input())
        #Getting user's location in table from its ID
        for i in range(len(customers)):
            if user_id == customers[i]["id"]:
                customer_id = i
                break
        consumption = input("Enter customer yearly consumption [" + str(customers[customer_id]["yearly_consumption"]) + "] (Leave blank if unchanged)")
        
        #Writing new data only if the input isn't empty
        if consumption != "":
            customers[customer_id]["yearly_consumption"] = int(consumption)
            
        #writing data
        self.write_data()
    
    #Changing providers data
    def set_providers(self):
        self.get_data()
        providers = self.data["providers"]
        print("Enter provider ID")
        provider_id = int(input())
        #Getting provider's location in table from its ID
        for i in range(len(providers)):
            if provider_id == providers[i]["id"]:
                id_provider = i
                break
        ppkwh = input("Enter provider price per kwh [" + str(providers[id_provider]["price_per_kwh"]) + "] (Leave blank if unchanged)")
        
        #Writing new data only if the input isn't empty
        if ppkwh != "":
            providers[id_provider]["price_per_kwh"] = float(ppkwh)
            
        cancellation_fee = input("Does the provider applies cancellation fee [" + str(providers[id_provider]["cancellation_fee"]) + "] (Y/N)")
        
        #Processing input as a True/False variable
        if cancellation_fee == "Y" or cancellation_fee == "y":
            providers[id_provider]["cancellation_fee"] = True
        elif cancellation_fee != "":
            providers[id_provider]["cancellation_fee"] = False
        
        self.write_data()
    
    #Changing contracts data
    def set_contracts(self):
        self.get_data()
        contracts = self.data["contracts"]
        print("Enter contract ID")
        #Getting provider's location in table from its ID
        contract_id = int(input())
        for i in range(len(contracts)):
            if contract_id == contracts[i]["id"]:
                id_contract = i
                break
        start_date = input("Enter contract start date [" + str(contracts[id_contract]["start_date"]) + "] (YYYY-MM-DD)")
        
        #Writing new data only if the input isn't empty
        if start_date != "":
            contracts[id_contract]["start_date"] = start_date
            
        end_date = input("Enter contract end date [" + str(contracts[id_contract]["end_date"]) + "] (YYYY-MM-DD)")
        
        #Writing new data only if the input isn't empty
        if end_date != "":
            contracts[id_contract]["end_date"] = end_date
            
        green = input("Is the contract green [" + str(contracts[id_contract]["green"]) + "] (Y/N)")
        
        #Processing input as a True/False variable
        if green == "Y" or green == "y":
            contracts[id_contract]["green"] = True
        elif green != "":
            contracts[id_contract]["green"] = False
            
            
        provider_id = input("Enter the provider ID [" + str(contracts[id_contract]["provider_id"]) + "] (Leave blank if unchanged)")
        
        #Writing new data only if the input isn't empty
        if provider_id != "":
            contracts[id_contract]["provider_id"] = int(provider_id)
        
        user_id = input("Enter the user ID [" + str(contracts[id_contract]["user_id"]) + "] (Leave blank if unchanged)")
        
        #Writing new data only if the input isn't empty
        if user_id != "":
            contracts[id_contract]["user_id"] = int(user_id)
            
        self.write_data()
        
    #Adding a new user   
    def add_users(self):
        self.get_data()
        customers = self.data["users"]
        user = {}
        consumption = input("Enter customer yearly consumption in kWh")
        
        #Assigning a new ID
        user["id"] = len(customers) + 1
        user["yearly_consumption"] = int(consumption)
        
        #Adding the user to the userlist
        customers.append(user)
        
        self.write_data()
       
    #Adding a provider
    def add_providers(self):
        self.get_data()
        providers = self.data["providers"]
        provider = {}
        
        #Assigning a new ID
        provider["id"] = len(providers) + 1
        ppkwh = input("Enter provider price per kWh")
        provider["price_per_kwh"] = float(ppkwh)
            
        cancellation_fee = input("Does the provider applies cancellation fee? (Y/N)")
        
        #Processing data as a True/False variable
        if cancellation_fee == "Y" or cancellation_fee == "y":
            provider["cancellation_fee"] = True
        elif cancellation_fee != "":
            provider["cancellation_fee"] = False
        
        #Adding the provider to the provider list
        providers.append(provider)
        
        self.write_data()
    
    #Adding a contract
    def add_contracts(self):
        self.get_data()
        contracts = self.data["contracts"]
        contract = {}
        
        #Assigning an ID
        contract["id"] = len(contracts) + 1
        
        start_date = input("Enter contract start date (YYYY-MM-DD): ")
        
        if start_date != "":
            contract["start_date"] = start_date
            
        end_date = input("Enter contract end date (YYYY-MM-DD): ")
        
        if end_date != "":
            contract["end_date"] = end_date
            
        green = input("Is the contract green (Y/N)? ")
        
        #Processing data as a True/False variable
        if green == "Y" or green == "y":
            contract["green"] = True
        elif green != "":
            contract["green"] = False
            
            
        provider_id = input("Enter the provider ID: ")
        
        if provider_id != "":
            contract["provider_id"] = int(provider_id)
        
        user_id = input("Enter the user ID: ")
        
        if user_id != "":
            contract["user_id"] = int(user_id)
            
        contracts.append(contract)
            
        self.write_data()
        
    #Adding a contract modification
    def modify_contracts(self):
        self.get_data()
        contracts = self.data["contract_modifications"]
        contract = {}
        
        #Assigning a new ID
        contract["id"] = len(contracts) + 1
        
        contract_id = input("Enter the contract ID: ")
        
        if contract_id != "":
            contract["contract_id"] = int(contract_id)
        
        cancel = input("Do you want to cancel the contract ? (Y/N) ")
        
        #Processing data as a True/False variable
        if cancel == "Y" or cancel == "y":
            cancellation = True
        elif cancel != "":
            cancellation = False
        
        #If the contract is new, we need new information
        if not cancellation:
            start_date = input("When does the contract start ? (YYYY-MM-DD) ")
            contract["start_date"] = start_date
            
            provider_id = input("Enter the provider ID: ")
        
            contract["provider_id"] = int(provider_id)
            
            green = input("Is the contract green (Y/N)? ")
            
            if green == "Y" or green == "y":
                contract["green"] = True
            elif green != "":
                contract["green"] = False
            
        #We need an end date anyway
        end_date = input("Enter contract end date (YYYY-MM-DD): ")
        
        if end_date != "":
            contract["end_date"] = end_date
            
            
        contracts.append(contract)
            
        self.write_data()
    
    #Requesting billing from server
    def billing(self):        
        self.get_data()
        r = requests.get(self.api_url, json=self.data)
        return r.json()
                
cli_tool()