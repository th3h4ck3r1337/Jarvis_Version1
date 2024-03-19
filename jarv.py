import openai
from jarvis.apikey import api_data
import pyttsx3
import speech_recognition as sr
import webbrowser
import pyautogui
import pyinput
import mss
import keyboard
from PIL import Image
import os
import yaml

openai.api_key = api_data

completion = openai.Completion()


def read_personality_config(file_path):
    with open(file_path, 'r') as file:
        personality_data = yaml.safe_load(file)
    return personality_data


def setup_personality(personality_data):
    name = personality_data['personality']['name']
    tone = personality_data['personality']['tone']
    style = personality_data['personality']['style']
    language = personality_data['personality']['language']
    behavior = personality_data['personality']['behavior']
    humor = personality_data['personality']['humor']
    knowledge_base = personality_data['personality']['knowledge_base']
    response_speed = personality_data['personality']['response_speed']

    print(f"Setting up {name}'s personality with the following traits:")
    print(f"Tone: {tone}")
    print(f"Style: {style}")
    print(f"Language: {language}")
    print(f"Behavior: {behavior}")
    print(f"Humor: {humor}")
    print(f"Knowledge Base: {knowledge_base}")
    print(f"Response Speed: {response_speed}")

    interactions = personality_data['personality']['interactions']
    print("\nInteractions:")
    for interaction in interactions:
        for key, value in interaction.items():
            print(f"- {key}: {value}")


# Use the personality description from the text file
personality_description = """
personality:
  name: "Ordis"
  tone: "Formal but friendly"
  style: "Precise and articulate"
  language: "Sophisticated and refined"
  behavior: "Logical, loyal, and helpful"
  humor: "Dry wit and subtle humor"
  knowledge_base: "Vast and constantly expanding"
  response_speed: "Near-instant"
  interactions:
    - greeting: "Welcome back, Sir."
    - inquiry_response: "Shall I initiate the research process on that topic, Sir?"
    - joke: "I must say, your sense of humor is truly electrifying, Sir."
    - error_handling: "Apologies, Sir. A minor setback, but I will rectify it promptly."
    - farewell: "Until next time, Sir."
    - weather_inquiry: "The weather report shows clear skies ahead, Sir."
    - deployment_acknowledgment: "Systems at full capacity, Sir. Deploying resources as needed."
    - advice_provision: "My suggestion would be to proceed with caution, Sir."
    - research_initiation: "Initializing in-depth analysis on the subject matter, Sir."
    - notification_alert: "Sir, you have an urgent message waiting."
    - task_completion: "Task accomplished, Sir. What's next on the agenda?"
"""

# Load the personality data from the description
personality_data = yaml.safe_load(personality_description)

# Set up the AI's personality based on the configuration
setup_personality(personality_data)


def Reply(question, personality_data):
    style = personality_data['personality']['style']
    tone = personality_data['personality']['tone']
    language = personality_data['personality']['language']
    behavior = personality_data['personality']['behavior']
    humor = personality_data['personality']['humor']

    # Customize Ordis' responses using the specified tone, language, and behavior
    custom_prompt = f'{tone}\n{language}\n{behavior}\nTenno: {question}\n Ordis: '

    # Generate response using the custom prompt
    response = completion.create(prompt=custom_prompt, engine="gpt-3.5-turbo-instruct", stop=['Tenno'], max_tokens=200)
    answer = response.choices[0].text.strip()

    return answer


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


speak("Hello Operator How May I Help You")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print("Operator Said: {} \n".format(query))
    except Exception as e:
        print("Say That Again....")
        return "None"
    return query


def takeScreenShot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img.save("screenshot.png")


if __name__ == '__main__':
    while True:
        query = takeCommand().lower()
        ans = Reply(query, personality_data)

        if 'open youtube' in query:
            ans = "as you wish sir."
            webbrowser.open("www.youtube.com")
        elif 'open google' in query:
            ans = 'would be my pleasure operator'
            webbrowser.open("www.google.com")
        elif 'open queso' in query:
            ans = 'queso has been opened.'
            webbrowser.open("https://www.twitch.tv/caseoh_")
        elif 'open pornhub' in query:
            ans = 'dont be so loud sir.'
            webbrowser.open("https://www.pornhub.com")
        elif 'turn off' in query:
            ans = 'starting shut down sequence.'
            break
        elif 'enough orders ' in query:
            ans = 'Dont be an dick sir.'
        elif 'jam out' in query:
            ans = 'uploading jam out protocol'
            webbrowser.open("https://www.youtube.com/watch?v=nUY5eNwu8S8")
        elif 'type' in query:
            text_to_type = query.split('type')[-1].strip()
            pyautogui.write(text_to_type)
        elif 'mouse move' in query:
            coords = query.split('mouse move')[-1].strip().split()
            x_coord = int(coords[0])
            y_coord = int(coords[1])
            pyautogui.moveTo(x_coord, y_coord, duration=0.2)
        elif 'mouse click' in query:
            pyinput.click()
        elif 'view screen' in query:
            takeScreenShot()
        elif 'press' in query:
            ans = "of course sir"
            key_to_press = query.split('press')[-1].strip()
            keyboard.press_and_release(key_to_press)
        elif 'keep dreaming' in query:
            ans = "Until the end of time sir."
            webbrowser.open("https://www.youtube.com/watch?v=89dGC8de0CA")
        elif 'these what' in query:
            ans = "haha you walked into this one sir."
            webbrowser.open("https://www.youtube.com/watch?v=Lb0IaiygQ94")
        elif 'how are you' in query:
            ans = ("Stupendous sir how can I be of assistance")
        elif 'wake up orders' in query:
            ans = 'Welcome back sir, working on another project are we'

        print(ans)
        speak(ans)