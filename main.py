from fastapi import FastAPI, Request
from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import configparser


class OpenAIRequest(BaseModel):
    samples: int
    fields: List[str]
    message: str


config = configparser.ConfigParser()


load_dotenv()

base_system = "I will provide a prompt with this structure -> {message: string, samples: int, fields: [field1,field2]} and you will generate a json with an array of size samples of objects with the specified fields and fill them with mock data, and the context from the field name and the message which specifies the data context."
key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=key)
app = FastAPI()

cache = {}


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.post("/mock")
async def mock(data: OpenAIRequest):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": base_system},
            {"role": "user", "content": str(data)},
        ],
        max_tokens=1000,
        response_format={"type": "json_object"},
    )

    return eval(completion.choices[0].message.content)


@app.post("/{mock}")
async def preset(mock: str, samples: int):
    mock = mock.upper()

    request = str(mock) + "_" + str(samples)

    if request in cache:
        return cache[request]

    mock_type = None
    try:
        config.read("config.ini")

        mock_type = config[mock]

        openai_request = OpenAIRequest(
            samples=samples,
            fields=mock_type["fields"].split(","),
            message=mock_type["message"],
        )

    except KeyError:
        return {"error": "Mock not found"}

    if samples < 1:
        return {"error": "Samples must be greater than 0"}

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": base_system},
            {"role": "user", "content": str(openai_request)},
        ],
        max_tokens=1000,
        response_format={"type": "json_object"},
    )

    response = eval(completion.choices[0].message.content)
    if "cache" in mock_type and mock_type["cache"]:
        cache[request] = response

    return response
