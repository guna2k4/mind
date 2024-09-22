import streamlit as st
import requests
import pyttsx3
import os

# Set your API key and endpoint
API_KEY = 'sk-tune-9ZXc1hIUkwfXsux9Wn1IA51Yx60NkdmzZrL'  # Replace with your actual API key
API_ENDPOINT = 'https://proxy.tune.app/chat/completions'

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to stop the speech (from voice.py)
def stop_speech():
    """Function to stop the speech."""
    engine.stop()

# Function to convert text to speech (from voice.py)
def text_to_speech(text):
    """Function to convert text to speech."""
    engine.say(text)
    engine.runAndWait()

# Function to save speech to an audio file
def save_speech_to_audio(text):
    engine = pyttsx3.init()
    audio_file = 'mindfulness_story.mp3'
    engine.save_to_file(text, audio_file)
    engine.runAndWait()
    return audio_file

# Function to send messages to the API (from app.py)
def send_message(mindfulness_prompt):
    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }
    
    data = {
        "temperature": 0.9,
        "messages": [
            {"role": "system", "content": "You are TuneStudio, generate a mindfulness story."},
            {"role": "user", "content": mindfulness_prompt}
        ],
        "model": "kaushikaakash04/tune-blob",
        "stream": False,
        "frequency_penalty": 0.2,
        "max_tokens": 200
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    return response.json()

# Streamlit app layout
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a Page", ["Mindfulness Goal Setter", "Mindfulness Story Player"])

# Mindfulness Goal Setter Page
if page == "Mindfulness Goal Setter":
    st.title('Mindfulness Goal Setter')

    # User input for task
    task = st.text_input("What is your task or goal?")

    if task:
        st.write("Please answer the following questions:")

        # Collecting user details
        possible_problems = st.text_input(" Problems you faced:")
        motivation = st.text_input("Motivation:")
        benefits = st.text_input("Benefits:")
        health_status = st.text_input("Health Status:")
        day_count = st.number_input("Day Count:", min_value=1, value=1)
        status = st.text_input("Status:")
        what_if_fail = st.text_input("What if you fail:")

        if st.button('Generate Mindfulness Story'):
            # Ensure all fields are filled
            if all([possible_problems, motivation, benefits, health_status, status, what_if_fail]):
                # Create the prompt for the API
                mindfulness_prompt = f"""
                Task: {task}
                Problems you faced: {possible_problems}
                Motivation: {motivation}
                Benefits: {benefits}
                Health Status: {health_status}
                Day Count: {day_count}
                Status: {status}
                What if I fail: {what_if_fail}
                Create a solution-based mindfulness story for the user to achieve this task today.
                combine all details to give me persnalise story this take 3 mintus readabel duration 
                """

                # Send the mindfulness prompt to the API
                with st.spinner("Generating mindfulness story..."):
                    response = send_message(mindfulness_prompt)
                    story = response.get('choices', [{}])[0].get('message', {}).get('content', 'No response received.')

                    # Display the story
                    st.write("Mindfulness Story:", story)

                    # Convert the story to speech and save as audio file
                    audio_file = save_speech_to_audio(story)
                    
                    # Provide a button to play the audio
                    if st.button("Play Meditation"):
                        st.audio(audio_file)

                    # Clean up the audio file after playing
                    if os.path.exists(audio_file):
                        os.remove(audio_file)

            else:
                st.warning("Please fill in all fields before generating the story.")
    else:
        st.info("Please enter your task to get started.")

# Mindfulness Story Player Page (from voice.py)
elif page == "Mindfulness Story Player":
    st.header("Enter and Hear Your Mindfulness Story")

    # Text input from user
    text_input = st.text_area("Enter the text you want to convert to speech:")

    # Create two columns for the buttons
    col1, col2 = st.columns(2)

    # Button to start speaking
    if col1.button("Speak"):
        if text_input:
            st.write("Reading text aloud...")
            text_to_speech(text_input)
        else:
            st.warning("Please enter some text first!")

    # Button to stop speaking
    if col2.button("Stop"):
        st.write("Stopping speech...")
        stop_speech()
