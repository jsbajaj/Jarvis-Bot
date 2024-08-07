import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sys
import pyjokes
import pyautogui
import time
import instaloader
import PyPDF2
from pywikihow import search_wikihow
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_USER = os.getenv("jasnoorsinghbajaj@gmail.com")
EMAIL_PASSWORD = os.getenv("4193226599jassi#")

# Initialize the pyttsx3 engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Setting the voice to the first option

# Text-to-speech function
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Speech recognition function
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")

    except Exception as e:
        speak("Sorry, can you please repeat that again.")
        print(f"Error: {e}")
        return "none"
    query = query.lower()
    return query

def wake_word_detection():
    while True:
        command = takecommand().lower()
        if "wake up jarvis" in command or "hey jarvis" in command:
            speak("Yes Sir, I am here.")
            TaskExecution()

def wish():
    hour = int(datetime.datetime.now().hour)
    current_time = datetime.datetime.now().strftime("%I:%M %p")

    if hour >= 0 and hour < 12:
        speak("Good morning")

    elif hour >= 12 and hour < 16:
        speak("Good afternoon")
    else:
        speak("Good evening")
    
    speak(f"It is {current_time}")
    speak("I am Jarvis, your virtual assistant")

    # Asking the user how they are
    speak("How are you?")
    user_response = takecommand().lower()

    # Responding based on the user's reply
    if "great" in user_response or "alright" in user_response or "well" in user_response or "fine" in user_response:
        speak("That's good to hear. How may I help you?")
    else:
        speak("I hope everything is okay. How may I assist you?")

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Corrected port number
        server.ehlo()
        server.starttls()
        server.login("jasnoorsinghbajaj@gmail.com", "4193226599jassi#")
        server.sendmail("jasnoorsinghbajaj@gmail.com", to, content)
        server.close()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak("Sorry, I was unable to send the email.")
        print(f"Error: {e}")

def pdf_reader():
    book = open('book.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"Total number of pages in this book are {pages}")
    speak("Please enter the page number you would like me to read.")
    pg = int(input("Please enter the page number: "))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)

def TaskExecution():
    wish()
    while True:
        query = takecommand().lower()

        # Logic building for task
        if "open notepad" in query:
            npath = "C:\\Windows\\notepad.exe"
            os.startfile(npath)

        elif "open vs code" in query:
            cpath = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(cpath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                if cv2.waitKey(50) == 27:  # Escape key to exit
                    break
            cap.release()
            cv2.destroyAllWindows()
        
        elif "play a song" in query or "play music" in query or "play songs" in query:
            music_dir = "C:\\music"
            songs = os.listdir(music_dir)
            rd = random.choice(songs)
            os.startfile(os.path.join(music_dir, rd))

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")

        elif "wikipedia" in query:
            speak("Searching...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            speak(results)
            print(results)

        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")

        elif "open netflix" in query:
            webbrowser.open("www.netflix.com")

        elif "open blackboard" in query:
            webbrowser.open("https://blackboard.utdl.edu/?new_loc=%2Fultra%2Fcourse")

        elif "open google" in query:
            speak("What should I search on google?")
            cm = takecommand().lower()
            webbrowser.open(f"{cm}")

        elif "send whatsapp message" in query:
            speak("Please tell me the phone number of the recipient with country code.")
            phone_number = takecommand().lower().replace(" ", "")
            speak("What is the message?")
            message = takecommand().lower()
            speak("At what time should I send the message? Please specify in 24-hour format.")
            speak("Hour:")
            hour = int(takecommand().lower())
            speak("Minute:")
            minute = int(takecommand().lower())
            kit.sendwhatmsg(phone_number, message, hour, minute)
            speak("Message scheduled successfully.")

        elif "play song on youtube" in query:
            speak("Which song would you like me to play?")
            song = takecommand().lower()
            kit.playonyt(song)

        elif "send an email" in query:
            speak("What should I say?")
            content = takecommand().lower()
            sendEmail('jasnoorocks@gmail.com', content)

        elif "send a file" in query:
            speak("What is the subject?")
            subject = takecommand().lower()
            speak("What is the message?")
            message = takecommand().lower()
            speak("Please enter the correct path of the file into the shell")
            file_location = input("Please enter the path here: ")

            msg = MIMEMultipart()
            msg['From'] = EMAIL_USER
            msg['To'] = 'jasnoorocks@gmail.com'
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            filename = os.path.basename(file_location)
            attachment = open(file_location, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename}")

            msg.attach(part)

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("jasnoorsinghbajaj@gmail.com", "EMAIL_PASSWORD")
                text = msg.as_string()
                server.sendmail("jasnoorsinghbajaj@gmail.com", 'jasnoorocks@gmail.com', text)
                server.quit()
                speak("Email has been sent to the recipient.")
            except Exception as e:
                speak("Sorry, I was unable to send the email.")
                print(f"Error: {e}")

        elif "close notepad" in query:
            speak("Okay, closing notepad")
            os.system("taskkill /f /im notepad.exe")

        elif "set alarm" in query:
            nn = int(datetime.datetime.now().hour)
            if nn == 22:
                music_dir = "C:\\music"
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "shutdown" in query:
            speak("Shutting down the system")
            os.system("shutdown /s /t 5")

        elif "restart" in query:
            speak("Restarting the system")
            os.system("shutdown /r /t 5")

        elif "switch the window" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        elif "where am I" in query or "where are we" in query:
            speak("Wait Sir, let me check")
            try:
                ipAdd = get('https://api.ipify.org').text
                print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                geo_requests = get(url)
                geo_data = geo_requests.json()
                city = geo_data['city']
                country = geo_data['country']
                speak(f"Sir, I am not sure, but I think we are in {city} city of {country} country")
            except Exception as e:
                speak("Sorry sir, Due to network issue I am not able to find where we are.")
                pass

        elif "instagram profile" in query or "profile on instagram" in query:
            speak("Please enter the user name correctly.")
            name = input("Enter username here: ")
            webbrowser.open(f"www.instagram.com/{name}")
            speak(f"Sir, here is the profile of the user {name}")
            time.sleep(5)
            speak("Would you like to download the profile picture of this account?")
            condition = takecommand().lower()
            if "yes" in condition:
                mod = instaloader.Instaloader()
                mod.download_profile(name, profile_pic_only=True)
                speak("I am done, Profile picture is saved in our main folder. Now I am ready to take the next command.")

        elif "take screenshot" in query or "take a screenshot" in query:
            speak("Sir, please tell me the name for this screenshot file")
            name = takecommand().lower()
            speak("Please hold the screen for few seconds, I am taking screenshot")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("I am done, the screenshot is saved in our main folder. Now I am ready to take the next command.")

        elif "read pdf" in query:
            pdf_reader()

        elif "volume up" in query:
            pyautogui.press("volumeup")

        elif "volume down" in query:
            pyautogui.press("volumedown")

        elif "mute" in query:
            pyautogui.press("volumemute")

        elif "how to" in query:
            speak("Getting data from the internet")
            op = query.replace("jarvis", "")
            max_results = 1
            how_to_func = search_wikihow(op, max_results)
            assert len(how_to_func) == 1
            how_to_func[0].print()
            speak(how_to_func[0].summary)

        elif "temperature" in query:
            search = "temperature in Toledo"
            url = f"https://www.google.com/search?q={search}"
            r = get(url)
            data = r.text
            temperature = data.split('">')[1].split('°')[0]
            speak(f"The temperature in Toledo is {temperature} degrees Celsius.")

        elif "stop listening" in query:
            speak("For how many seconds do you want me to stop listening to your commands?")
            ans = int(takecommand())
            time.sleep(ans)
            print(ans)

        elif "log out" in query:
            speak("Logging out")
            os.system("shutdown -l")

        elif "goodbye" in query or "bye" in query or "exit" in query or "take rest" in query or "go to sleep" in query or "that's all" in query:
            speak("Goodbye Sir, Have a great day!")
            sys.exit()

        elif "thank you" in query or "thanks buddy" in query or "thanks" in query:
            speak("You're welcome! How else can I help you?")
            continue

        elif "not working" in query:
            speak("I'm sorry to hear that something isn't working. Can you provide more details or specify which feature is causing the issue?")

if __name__ == "__main__":
    wake_word_detection()
