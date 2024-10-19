from uagents import Agent, Context
from pydantic import BaseModel
import ssl
import certifi
import requests
headers = {
    'Authorization': 'Bearer <your token here>',
    'Content-Type': 'application/json'
}
response = requests.get('https://agentverse.ai/v1/almanac/recent', headers=headers)
print(response.json())

ssl_context = ssl.create_default_context(cafile=certifi.where())

# Define the Pydantic model for the energy request message
class EnergyRequest(BaseModel):
    units: int

# Define the Pydantic model for the energy offer message
class EnergyOffer(BaseModel):
    units: int
    price: float

# Create the Producer agent with a fixed seed and specify the endpoint
producer = Agent(
    name="producer_agent",
    seed="producer seed phrase",
    endpoint="http://localhost:8001"  # Specify an endpoint for the producer agent
)

# Available energy units
available_energy = 100

# Handle energy requests from the consumer
@producer.on_message(model=EnergyRequest)
async def handle_energy_request(ctx: Context, message: EnergyRequest):
    global available_energy
    requested_units = message.units
    
    if requested_units <= available_energy:
        available_energy -= requested_units
        # Send an energy offer back to the consumer using the EnergyOffer model
        await ctx.send(message.get("from"), EnergyOffer(units=requested_units, price=requested_units * 0.05))
        ctx.logger.info(f"Offered {requested_units} units of energy.")
    else:
        ctx.logger.info("Not enough energy available.")

if __name__ == "__main__":
    producer.run()

class EnergyCounterOffer(BaseModel):
    new_price: float

'''
@producer.on_message(model=EnergyCounterOffer)
async def handle_counter_offer(ctx: Context, message: EnergyCounterOffer):
    if message.new_price >= MINIMUM_ACCEPTABLE_PRICE:
        ctx.logger.info(f"Counter offer accepted with new price: {message.new_price}")
        await ctx.send(message.get("from"), "Accepted")
    else:
        ctx.logger.info(f"Counter offer rejected, price too low: {message.new_price}")
        await ctx.send(message.get("from"), "Rejected")
'''