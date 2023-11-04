# Import necessary libraries
from fastapi import FastAPI

# Create the FastAPI instance
app = FastAPI()

# Define a route
@app.get("/")
async def read_root():
    return {"Hello": "World"}

