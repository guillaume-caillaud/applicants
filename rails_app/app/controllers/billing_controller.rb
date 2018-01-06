class BillingController < ApplicationController

	def yearly_bill
		
		providers = params["providers"]
		users = params["users"]
		contracts = params["contracts"]
		contract_modifications = params["contract_modifications"]
		
		bills = Array.new
		user_consumption = {}
		provider_ppkwh = {}
		contract_id = {}
		for user in users
			user_consumption[user["id"].to_s] = user["yearly_consumption"]
		end
		for provider in providers
			provider_ppkwh[provider["id"].to_s] = provider["price_per_kwh"]
		end
		id=0
		for contract in contracts
			contract_id[contract["id"].to_s]=id
			id+=1
		end
		for contract_modification in contract_modifications
			contract = contracts[contract_id[contract_modification["contract_id"].to_s]]
			if contract_modification["start_date"] != nil
				contracts.push(contract.clone)
				contract_id[contract["id"].to_s]=id
				contract = contracts[id]
				contract["cancellation"] = false
				contract["start_date"] = contract_modification["start_date"]
				id+=1
			else
				contract["cancellation"] = true
			end
			
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
		for contract in contracts
			consumption = user_consumption[contract["user_id"].to_s].to_f
			ppkwh = provider_ppkwh[contract["provider_id"].to_s].to_f
			
			start_date = Date.strptime(contract["start_date"], '%Y-%m-%d').to_time.to_i
			end_date = Date.strptime(contract["end_date"], '%Y-%m-%d').to_time.to_i
			contract_length = (end_date-start_date) / (60*60*24*365)
			
			if contract_length <= 1
				discount = 0.9
			elsif contract_length <= 3
				discount = 0.8
			else
				discount = 0.75
			end
			
			
			price = consumption * ppkwh * discount * contract_length.to_f
			
			if contract["green"]
				price -= 0.05 * consumption
			end
			
			insurance_fee = 0.05 * contract_length * 365
			provider_fee = price - insurance_fee
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
		
		json_response({'bills': bills})
	end

	private

	def json_response(object, status = :ok)
		render json: object, status: status
	end
end
