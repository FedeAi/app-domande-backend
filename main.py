import datetime
import random
import pandas as pd

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

dataframe = pd.read_csv("domande.csv")
topics = list(dataframe["topic"].unique())

app = FastAPI()

origins = [
    # "http://localhost:3000",
    # "localhost:3000"
    '*'
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def buonanotte(entry):
    if datetime.datetime.now().time() > datetime.time(23,0,0) or datetime.datetime.now().time() < datetime.time(7,30,0):
        return {"question": "Buonanotte tesoro <3",
                "topic": "Notte"}
    return entry

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/question")
async def question():
    if dataframe.shape[0] == 0:
        return {"message": "",
                "topic": ""}
    random_index = random.randint(0, dataframe.shape[0] - 1)
    entry = dataframe.iloc[random_index]
    entry = buonanotte(entry)
    return {"message": entry["question"],
            "topic": entry["topic"]}


@app.get("/topics")
async def pollo():
    return {"message": topics}


@app.get("/question/{topic}")
async def question(topic: str):
    df = dataframe[dataframe["topic"]==topic]
    if df.shape[0] == 0:
        return {"message": "",
                "topic": ""}

    random_index = random.randint(0, df.shape[0] - 1)
    entry = df.iloc[random_index]
    entry = buonanotte(entry)
    return {"message": entry["question"],
            "topic": entry["topic"]}

