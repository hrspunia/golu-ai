import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import wikipedia
import threading

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
wikipedia.set_lang("en")

def speak(text):
    """Convert text to speech and print it"""
    print("Golu:", text)
    engine.say(text)
    engine.runAndWait()

def get_weather(city="Delhi"):
    """Return mock weather information (replace with API if needed)"""
    return f"The weather in {city} is 30°C with clear skies."

def remind_me(text, delay_seconds):
    """Set a reminder with a delay"""
    def reminder():
        speak(f"Reminder: {text}")
    threading.Timer(delay_seconds, reminder).start()

def get_time():
    """Return the current time"""
    return datetime.datetime.now().strftime("It's %I:%M %p")

def get_date():
    """Return the current date"""
    return datetime.datetime.now().strftime("Today is %A, %B %d, %Y.")

def process_command(command):
    """Process and respond to user commands"""
    command = command.lower()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif command.startswith("play"):
        song = command.replace("play", "").strip()
        music_library = {
            "room": "https://www.youtube.com/watch?v=EHGsGJ4V3ZA",
            "metamorphosis": "https://www.youtube.com/watch?v=FSuGx2758Y4",
            "forever": "https://www.youtube.com/watch?v=oNjQXmoxiQ8"
        }
        #Can add as many as one want

        link = music_library.get(song)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find {song} in your music library.")

    elif "search for" in command:
        query = command.replace("search for", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "tell me about" in command:
        topic = command.replace("tell me about", "").strip()
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except:
            speak("Sorry, I couldn't find information on that topic.")

    elif "what's the time" in command or "what is the time" in command:
        speak(get_time())

    elif "what's the date" in command or "what is the date" in command:
        speak(get_date())

    elif "weather" in command:
        speak(get_weather())

    elif "remind me" in command:
        try:
            speak("What should I remind you about?")
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
                reminder_text = recognizer.recognize_google(audio)

            speak("In how many seconds?")
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
                delay = int(recognizer.recognize_google(audio))

            remind_me(reminder_text, delay)
            speak(f"Reminder set for {delay} seconds from now.")
        except:
            speak("Sorry, I couldn't set the reminder.")

    elif "shut down" in command or "shutdown" in command:
        speak("Shutting down. Goodbye!")
        exit()

    else:
        speak("I didn't understand that command.")

def main():
    """Main loop to listen for the wake word and execute commands"""
    speak("Golu Initialized. Awaiting your command.")

    while True:
        try:
            with sr.Microphone() as source:
                print("🎤 Listening for wake word 'Golu'...")
                audio = recognizer.listen(source)

            try:
                trigger = recognizer.recognize_google(audio)
                print("Heard:", trigger)

                # Check for variations of the wake word
                if any(w in trigger.lower() for w in ["golu", "go lu", "golo", "goloo"]):
                    speak("Yes bro, I'm listening.")
                    with sr.Microphone() as source:
                        print("🎤 Listening for your command...")
                        audio = recognizer.listen(source)

                    try:
                        command = recognizer.recognize_google(audio)
                        print("Command received:", command)
                        process_command(command)

                    except sr.UnknownValueError:
                        speak("Sorry, I couldn’t understand your command.")
                    except sr.RequestError:
                        speak("Speech recognition service is down.")
                    except Exception as e:
                        print("Command Error:", e)
                        speak("Something went wrong while processing your command.")

            except sr.UnknownValueError:
                print("Could not understand wake word.")
            except sr.RequestError:
                print("Speech recognition service unavailable.")
            except Exception as e:
                print("Wake Word Error:", e)

        except Exception as e:
            print("Mic Error:", e)

if __name__ == "__main__":
    main()
