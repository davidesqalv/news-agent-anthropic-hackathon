from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # TODO implement OAuth2
    # TODO replace mytoken with the actual token
    return {"access_token": "mytoken", "token_type": "bearer"}


@app.get("/preferences")
async def get_preferences(token: Annotated[str, Depends(oauth2_scheme)]):
    # TODO: verify the token
    preferences = [
        "Artificial Intelligence",
        "UK Politics",
        "Russia-Ukraine War",
    ]  # TODO: Look up the user's preferences in the DB
    return preferences
