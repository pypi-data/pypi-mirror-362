import os
from dotenv import load_dotenv
import google.generativeai as genai
import time as T
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text
console = Console()


# Load environment variables from .env file
load_dotenv()
a = ""

def ConAi(b):
    #ConAI(x): Register your API key before using any other Function, Place API key as x or register it in Activate
    
    global a
    if b == "":
        a = input("Enter API Key: ")
    else:
        a = b

def T1(x="", t=""):
    #T1(x,t): Translator function, Translate the Sentence X into the language T
    
    # User Inputs
    if not x.strip():
        x = input("Enter the text to translate: ")
    if not t.strip():
        t = input("Enter the target language (e.g., French, Hindi): ")

    genai.configure(api_key=a)
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        f"You are a translation agent. Translate this to {t}: '{x}'"
    )
    T.sleep(2)
    print("\nTranslated Text:")
    print(response.text)

def T2(x=""):
    #T2(x): Language Identifiers Function, Identify the Languagethat the text X written in
    
    if not x.strip():
        x = input("Enter the text to identify: ")

    genai.configure(api_key=a)
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        f"You are a language agent. Identify the language in this text: '{x}'"
    )
    T.sleep(2)
    print(response.text)

def T3(x=""):
    #T3(x): Text Definer and Explained Function, Define and Explain any language in world
    
    if not x.strip():
        x = input("Enter the text to understand: ")

    genai.configure(api_key=a)
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        f"You are a grammar expert. Explain the builder of the sentence '{x}' including phrases, clauses, helping verbs, idioms, etc."
    )
    T.sleep(2)
    print("\nExplanation:")
    print(response.text)

def T4():
    #T4(): Chatbot Function, Ask Pablo anything about Languages
    
    while True:
        x = input("Enter: ")
        if x.strip().lower() == "exit":
            print("Exiting...")
            T.sleep(1)
            break

        genai.configure(api_key=a)
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            f"You are a translator ChatBot and a guide. Your name is Pablo. Respond to this: {x}"
        )
        T.sleep(2)
        print(response.text)
import inspect

import inspect
import textwrap

def GameSafe(func):
    #GameSafe(x): GameSafe function, Fetch the Coding of X() function
    
    console = Console()

    try:
        source = inspect.getsource(func)
        lines = source.splitlines()
        body_lines = lines[1:]  
        dedented = textwrap.dedent('\n'.join(body_lines))

        syntax = Syntax(
            dedented,
            "python",
            theme="monokai",  
            line_numbers=True,
            word_wrap=True,
        )

        console.print(f"[bold bright_green]GameSafe: {func.__name__}()[/bold bright_green]")
        console.print(syntax, style="bright_green")

    except Exception as e:
        console.print(f"[red]# Error fetching code: {e}[/red]")
def Render(x=""):
    """Render: Ask anything to Gemini"""
    # User input
    if not x.strip():
        x = input("Enter the text to Render: ")
        
    genai.configure(api_key=a)
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        f"You are a AI. Answer to '{x}' question"
    )
    T.sleep(2)
    console.print(x, style="green")
    console.print(response.text, style="cyan")
import os
import time as T
import speech_recognition as sr
import pyttsx3
from rich import print



api_key = a
genai.configure(api_key=a)



def ActNLP():
    def speak(text):
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)  
        print(f"[cyan]{text}[/cyan]")  
        engine.say(text)
        engine.runAndWait()
    def listen():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("[yellow]Listening...[/yellow]")
            audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio)
            print(f"[green]You said:[/green] {query}")
            return query
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Speech recognition failed."
    while True:
        user_input = listen()
        genai.configure(api_key=a)
        if "exit" in user_input.lower():
            speak("Okay, exiting now!")
            return
            break
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"You are a frendly Ai named Rico respond to this '{user_input}'")
        T.sleep(2)
        speak(response.text)
import cv2

def ActCV():
    # ActCV: Activate Computer vision function
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)

    print("ActCV: Face Detection Activated. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("👁", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
from ultralytics import YOLO
import cv2

def ActCV_Yolo():
    # ActCV_Yolo: Activate Computer Vision Yolo Intregered function
    import cv2
    import logging
    from ultralytics import YOLO

    # Silence YOLO logs
    logging.getLogger("ultralytics").setLevel(logging.ERROR)

    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(0)

    print("ActCV: Hand Detection (Press 'q' to quit)")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result = model.predict(source=frame, conf=0.5, verbose=False)[0]

        boxes = result.boxes
        for box in boxes:
            cls = int(box.cls[0])
            label = model.names[cls]
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            cv2.rectangle(frame, tuple(xyxy[:2]), tuple(xyxy[2:]), (0, 255, 0), 2)
            cv2.putText(frame, label, tuple(xyxy[:2] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("👁", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()






    
        
    
