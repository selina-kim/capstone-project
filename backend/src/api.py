# Given a word, the program will make a flash card with translation and relevant examples
# first use api to get translation

import requests

def call_definition_api(word):
    # Example: Sending a GET request to a public API
    # https://dictionaryapi.com/products/api-collegiate-dictionary
    url = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key=ce0168de-8eaa-429e-949a-714b3bce818a"
    response = requests.get(url)

    # Check for success
    if response.status_code == 200:
        data = response.json()

        # Grab the very first definition/pronunciation/audio
        try:
            first_sense = data[0]["def"][0]["sseq"][0][0]
            first_definition = first_sense[1]["dt"][0][1].replace("{bc}", "").strip()
            print(first_definition)

            pronunciation = data[0]["hwi"]["prs"][0]["mw"]
            print(pronunciation)

            # defined here under audio: https://www.dictionaryapi.com/products/json#sec-2.prs
            audio = data[0]["hwi"]["prs"][0]["sound"]["audio"]

            # Determine subdirectory
            if audio.startswith("bix"):
                subdirectory = "bix"
            elif audio.startswith("gg"):
                subdirectory = "gg"
            elif audio[0].isdigit() or not audio[0].isalpha():  # numbers or punctuation
                subdirectory = "number"
            else:
                subdirectory = audio[0]

            audio_url = f"https://media.merriam-webster.com/audio/prons/en/us/mp3/{subdirectory}/{audio}.mp3"
            print(audio_url)


        except (KeyError, IndexError):
            first_definition = "Definition not found"
            pronunciation = None
            audio_url = None
        
        return {
            "word": word,
            "definition": first_definition,
            "pronunciation": pronunciation,
            "audio_url": audio_url
        }
    else:
        return {"error": "Failed to fetch data"}, response.status_code