from setuptools import setup, find_packages

setup(
    name="MiraAiSystems",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "google-generativeai",
        "rich",
        "ultralytics",
        "pyttsx3",
        "SpeechRecognition",
        "PyAudio",
        "Pillow",         
        "PyPDF2",         
        "mutagen",        
        "pygame"           
    ],
    author="MoonTech",
    description="An AI system that uses Gemini AI to do various tasks including NLP, file operations, and media handling.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
