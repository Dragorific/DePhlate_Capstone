import openai

# Set up the OpenAI API key
openai.api_key = "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"

# Define a function to get a response from ChatGPT
def get_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,  # The maximum number of tokens (words and punctuation) that the generated text can have. The actual number of tokens in the generated text may be less than this value.
        n=1,              # The number of responses to generate. In most cases, you'll only need one response, so you can set this to 1.
        stop=None,        # Keep generating until max toxen reached
        temperature=0.5,  # A parameter that controls the randomness and creativity of the generated text. A higher temperature results in more random and creative text, while a lower temperature results in more predictable and conservative text. A value of 0.5 is a good starting point.  
    )
    message = response.choices[0].text.strip()
    return message

# Define a function to provide health advice based on nutritional information
def provide_health_advice(nutrition_info):
    # Here, you can add your logic to analyze the nutrition information and provide health advice based on it.
    # For example, you could check the amount of calories, fat, sugar, etc. and suggest dietary changes or exercise routines.
    # In this example, we'll just return a generic health advice message.
    return "Based on the nutritional information you provided, it's important to maintain a balanced diet and exercise regularly to stay healthy."

# Start the conversation
prompt = "The following is a conversation with a health advisor. The advisor can provide you with health advice based on nutritional information you provide. To begin, please enter your nutritional information:"

# Enter into a loop to keep the conversation going
while True:
    # Get user input
    user_input = input("You: ")

    # Add the user input to the prompt
    prompt += "\nUser: " + user_input

    # Check if the user has entered nutritional information
    if "calories" in user_input.lower() or "fat" in user_input.lower() or "sugar" in user_input.lower():
        # Provide health advice based on the nutritional information
        health_advice = provide_health_advice(user_input)

        # Get a response from ChatGPT with the health advice
        message = get_response(prompt + "\nHealth Advisor: " + health_advice)

        # Print the response
        print("ChatGPT:", message)

        # Add the response to the prompt
        prompt += "\nChatGPT: " + message
    else:
        # Get a response from ChatGPT without health advice
        message = get_response(prompt)

        # Print the response
        print("ChatGPT:", message)

        # Add the response to the prompt
        prompt += "\nChatGPT: " + message
