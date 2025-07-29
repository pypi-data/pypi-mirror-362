from setuptools import setup, find_packages

setup(
    name="MiraAiSystems",
    version="0.1.9",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "google-generativeai",
        "rich",
        "ultralytics",
        "pyttsx3",
        "SpeechRecognition",
        "PyAudio"
    ],
    author="MoonTech",
    description="An AI system that using Gemini AI to do various tasks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
