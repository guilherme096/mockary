from fastapi import FastAPI
from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import configparser
import json


class OpenAIRequest(BaseModel):
    samples: int
    fields: List[str]
    message: str


config = configparser.ConfigParser()

if not os.path.exists("config.ini"):
    raise Exception("Config file not found")

load_dotenv()

base_system = "I will provide a prompt with this structure -> {message: string, samples: int, fields: [field1,field2]} and you will generate a json with an array of size samples of objects with the specified fields and fill them with mock data, and the context from the field name and the message which specifies the data context."
key = os.getenv("OPENAI_API_KEY")

if key is None:
    raise Exception("OpenAI API Key not found")

client = OpenAI(api_key=key)
app = FastAPI()

cache = {}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/{mock}")
async def preset(
    mock: str, samples: int, randomize: bool = False, max_tokens: int = 10000
):
    mock = mock.upper()
    path = ""

    if samples < 1:
        return {"error": "Samples must be greater than 0"}

    request = str(mock) + "_" + str(samples)

    if not randomize and request in cache:
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

    if not randomize and "save" in mock_type and mock_type["save"]:
        if "save_path" in mock_type:
            path = mock_type["save_path"] + ".json"
        else:
            path = mock.lower() + ".json"

        if os.path.exists(path):
            with open(path, "r") as file:
                data = file.read()

                data = json.loads(data)

                if samples <= len(data["data"]):
                    return data["data"][1:samples]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": base_system},
            {"role": "user", "content": str(openai_request)},
        ],
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
    )

    response = eval(completion.choices[0].message.content)
    if "cache" in mock_type and mock_type["cache"]:
        cache[request] = response

    if "save" in mock_type and mock_type["save"]:
        with open(path, "w") as file:
            file.write(json.dumps(response))

    return response
