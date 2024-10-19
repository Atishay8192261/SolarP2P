from uagents import Agent, Context
from pydantic import BaseModel
import ssl
import certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Define the Pydantic model for the energy request message
class EnergyRequest(BaseModel):
    units: int



# Define the Pydantic model for the energy offer message
class EnergyOffer(BaseModel):
    units: int
    price: float

# Create the Consumer agent with a fixed seed and specify the endpoint
consumer = Agent(
    name="consumer_agent",
    seed="consumer seed phrase",
    endpoint="http://localhost:8002"  # Specify an endpoint for the consumer agent
)

# On startup, the consumer requests energy
@consumer.on_event("startup")
async def request_energy(ctx: Context):
    # Consumer requests 30 units of energy from the producer
    await ctx.send("http://localhost:8001", EnergyRequest(units=30))  # Send to producer's endpoint
    ctx.logger.info("Requested 30 units of energy from the producer.")

# Handle the energy offer response from the producer
@consumer.on_message(model=EnergyOffer)
async def handle_energy_offer(ctx: Context, message: EnergyOffer):
    units = message.units
    price = message.price
    ctx.logger.info(f"Received offer for {units} units of energy at {price} FET/unit.")

if __name__ == "__main__":
    consumer.run()

'''# Handle the producer's energy offer and respond with a counter offer
@consumer.on_message(model=EnergyOffer)
async def handle_energy_offer(ctx: Context, message: EnergyOffer):
    if message.price > MAXIMUM_WILLING_PRICE:
        new_price = message.price * 0.9  # Consumer offers 10% less
        ctx.logger.info(f"Counter-offering with new price: {new_price}")
        await ctx.send("http://localhost:8001", EnergyCounterOffer(new_price=new_price))
    else:
        ctx.logger.info(f"Accepted offer for {message.units} units at {message.price} FET/unit.")
'''