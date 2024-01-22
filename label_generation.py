import openai

api_key = "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"

def generate_tags_with_chat_model(sentence):
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[

            {"role": "system", "content": "Suggest up to three tags that represent the topic of the user input. Return 'none' if no relevant tags are found. Example: \"The sun sets early in the winter\" Tags: Nature, Seasons, Daylight."},
            {"role": "user", "content": sentence}
        ]
    )
    tags= response.choices[0].message['content'].strip()
    return tags.split(", ")

#Example
#sentence = "Draw the general structure of a profile hidden markov model with labels"
#tags = generate_tags_with_chat_model(sentence, api_key)
#print(tags)
# >> ['Modeling', 'Machine Learning', 'Hidden Markov Model']