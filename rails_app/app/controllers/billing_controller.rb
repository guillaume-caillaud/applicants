class BillingController < ApplicationController

	def yearly_bill
		
		providers = params["providers"]
		users = params["users"]
		
		bills = Array.new
		id = 1
		for user in users
			consumption = user["yearly_consumption"].to_f
			
			for provider in providers
				if provider["id"] == user["provider_id"]
					ppkwh = provider["price_per_kwh"].to_f
				end
			end
			
			price = consumption * ppkwh
			bills.push({
				"id": id,
				"price": price.to_i,
				"user_id": user["id"]
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
