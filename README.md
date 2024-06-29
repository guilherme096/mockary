<p align="center">
<img src="https://github.com/guilherme096/mockary/assets/69405307/6c66e2d5-6758-4d64-a003-ed76804ecdf2" height="300">
</p>
<p align="center">
A feather weight mock data generator API
</p>

Extremely simple python API to generate mock data for your app using chatgpt openai model.

## Features

- Mock Data generation for especific fields and context
- Data caching and saving to file

## Installation

It is recommended to use poetry to create a virtual environment and install the dependencies.

```bash
poetry install
```

## Usage

```bash
poetry run uvicorn mockary:app
```

## Quick Start

Mockary is very simple to use. It only takes around 5 minutes to get it up and running (including the time of reading this guide).

### Add OpenAI API Key

Modify the `.env.example` with the OpenAI Api Key and rename it to `.env`.

### Start the server

```bash
poetry run uvicorn mockary:app
```

### Define a Mock

There are some examples in the `config.ini` file. To add a new one use this base template:

```ini
[MockName]
fields=field1,field2,field3
message="Message to give the AI model context about the data"
cache=true
```

### Call the API

```bash
curl -X 'POST' \
  'http://localhost:8000/MockName?samples=[number of samples]'
```

The result will be a JSON with the generated data.

```json
{
    "data": [
        {
            ... generated data ...
        },
    ]
}
```
