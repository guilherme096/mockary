from fastapi import FastAPI
from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import configparser
import json
from config import *
from OpenAIRequest import *


load_dotenv()
key = os.getenv("OPENAI_API_KEY")
assert key is not None


config_parser = configparser.ConfigParser()
config_parser.read("config.ini")

if not os.path.exists("config.ini"):
    raise Exception("Config file not found")

config = get_config_from_file(config_parser)
config = set_config_key(key, config)

client = OpenAI(api_key=config.key)
app = FastAPI()

cache = {}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/{mock}")
async def preset(mock: str, samples: int, randomize: bool = False):
    mock = mock.upper()
    path = ""

    if samples < 1:
        return {"error": "Samples must be greater than 0"}

    # identifier for cache
    request = str(mock) + "_" + str(samples)

    use_cache = not randomize and request in cache
    if use_cache:
        return cache[request]

    mock_type = None
    try:
        # re-read file to allow for dynamic changes in config without restarting the server
        config_parser = configparser.ConfigParser()
        config_parser.read("config.ini")

        mock_type = config_parser[mock]

        openai_request = OpenAIRequest(
            samples=samples,
            fields=mock_type["fields"].split(","),
            message=mock_type["message"],
        )
    except KeyError:
        return {"error": "Mock not found"}

    save_data = not randomize and "save" in mock_type and mock_type["save"]
    if save_data:
        if "save_path" in mock_type:
            path = mock_type["save_path"] + ".json"
        else:
            path = mock.lower() + ".json"

        path = os.path.expanduser(path)

        if os.path.exists(path):
            with open(path, "r") as file:
                data = file.read()

                data = json.loads(data)

                # load number of samples request from file
                if samples <= len(data["data"]):
                    return data["data"][1:samples]

    completion = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": config.base_system},
            {"role": "user", "content": str(openai_request)},
        ],
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        response_format={"type": "json_object"},
    )

    response = eval(completion.choices[0].message.content)

    cache_data = config.cache or ("cache" in mock_type and mock_type["cache"])
    if cache_data:
        cache[request] = response

    if save_data:
        with open(path, "w") as file:
            file.write(json.dumps(response))

    return response
