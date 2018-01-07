class BillingController < ApplicationController

	def yearly_bill
		#Getting input informations
		providers = params["providers"]
		users = params["users"]
		contracts = params["contracts"]
		contract_modifications = params["contract_modifications"]
		
		#Creating hashed dictionnaries to ease the information processing
		bills = Array.new
		user_consumption = {}
		provider_ppkwh = {}
		contract_id = {}
		#Linking User id and yearly consumption
		for user in users
			user_consumption[user["id"].to_s] = user["yearly_consumption"]
		end
		#Linking provider ID and ppkwh
		for provider in providers
			provider_ppkwh[provider["id"].to_s] = provider["price_per_kwh"]
		end
		#Linking contract ID and the position in contracts array
		#This will be useful is we modify contracts
		id=0
		for contract in contracts
			contract_id[contract["id"].to_s]=id
			id+=1
		end
		#Handling contract modification
		for contract_modification in contract_modifications
			contract = contracts[contract_id[contract_modification["contract_id"].to_s]]
			#If we have a start date, then it's a new contract
			if contract_modification["start_date"] != nil
				contracts.push(contract.clone)
				contract_id[contract["id"].to_s]=id
				contract = contracts[id]
				contract["cancellation"] = false
				contract["start_date"] = contract_modification["start_date"]
				id+=1
			#Otherwise it's a contract cancellation
			else
				contract["cancellation"] = true
			end
			
			#We assume that the new contract is the same than the previous one, unless the field is present in contract modification
			if contract_modification["end_date"] != nil
				contract["end_date"] = contract_modification["end_date"]
			end
			if contract_modification["green"] != nil
				contract["green"] = contract_modification["green"]
			end
			if contract_modification["provider_id"] != nil
				contract["provider_id"] = contract_modification["provider_id"]
			end
		end
		
		id = 1
		#For every contract we process the price
		for contract in contracts
			#Gathering basic data for the contract
			daily_consumption = user_consumption[contract["user_id"].to_s].to_f / 365
			ppkwh = provider_ppkwh[contract["provider_id"].to_s].to_f
			
			#Calculating how much time is spent in every season
			start_date = Date.strptime(contract["start_date"], '%Y-%m-%d').to_time.to_i
			end_date = Date.strptime(contract["end_date"], '%Y-%m-%d').to_time.to_i
			temp_date = start_date
			spring_time = 0
			summer_time = 0
			fall_time = 0
			winter_time = 0
			#For every day we add time for the according season
			while temp_date < end_date
				month = Time.at(temp_date).strftime("%m").to_i
				if month >=3 and month <6
					spring_time += 1
				elsif month >=6 and month<9
					summer_time += 1
				elsif month >=9 and month<12
					fall_time += 1
				else
					winter_time +=1
				end
				temp_date += 60*60*24
			end
			
			#Calculating fall consumption
			if spring_time + summer_time != 0
				fall_consumption = 1.007 * ( spring_time*1.01 + summer_time * 0.985) / (spring_time + summer_time)
			else
				fall_consumption = 1.007
			end
			#Calculating overall consumption
			#NB: The output doesn't match what is expected. maybe there's a misunderstanding on the calculation method
			consumption = daily_consumption * (winter_time + spring_time*1.01 + summer_time * 0.985 + fall_time*fall_consumption)
			
			
			#Calculating the discount
			contract_length = (end_date-start_date) / (60*60*24*365)
			if contract_length <= 1
				discount = 0.9
			elsif contract_length <= 3
				discount = 0.8
			else
				discount = 0.75
			end
			
			#Overall price
			price = consumption * ppkwh * discount * contract_length.to_f
			
			#Adding a discount if the contract is green
			if contract["green"]
				price -= 0.05 * consumption
			end
			
			#Calculating insurance/provider/selectra fee
			insurance_fee = 0.05 * contract_length * 365
			provider_fee = price - insurance_fee
			#Adding malus for cancellation
			if contract["cancellation"]
				provider_fee += 50
			end
			selectra_fee = provider_fee * 0.125
			
			bills.push({
				"commission": {
					"insurance_fee": insurance_fee.round(2),
					"provider_fee": provider_fee.round(2),
					"selectra_fee": selectra_fee.round(2)
				},
				"id": id,
				"price": price.round(2),
				"user_id": contract["user_id"]
			})
			id+=1
		end
		
		#Sending the bills
		json_response({'bills': bills})
	end

	private
	#rendering a json object
	def json_response(object, status = :ok)
		render json: object, status: status
	end
end
