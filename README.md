<p align="center">
<img src="https://github.com/guilherme096/mockary/assets/69405307/6c66e2d5-6758-4d64-a003-ed76804ecdf2" height="300">
</p>
<p align="center">
A feather weight mock data generator API
</p>

**Extremely simple python API to generate mock data for your app using chatgpt openai model.**

## Features

- Mock Data generation for especific fields and context
- Data caching and saving to file

## Installation

Use poetry to create a virtual environment and install the dependencies.

Move into `/mockary/mockary` folder and run:

```bash
poetry install
```

## Quick Start

Mockary is very simple to use. It only takes around 5 minutes to get it up and running (including the time of reading this guide).

### Add OpenAI API Key

Modify the `.env.example` with the OpenAI Api Key and rename it to `.env`.

### Start the server

Inside the `/mockary/mockary` directory run:

```bash
poetry run uvicorn main:app
```

### Define a Mock

There are some examples in the `/mockary/mockary/config.ini` file. To add a new one use this base template:

```ini
[MockName]
fields=field1,field2,field3
message="Message to give the AI model context about the data"
cache=true
```

### Call the API

```bash
curl -X 'GET' \
  'http://localhost:8000/[MockName]?samples=[number of samples]'
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

## Settings

**Global Settings**
| Option | Description |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `cache` | Can be used in `CONFIG` or individual mock. If true, the generated data will cached in memory. |
| `max_tokens` | Maximum tokens to generate. Default is the maximum - 4096. |
| `model` | Especific model to use. Default is `gpt-3.5-turbo`. To use other models use the name as described in the openai documentation |
| `temperature` | Temperature to use in the model. Default is 1. |

**Mock Settings**  
| Option | Description |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `save` | Save the generated data to a file. |
| `save_path` | Path to save the generated data. The default is `./mock_name` |
| `fields` | Fields to generate data. |
| `message` | Message to give the AI model context about the data. |
