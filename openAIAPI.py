import openai
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')

# Set up the OpenAI API key
openai.api_key = OPENAI_KEY

# Define a function to get a response from ChatGPT
def get_response(info, prompt):
    conversation = f"Pretend you are my intelligent human assistant that analyzes user info and give \
             health advice based on their age, weight, gender, height and caloric information. Do NOT mention you are an AI language model."
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_KEY}",
    }

    age = info[0]
    gender = info[1]
    weight = info[2]
    height = info[3]

    starter = f"Do NOT mention you are an AI language model. I am a {age} year old {gender}, I weigh {weight} pounds and am {height}cm tall. "
    user_input = starter + prompt

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "assistant", "content": conversation},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 256,
        "n": 1,
        "temperature": 0.5,
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"