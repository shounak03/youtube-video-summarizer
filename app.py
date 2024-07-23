import streamlit as st
import os
from dotenv import load_dotenv
import re

load_dotenv()
import google.generativeai as genai

genai.configure(api_key=os.getenv("API_KEY"))

from youtube_transcript_api import YouTubeTranscriptApi

prompt="""you are a yt video summarizer, you'll be taking the
        transcript text and summarizing the entire video and
        providing the important summary in points within 300 words
        the transcript will be appended here: 
        """

def extract_trans_detail(url):
    try:
        id = url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(id)

        transcript = ""
        for i in transcript_text:
            transcript+=" "+i["text"] 
        
        return transcript

    except Exception as e:
        raise e

def generate_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

def extract_video_id(url):
    # This regex pattern matches both standard and shortened YouTube URLs
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|v\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None



st.title("YOUTUBE VIDEO SUMMARIZER")

link = st.text_input("ENTER THE YOUTUBE VIDEO LINK: ")

if link:
    video_id = extract_video_id(link)
    if video_id:
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
        st.image(thumbnail_url, use_column_width=True)
    else:
        st.error("Invalid YouTube URL. Please check the link and try again.")


if st.button("get detailed notes"):
    trans_text = extract_trans_detail(link)

    if(trans_text):
        summary = generate_content(trans_text,prompt)
        st.markdown("Detailed Notes")
        st.write(summary)
