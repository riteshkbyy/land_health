
import google.generativeai as genai
from google.cloud import texttospeech

import requests
import subprocess
import json
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY2')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")
permissible_range = {
    'Ph' : '6.5 to 7.5',
    'Electrical Conductivity (EC)' : 'less than 1',
    'Organic Carbon (OC)' : '0.5 to 0.75',
    'Nitrogen (N)'	: '250 to 500',
    'Phosphorus (P)' : '25 to 50',
    'Potassium (K)' : '125 to 300',
    'Boron (B)' : 'greater than 10',
    'Sulfur (S)' : 'greater than 0.78',
    'Zinc (Zn)' : 'greater than 0.50',
    'Copper (Cu)' : 'greater than 7',
    'Iron (Fe)' :'greater than 3',
    'Manganese (Mn)' :'greater than 0.6',
}

def generate_prompt(df,row, language):
    farmer_name = str(df.iloc[row]["FARMER'S NAME"])
    soil_parameters = df.iloc[row][['PH', 'EC', 'OC', 'N', 'P', 'K', 'B', 'S', 'Zn', 'Cu', 'Fe', 'Mn']].values

    prompt = (
        f"You are an experienced female agrologist. After conducting laboratory tests, "
        f"you have received the following soil parameter values for a farm owned by {farmer_name} in Western Bihar. "
        f"The permissible limits for each parameter are {permissible_range}. "
    )

    prompt += (
        "The test results for these soil parameters are as follows: "
        f"{soil_parameters}. "
    )

    prompt += (
        f"Based on these results and considering the climate conditions of Western Bihar, "
        f"please advise {farmer_name} on the most suitable crops to grow. "
        f"Keep your advice clear, simple, and STRICTLY in everyday {language} language. "
        "Avoid using symbols. Instead of symbols, use numbers where necessary to make it easy to understand. "
        "Also, suggest the appropriate amount of fertilizers to apply per hectare, ensuring the best efficiency and healthy crop growth."
    )

    prompt += (
        f"also add this remark at the end in {language} language {df.iloc[row]["remarks"]} do not use any symbols"
    )

    return prompt

def text_to_speech(df,text, row, language):
    # Initialize the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Set the input text
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Set the voice parameters (language and gender)
    voice = texttospeech.VoiceSelectionParams(
        language_code="hi-IN",  # Change this to your desired language code
        # ssml_gender=texttospeech.SsmlVoiceGender.FEMALE  # Can be MALE or NEUTRAL as well
        name = "hi-IN-Chirp3-HD-Zephyr"# "hi-IN-Chirp3-HD-Leda" "hi-IN-Chirp3-HD-Kore"
    )

    # Set the audio encoding (MP3, OGG, or WAV)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3  # You can use MP3, OGG, or LINEAR16
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio to a file
    filename = "output/{}_{}_output.mp3".format(str(df.iloc[row]["FARMER'S NAME"]).replace(" ","_"),language)
                
    with open(filename, "wb") as out:
        out.write(response.audio_content)

    print("Audio content written to file " + filename)
    return filename


def Generate_Audio_explanation(df,x = 0):
    language = "hindi"
    df.rename(columns={'farmer_name': 'FARMER\'S NAME', 'ph' :'PH', 'ec': 'EC', 'oc': 'OC', 'n':'N', 'p': 'P', 'k':'K', 'b':'B', 's': 'S', 'zn': 'Zn', 'cu': 'Cu', 'fe': 'Fe', 'mn': 'Mn'}, inplace=True)
    prompt = generate_prompt(df, row = x, language = language)
    print('prompt generated')
    response = model.generate_content(prompt)
    text = response.text
    print('response from gen ai model received')
    filename = text_to_speech(df = df, text = text, row = x, language = language)
    return filename

ACCESS_TOKEN = "EAAP5ZCGTlinwBO9cejpQIM3Kt7o0khmaPsmVjc7ZCABsG7LKRZAieUeAFHDu6PFEwZCT4esykJaYsenvWWTKN2oLXtGieFgCUPKZAsZC1mQqaFirw2PCqnzYFCzH3kh7O7nedACfebWttZBevGFZBiedBlpvVyLboMVTgLFcQjbZC6ZBzbka1Ac9ZCxMm24M72qZBMP46DbHkbRx8SUGmm4rCvbzUbkLETxZB"
PHONE_NUMBER_ID = "618662564644276"  # Your WhatsApp Business Account's Phone Number ID

message_url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
message_headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
    }

def Whatsapp_notification(RECIPIENT_PHONE_NUMBER):
    # Replace these values

    payload = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_PHONE_NUMBER,
        "type": "template",
        "template": {
            "name": "land_health_report_bhojpuri_template",  # Replace with your template name
            "language": {
                "code": "hi"  # Hindi
            }
        }
    }

    response = requests.post(message_url, headers=message_headers, json=payload)

    # Print the response
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def Whatsapp_send_file(RECIPIENT_PHONE_NUMBER, filename):
    media_url =  f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/media"
    headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    files = {
        'file': ('audio.mp3', open(filename, 'rb'), 'audio/mpeg')
    }

    data = {
        "messaging_product": "whatsapp",
    }
    response = requests.post(media_url, headers=headers, files=files, data=data)

    print("Status Code:", response.status_code)
    print("Response:", response.json())

    media_id = response.json().get("id")
    print("Uploaded Media ID:", media_id)
    payload = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_PHONE_NUMBER,
        "type": "audio",
        "audio": {
            "id": media_id, 
        }
    }
    response = requests.post(message_url, headers=message_headers, json=payload)


