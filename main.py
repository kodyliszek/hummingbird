from fastapi import FastAPI

from fan.controller import FanController

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Please provide temperature[*C] and humidity[%] e.g. https://fuzzy-hummingbird.herokuapp.com/fan/?temperature=18&humidity=60 "
    }


@app.get("/fan/")
async def fan(temperature: int = 0, humidity: int = 0):
    fc = FanController()
    fan_speed = fc.compute(temperature, humidity).get('fan_speed')
    return {"message": f" For Temperature = {temperature} and Humidity = {humidity}, Fan Speed shall be {fan_speed}"}
