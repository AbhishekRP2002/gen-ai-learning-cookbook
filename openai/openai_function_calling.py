import langchain
import openai
from dotenv import load_dotenv
import os
import logging
import json
import requests
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_weather_forecast(location, unit = "celsius"):
    weather_api_key = os.getenv("WEATHER_API_KEY")
    request_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}"
    if requests.get(request_url).status_code == 200:
        response  = requests.get(request_url).json()
        if unit == "celsius":
            temperature = response["main"]["temp"] - 273.15
            unit = "C"
        elif unit == "fahrenheit":
            temperature = (response["main"]["temp"] - 273.15) * 9/5 + 32
            unit = "F"
    else:
        logger.info(f"Error in fetching the weather forecast for the location {location}")
    # return response in json format or dictionary format
    return response
    

# client = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather_forecast",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string", 
                        "enum": ["celsius","fahrenheit"]
                        },
                },
                "required": ["location"],
            },
        }
    }
]
messages = [
    {"role": "system", "content": "You are an helpful AI assistant."},
    {"role": "user", "content": "What's the weather like in Boston today?"} # Please note that searching by states available only for the USA locations. We can use Geocoder API to get the location coordinates and then use the OpenWeatherMap API to get the weather forecast.
    ]

completion_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0125",
    messages=messages,
    tools=tools,
    tools_choice="auto"
)

response_message = completion_response.choices[0].message
tool_calls = response_message.tool_calls
if tool_calls:
    available_functions = {
        "get_weather_forecast": get_weather_forecast,
    }
    messages.append(response_message)
    for tool_call in tool_calls:
        function_name = tool_call.function_name
        function = available_functions[function_name]
        function_args = json.loads(tool_call.arguments)
        function_kwargs = tool_call.keyword_arguments
        function(*function_args, **function_kwargs)
        function_response = function(
            location= function_args.get("location"),
            unit= function_args.get("unit")
        )
        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        )
    final_response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,

    )
    print(final_response.choices[0].message.content)