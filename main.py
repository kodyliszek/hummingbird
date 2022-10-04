from fastapi import FastAPI
from fuzzywuzzy import fuzz

from fan.controller import FanController

app = FastAPI()


@app.get("/")
async def root():
    domain = "https://fuzzy-hummingbird.herokuapp.com"
    # domain = "http://127.0.0.1:8000"
    return {
        "fan": f"Please provide temperature[*C] and humidity[%] e.g. {domain}/fan/?temperature=18&humidity=60",
        "words": {
            "ratio": f"{domain}/words/ratio/?phrase_1=Idego%20is%20the%20best&phrase_2=Idego%20is%20the%20best%21",
            "partial_ratio": f"{domain}/words/partial_ratio/?phrase_1=Idego%20is%20the%20best&phrase_2=Idego%20is%20the%20best%21",
            "token_sort_ratio": f"{domain}/words/token_sort_ratio/?phrase_1=Idego%20is%20the%20best&phrase_2=Idego%20the%20best%20is",
        },
    }


@app.get("/fan/")
async def fan(temperature: int = 0, humidity: int = 0):
    fc = FanController()
    fan_speed = fc.compute(temperature, humidity).get("fan_speed")
    return {
        "message": f" For Temperature = {temperature} and Humidity = {humidity}, Fan Speed shall be {fan_speed}"
    }


@app.get("/words/ratio/")
async def ratio(phrase_1: str, phrase_2: str):
    return fuzz.ratio(phrase_1, phrase_2)


@app.get("/words/partial_ratio/")
async def ratio(phrase_1: str, phrase_2: str):
    return fuzz.partial_ratio(phrase_1, phrase_2)


@app.get("/words/token_sort_ratio/")
async def ratio(phrase_1: str, phrase_2: str):
    return fuzz.token_sort_ratio(phrase_1, phrase_2)
