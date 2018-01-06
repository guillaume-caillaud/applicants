class BillingController < ApplicationController

	def yearly_bill
		
		providers = params["providers"]
		users = params["users"]
		contracts = params["contracts"]
		
		bills = Array.new
		user_consumption = {}
		provider_ppkwh = {}
		for user in users
			user_consumption[user["id"].to_s] = user["yearly_consumption"]
		end
		for provider in providers
			provider_ppkwh[provider["id"].to_s] = provider["price_per_kwh"]
		end
		
		
		id = 1
		for contract in contracts
			consumption = user_consumption[contract["user_id"].to_s].to_f
			ppkwh = provider_ppkwh[contract["provider_id"].to_s].to_f
			
			if contract["contract_length"] <= 1
				discount = 0.9
			elsif contract["contract_length"] <= 3
				discount = 0.8
			else
				discount = 0.75
			end
			
			
			price = consumption * ppkwh * discount * contract["contract_length"].to_f
			
			insurance_fee = 0.05 * contract["contract_length"] * 365
			provider_fee = price - insurance_fee
			selectra_fee = provider_fee * 0.125
			
			bills.push({
				"commission": {
					"insurance_fee": insurance_fee.round(2),
					"provider_fee": provider_fee.round(2),
					"selectra_fee": selectra_fee.round(2)
				},
				"id": id,
				"price": price,
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
