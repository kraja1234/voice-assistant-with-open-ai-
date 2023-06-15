import AppOpener
import speech_recognition as sr
import win32com.client
import  webbrowser
import openai
import os
import datetime
import requests
from config import apikey
from config import weather_api
from config import news_api
speaker=win32com.client.Dispatch("SAPI.SpVoice")
n=0
def chat(query):
    global chatStr
    openai.api_key = apikey
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])

def weather():
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?units=metric&"
    city = "Hyderabad"
    appid = weather_api
    url = BASE_URL + "appid=" + appid + "&q=" + city
    response = requests.get(url).json()
    res_des=response['weather'][0]['description']
    res_temp=response['main']['temp']
    res_hum=response['main']['humidity']
    say(f"weather is {res_des} temperature is{res_temp} degree celsius and {res_hum} humid")
def news():
    BASE_URL = "https://newsapi.org/v2/top-headlines?country=in&sortBy=popularity&apiKey="
    key = news_api
    url = BASE_URL + key
    global n
    response = requests.get(url).json()
    say(response['articles'][n]['content'])
    n=n+1

def ai(prompt):
    openai.api_key = apikey
    text = f"{prompt}\n**************************\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # print(response["choices"][0]["text"])
    try:
        text += response["choices"][0]["text"]

    except Exception as e:
        print(e)
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def say(text):
    speaker.Speak(text)

def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold= 0.6
        audio=r.listen(source)
        try:
            print("recognizing........")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said :{query}")
            return query
        except Exception as e:
            return "an error occured sorry from jarvis"

if __name__ == '__main__':
    say("Hello I am jarvis A I ")
    while True:
        print("Listening......")
        command = takecommand()
        sites =[["youtube","https://youtube.com"],["google","https://google.com"],["instagram","https://instagram.com"]]
        for site in sites:
                if f"open {site[0]}".lower() in command.lower():
                         say(f"opening{site[0]} sir")
                         webbrowser.open(site[1])
        if "open spotify".lower() in command.lower():
            say("opening spotify")
            AppOpener.open("spotify")
        elif "open telegram".lower()  in command.lower():
            say("opening telegram")
            AppOpener.open("telegram")
        elif "the time".lower() in command.lower():
            hour=datetime.datetime.now().strftime("%H")
            min=datetime.datetime.now().strftime("%M")
            say(f"sir time is {hour} hours {min} minutes")
        elif "open brave" in command.lower():
            AppOpener.open("brave")
        elif "using artificial intelligence".lower() in command.lower():
            ai(prompt=command)
        elif "weather".lower() in command.lower():
            weather()
        elif "news".lower() in command.lower():
            news()
        else:
            chat(command)
        # say(command)


